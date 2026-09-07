#!/usr/bin/env python3
"""Tushare MCP 直连取数脚本库——个股数据包
用法: python3 ts.py valuation <ts_code>  # 叙事估值全量数据包（落盘+摘要，估值首选）
      python3 ts.py package <ts_code>   # 轻量包（保留兼容）
      python3 ts.py call <tool> '<json_args>'   # 任意接口单次调用
URL 从项目根 .mcp.json 读取（凭据不入库、不入脚本）。
原始响应全部落盘 research_data/data/<code>/；stdout 只打印摘要，避免上下文膨胀。
"""
import datetime
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
URL = json.load(open(os.path.join(ROOT, '.mcp.json')))['mcpServers']['tushareMcp']['url']

def call(tool, args):
    """单次 MCP tools/call，解析 SSE 响应，返回解析后的数据"""
    import urllib.request
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                       "params": {"name": tool, "arguments": args}}).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Content-Type": "application/json", "Accept": "application/json, text/event-stream"})
    raw = urllib.request.urlopen(req, timeout=60).read().decode()
    for line in raw.splitlines():
        if line.startswith('data: '):
            resp = json.loads(line[6:])
            if resp.get('error'): raise RuntimeError(f"MCP error: {resp['error']}")
            text = resp['result']['content'][0]['text']
            try: return json.loads(text)
            except json.JSONDecodeError: return text
    raise RuntimeError(f"无 data 行: {raw[:200]}")

def yi(v):
    """亿格式化，空值返回占位符"""
    return f"{v/1e8:.2f}亿" if isinstance(v, (int, float)) else "—"

def _fetch(out, name, tool, args, gaps):
    """拉取并落盘；返回行列表。空结果/异常文本记入 gaps，不中断整包。"""
    try:
        d = call(tool, args)
    except Exception as e:
        gaps.append(f"{tool}({args}): 调用失败 {str(e)[:80]}")
        print(f"[{tool}] 调用失败: {str(e)[:60]}")
        return []
    if isinstance(d, str):
        gaps.append(f"{tool}({args}): 返回非结构化文本")
        json.dump({'raw_text': d[:5000]}, open(os.path.join(out, name), 'w'), ensure_ascii=False)
        print(f"[{tool}] 返回异常文本，已落盘 {name}")
        return []
    json.dump(d, open(os.path.join(out, name), 'w'), ensure_ascii=False)
    n = len(d) if isinstance(d, list) else 1
    if not n:
        gaps.append(f"{tool}({args}): 空结果")
    return d if isinstance(d, list) else []

def latest_by_period(rows):
    """多报表类型/多公告轮次去重：同报告期保留公告日最新一行"""
    periods = {}
    for r in rows:
        p = r.get('end_date')
        if not p: continue
        cur = periods.get(p)
        if cur is None or (r.get('ann_date') or '') > (cur.get('ann_date') or ''):
            periods[p] = r
    return periods

def package(code):
    """轻量数据包（保留兼容）：身份/季度利润/现金流/行情"""
    out = os.path.join(ROOT, 'research_data', 'data', code)
    os.makedirs(out, exist_ok=True)
    save = lambda name, data: json.dump(data, open(os.path.join(out, name), 'w'), ensure_ascii=False)

    basic = call('stock_basic', {'ts_code': code})
    assert basic, f"{code} 不存在"
    save('basic.json', basic)
    print(f"[basic] {basic[0]['name']} | 行业{basic[0]['industry']} | 上市{basic[0]['list_date']} | 实控人 {basic[0].get('act_name')}")

    inc = call('income', {'ts_code': code, 'start_date': '20240101', 'end_date': '20261231'})
    save('income_q.json', inc)
    periods = latest_by_period(inc)
    print('[income] 单季差分（亿）:')
    prev = None
    prev_p = ''
    for p in sorted(periods):
        r = periods[p]
        rev, cost, np_ = r['revenue']/1e8, (r.get('oper_cost') or 0)/1e8, r['n_income_attr_p']/1e8
        gm = (rev-cost)/rev*100 if rev else 0
        dq = f" 单季{np_-prev:.2f}" if prev is not None and p[4:6] != '12' and p[:4] == prev_p[:4] else ""
        print(f"  {p}: 营收{rev:.1f} 毛利率{gm:.1f}% 归母{np_:.2f}{dq}")
        prev, prev_p = np_, p
    assert periods, "income 为空"

    cf = call('cashflow', {'ts_code': code, 'start_date': '20250101', 'end_date': '20261231'})
    save('cashflow_q.json', cf)
    print('[cashflow] 经营净现金流/购建固定资产（亿）:')
    for p, r in sorted(latest_by_period(cf).items()):
        if p in ('20251231', '20260630'):
            print(f"  {p}: OCF {(r.get('n_cashflow_act') or 0)/1e8:.2f} capex {(r.get('c_pay_acq_const_fiolta') or 0)/1e8:.2f}")

    dbp = call('daily_basic', {'ts_code': code, 'start_date': '20250101', 'end_date': '20261231'})
    save('daily_basic.json', dbp)
    dbp = sorted(dbp, key=lambda r: r['trade_date'])
    last = dbp[-1] if dbp else None
    if last and last.get('pe_ttm'):
        ttm = last['total_mv']/last['pe_ttm']/1e4
        print(f"[daily_basic] 最新 {last['trade_date']} close {last['close']} PE_TTM {last['pe_ttm']:.1f} 市值 {last['total_mv']/1e4:.0f}亿 TTM净利≈{ttm:.1f}亿")
    assert len(dbp) > 50, f"行情序列过短: {len(dbp)}"
    print(f"已写入 {out}/（4 个文件）")

def valuation(code):
    """叙事估值全量数据包：一次拉齐 Memo 所需接口，落盘后只打印摘要。"""
    out = os.path.join(ROOT, 'research_data', 'data', code)
    os.makedirs(out, exist_ok=True)
    gaps = []
    Y = datetime.date.today().year
    START, END = f"{Y-6}0101", f"{Y+1}1231"

    # 1 主体确认
    basic = _fetch(out, 'basic.json', 'stock_basic', {'ts_code': code}, gaps)
    assert basic, f"{code} 不存在"
    b = basic[0]
    print(f"[basic] {b['name']} | 行业{b.get('industry')} | 上市{b.get('list_date')} | 实控人 {b.get('act_name')}")

    # 2 利润表：年度序列 + 最新报告期
    inc = _fetch(out, 'income.json', 'income', {'ts_code': code, 'start_date': START, 'end_date': END}, gaps)
    periods = latest_by_period(inc)
    annuals = {p: r for p, r in periods.items() if p.endswith('1231')}
    print('[income] 年度: 营收(同比)/归母（亿）')
    prev_rev = None
    for p in sorted(annuals):
        r = annuals[p]
        rev, np_ = (r.get('revenue') or 0)/1e8, (r.get('n_income_attr_p') or 0)/1e8
        yoy = f" +{(rev/prev_rev-1)*100:.0f}%" if prev_rev else ""
        print(f"  {p}: {rev:.1f}{yoy} / {np_:.2f}")
        prev_rev = rev
    if periods:
        p = max(periods)
        r = periods[p]
        rev = r.get('revenue') or 1
        gm = (rev - (r.get('oper_cost') or 0)) / rev * 100
        print(f"  最新 {p}: 营收{rev/1e8:.1f} 归母{(r.get('n_income_attr_p') or 0)/1e8:.2f} 毛利率{gm:.1f}%")

    # 3 现金流量表
    cf = _fetch(out, 'cashflow.json', 'cashflow',
                {'ts_code': code, 'start_date': START, 'end_date': END, 'report_type': '1'}, gaps)
    cfp = latest_by_period(cf)
    print('[cashflow] 最近报告期: OCF/购建capex/投资净/筹资净/期末现金（亿）')
    for p in sorted(cfp)[-6:]:
        r = cfp[p]
        print(f"  {p}: {(r.get('n_cashflow_act') or 0)/1e8:.1f} / {(r.get('c_pay_acq_const_fiolta') or 0)/1e8:.1f}"
              f" / {(r.get('n_cashflow_inv_act') or 0)/1e8:.1f} / {(r.get('n_cash_flows_fnc_act') or 0)/1e8:.1f}"
              f" / {yi(r.get('end_bal_cash'))}")

    # 4 资产负债表（近两年公告窗口内最新报告期）
    bs = _fetch(out, 'balancesheet.json', 'balancesheet',
                {'ts_code': code, 'start_date': f"{Y-1}0101", 'end_date': END}, gaps)
    bsp = latest_by_period(bs)
    if bsp:
        p = max(bsp)
        r = bsp[p]
        cash = next((r.get(k) for k in ('monetary_cap', 'cash_ce', 'cash_reser_cb') if r.get(k) is not None), None)
        cash_src = '货币资金'
        if cash is None and cfp and cfp.get(p, {}).get('end_bal_cash') is not None:
            cash = cfp[p]['end_bal_cash']  # 货币资金字段缺失时回退现金流量表期末现金
            cash_src = '现金流量表期末现金'
        debt = sum(r.get(k) or 0 for k in ('st_borr', 'noncur_liab_1yr', 'lt_borr', 'bond_payable'))
        print(f"[balancesheet] {p}: 总股本{yi(r.get('total_share'))} 归母权益{yi(r.get('total_hldr_eqy_exc_min_int'))}"
              f" 少数股东{yi(r.get('minority_int'))}")
        if cash is not None:
            print(f"  有息负债约{yi(debt)}（短借+1年内到期+长借+债券） 现金{yi(cash)}({cash_src})"
                  f" 净现金/净负债 {(cash-debt)/1e8:+.1f}亿")
        else:
            print(f"  有息负债约{yi(debt)}（短借+1年内到期+长借+债券） 现金字段缺失，请用现金流量表 end_bal_cash 核对")
        if (r.get('bond_payable') or 0) > (r.get('total_assets') or 1) * 0.01:
            print("  [提示] 应付债券占比>1%：转债转股价/余额需查转股结果公告或集思录，Tushare cb_basic 需债券代码")
    else:
        print("[balancesheet] 无数据")

    # 5 财务指标（年度）
    fi = _fetch(out, 'fina_indicator.json', 'fina_indicator',
                {'ts_code': code, 'start_date': START, 'end_date': END}, gaps)
    fip = {p: r for p, r in latest_by_period(fi).items() if p.endswith('1231')}
    print('[fina_indicator] 年度: 扣非ROE/资产负债率/毛利率/净利率')
    for p in sorted(fip)[-5:]:
        r = fip[p]
        print(f"  {p}: {r.get('roe_dt')} / {r.get('debt_to_assets')} / {r.get('grossprofit_margin')} / {r.get('netprofit_margin')}")

    # 6 业绩预告/快报（近两年）
    fc = _fetch(out, 'forecast.json', 'forecast', {'ts_code': code, 'start_date': f"{Y-1}0101", 'end_date': END}, gaps)
    for r in sorted(fc, key=lambda x: x.get('ann_date') or '')[-4:]:
        print(f"[forecast] {r.get('ann_date')} {r.get('end_date')} {r.get('type')}"
              f" {r.get('p_change_min')}~{r.get('p_change_max')}% {(r.get('summary') or '')[:40]}")
    _fetch(out, 'express.json', 'express', {'ts_code': code, 'start_date': f"{Y-1}0101", 'end_date': END}, gaps)

    # 7 分红
    dv = _fetch(out, 'dividend.json', 'dividend', {'ts_code': code}, gaps)
    seen = set()
    rows = []
    for r in dv:
        k = (r.get('end_date'), r.get('div_proc'))
        if k not in seen:
            seen.add(k)
            rows.append(r)
    print('[dividend] 最近分配:')
    for r in rows[:4]:
        print(f"  {r.get('end_date')} {r.get('div_proc')} 每股 {r.get('cash_div_tax')}")

    # 8 卖方预测集聚合（近6个月，过期预测会拉偏中位数）
    rc_since = (datetime.date.today() - datetime.timedelta(days=180)).strftime('%Y%m%d')
    rc = _fetch(out, 'report_rc.json', 'report_rc', {'ts_code': code, 'start_date': rc_since, 'end_date': END}, gaps)
    if rc:
        byyr = {}
        orgs = set()
        for r in rc:
            y = (r.get('quarter') or '')[:4]
            orgs.add((r.get('report_date'), r.get('org_name')))
            if y and int(y) >= Y:
                byyr.setdefault(y, {'np': [], 'rev': []})
                if r.get('np'): byyr[y]['np'].append(r['np'])
                if r.get('op_rt'): byyr[y]['rev'].append(r['op_rt'])
        latest_date = max(r.get('report_date') or '' for r in rc)
        print(f"[report_rc] 行数{len(rc)} 报告数{len(orgs)} 最新{latest_date}")
        for y in sorted(byyr):
            npv, rv = byyr[y]['np'], byyr[y]['rev']
            if npv:
                print(f"  {y}E: 归母中位{statistics.median(npv)/1e4:.1f}亿 均值{statistics.mean(npv)/1e4:.1f}亿"
                      f" 区间{min(npv)/1e4:.1f}-{max(npv)/1e4:.1f} n={len(npv)}"
                      + (f" 营收中位{statistics.median(rv)/1e4:.0f}亿" if rv else ""))

    # 9 行情/市值（近40天）
    since = (datetime.date.today() - datetime.timedelta(days=40)).strftime('%Y%m%d')
    dbp = _fetch(out, 'daily_basic.json', 'daily_basic', {'ts_code': code, 'start_date': since, 'end_date': END}, gaps)
    if dbp:
        last = sorted(dbp, key=lambda x: x['trade_date'])[-1]
        mv_yi = f"{last['total_mv']/1e4:.1f}亿" if last.get('total_mv') else "—"  # total_mv 单位为万元
        print(f"[daily_basic] {last['trade_date']} close {last['close']} PE_TTM {last.get('pe_ttm')} PB {last.get('pb')}"
              f" 总市值{mv_yi} 总股本{last.get('total_share')}万股 换手{last.get('turnover_rate')}%")

    # 10 分部数据（尽力而为，常见为空）
    if annuals:
        mb = _fetch(out, 'fina_mainbz.json', 'fina_mainbz',
                    {'ts_code': code, 'period': max(annuals), 'report_type': '2'}, gaps)
        if mb and mb[0].get('main_business'):
            for r in mb[:6]:
                print(f"[fina_mainbz] {r.get('type')} {r.get('main_business')}"
                      f" 收入{yi(r.get('main_business_income'))} 毛利率{r.get('gross_profit_margin')}")

    nfiles = len([f for f in os.listdir(out) if f.endswith('.json')])
    print(f"\n已写入 {out}/（{nfiles} 个文件）")
    if gaps:
        print('数据缺口（需记入 Memo）:')
        for g in gaps:
            print(f"  - {g}")

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] in ('package', 'valuation'):
        {'package': globals()['package'], 'valuation': valuation}[sys.argv[1]](sys.argv[2])
    elif len(sys.argv) >= 4 and sys.argv[1] == 'call':
        print(json.dumps(call(sys.argv[2], json.loads(sys.argv[3])), ensure_ascii=False, indent=1)[:3000])
    else:
        print(__doc__)
