#!/usr/bin/env python3
"""共识反推筛选：全市场"2028E 共识终局 vs 当前市值"分歧诊断。

用法: python3 consensus_screen.py [--window-days 180] [--k 0.85] [--r 0.10]
                                   [--min-orgs 2] [--top 15] [--out DIR]

对每只覆盖 ≥min-orgs 家券商的股票：
  V = k·Σ NP_t/(1+r)^t + k·NP_28/r/(1+r)^3   （t=1,2,3 对应 2026/27/28E 中位）
  ratio = V / 总市值
  ratio ≥ 1.5 → 深度分歧（市场深度怀疑共识，隐含 r 高）→ 预期差候选，去看市场对还是共识对
  ratio ≤ 0.7 → 叙事透支（价格超过"共识兑现并永续"的价值，隐含 r 极低）→ 需独立天花板证据
输出：research_data/screen/consensus_screen_<date>.csv + stdout 两端 top N。
状态：Candidate / Sandbox。固定 k、r 与卖方利润永续只是未经公司现金流桥验证的筛选假设，
不属于当前默认叙事估值模型。旗子只表示"分歧显著、值得去查"，不构成市场共识、
低估/高估或买卖结论；正式结论必须另做 Pass A、Pass B 与同口径现金流比较。
"""
import argparse
import csv
import datetime
import json
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ts import call, ROOT

CAP = 4800  # report_rc 单次返回上限 5000，留安全余量
TODAY = datetime.date.today()


def fetch_window(tool, args, start, end, date_key):
    """按日期窗口拉数，超上限则递归二分。"""
    a = dict(args)
    a['start_date'] = start.strftime('%Y%m%d')
    a['end_date'] = end.strftime('%Y%m%d')
    d = call(tool, a)
    rows = d if isinstance(d, list) else []
    if len(rows) < CAP or (end - start).days <= 3:
        return rows
    mid = start + (end - start) / 2
    return fetch_window(tool, args, start, mid, date_key) + fetch_window(tool, args, mid + datetime.timedelta(days=1), end, date_key)


def fetch_all_listed():
    """全市场上市股票（单次可完整返回）。"""
    rows = call('stock_basic', {'list_status': 'L'})
    return rows if isinstance(rows, list) else []


def fetch_daily_basic(date_str):
    """全市场单日 daily_basic（单次可完整返回，约 5500 行）。"""
    d = call('daily_basic', {'trade_date': date_str})
    return d if isinstance(d, list) else []


def median(v):
    return statistics.median(v) if v else None


def implied_r(mcap, nps, k, lo=0.02, hi=0.60):
    def V(r):
        disc = sum(nps[t - 1] * k / (1 + r) ** t for t in (1, 2, 3))
        return disc + nps[2] * k / r / (1 + r) ** 3
    if V(lo) < mcap:
        return None  # 隐含 r < 2%
    if V(hi) > mcap:
        return None  # 隐含 r > 60%
    for _ in range(60):
        mid = (lo + hi) / 2
        if V(mid) < mcap:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--window-days', type=int, default=180)
    ap.add_argument('--k', type=float, default=0.85)
    ap.add_argument('--r', type=float, default=0.10)
    ap.add_argument('--min-orgs', type=int, default=2)
    ap.add_argument('--top', type=int, default=15)
    ap.add_argument('--out', default=os.path.join(ROOT, 'research_data', 'screen'))
    a = ap.parse_args()

    end = TODAY
    start = end - datetime.timedelta(days=a.window_days)
    split = end - datetime.timedelta(days=a.window_days // 2)

    print(f'拉取 report_rc {start} ~ {end}（超限自动二分）...')
    rows = fetch_window('report_rc', {}, start, end, 'report_date')
    print(f'共 {len(rows)} 行')

    # 按股票分组：(code, org, 预测年) 保留最新一条；只取年度预测(Q4)
    per_stock = {}
    for r in rows:
        code = r.get('ts_code')
        q = r.get('quarter') or ''
        if not code or not q.endswith('Q4') or not r.get('np'):
            continue
        year = q[:4]
        if year not in ('2026', '2027', '2028'):
            continue
        key = (code, r.get('org_name'), year)
        cur = per_stock.get(key)
        if cur is None or (r.get('report_date') or '') > (cur.get('report_date') or ''):
            per_stock[key] = r

    by_code = {}
    for (code, org, year), r in per_stock.items():
        by_code.setdefault(code, {'org': {}, 'last': ''})
        by_code[code]['org'].setdefault(org, {})[year] = r['np'] / 1e4  # 万→亿
        by_code[code]['last'] = max(by_code[code]['last'], r.get('report_date') or '')

    print(f'有年度预测覆盖的股票: {len(by_code)}')

    basic = fetch_all_listed()
    meta = {b['ts_code']: b for b in basic if isinstance(b, dict) and b.get('ts_code')}
    dbp = fetch_daily_basic(end.strftime('%Y%m%d'))
    mcap = {d['ts_code']: d['total_mv'] / 1e4 for d in dbp if isinstance(d, dict) and d.get('total_mv')}
    close_map = {d['ts_code']: d.get('close') for d in dbp if isinstance(d, dict)}
    if not mcap:
        prev = fetch_daily_basic((end - datetime.timedelta(days=1)).strftime('%Y%m%d'))
        mcap = {d['ts_code']: d['total_mv'] / 1e4 for d in prev if isinstance(d, dict) and d.get('total_mv')}
        close_map = {d['ts_code']: d.get('close') for d in prev if isinstance(d, dict)}
    print(f'市值表: {len(mcap)} 只')

    out_rows = []
    skipped = {'单家覆盖': 0, '年份不全或非正': 0, '无市值': 0}
    for code, info in by_code.items():
        if code not in mcap or code not in meta:
            skipped['无市值'] += 1
            continue
        name = meta[code].get('name', '')
        if 'ST' in name or '退' in name:
            continue
        industry = meta[code].get('industry') or ''
        if any(w in industry for w in ('银行', '保险', '证券', '金融')):
            continue  # 金融资产负债表即经营原料，净利润 DCF 模型不适用（AGENTS.md 第八节）
        # 2028E 覆盖券商数与逐券商最新值
        np28_by_org = {o: y['2028'] for o, y in info['org'].items() if '2028' in y}
        if len(np28_by_org) < a.min_orgs:
            skipped['单家覆盖'] += 1
            continue
        np26_by_org = {o: y['2026'] for o, y in info['org'].items() if '2026' in y}
        np27_by_org = {o: y['2027'] for o, y in info['org'].items() if '2027' in y}
        np26, np27, np28 = median(list(np26_by_org.values())), median(list(np27_by_org.values())), median(list(np28_by_org.values()))
        if not (np26 and np27 and np28) or min(np26, np28) <= 0:
            skipped['年份不全或非正'] += 1
            continue
        nps = [np26, np27, np28]
        k, r0 = a.k, a.r
        V = sum(nps[t - 1] * k / (1 + r0) ** t for t in (1, 2, 3)) + nps[2] * k / r0 / (1 + r0) ** 3
        mc = mcap[code]
        ratio = V / mc
        ir = implied_r(mc, nps, k)
        # 隐含 r 越界时的方向标注：<2%（透支端）或 >60%（深度怀疑端）
        def _V(r):
            return sum(nps[t - 1] * k / (1 + r) ** t for t in (1, 2, 3)) + nps[2] * k / r / (1 + r) ** 3
        ir_note = ''
        if ir is None:
            ir_note = '<2%' if _V(0.02) < mc else '>60%'
        # 近 3 月 vs 前 3 月的 2028E 修正方向（逐券商最新值分层）
        new_m, old_m = [], []
        for o, y in info['org'].items():
            if '2028' not in y:
                continue
            d = per_stock[(code, o, '2028')].get('report_date', '')
            (new_m if d >= split.strftime('%Y%m%d') else old_m).append(y['2028'])
        if new_m and old_m:
            rev = f'{(median(new_m)/median(old_m)-1)*100:+.0f}%'
        elif new_m:
            rev = '新增'
        else:
            rev = ''
        flag = ('深度分歧(市场怀疑共识)' if ratio >= 1.5
                else '共识与定价脱钩(隐含r<2%)' if ir_note == '<2%'
                else '叙事透支(隐含r≤6%)' if (ir is not None and ir <= 0.06)
                else '中间')
        out_rows.append({
            'code': code, 'name': name, 'industry': meta[code].get('industry', ''),
            'close': close_map.get(code, ''), 'mcap_yi': round(mc, 1), 'n_orgs28': len(np28_by_org),
            'np26_yi': round(np26, 1), 'np27_yi': round(np27, 1), 'np28_yi': round(np28, 1),
            'np28_min': round(min(np28_by_org.values()), 1), 'np28_max': round(max(np28_by_org.values()), 1),
            'last_report': info['last'], 'recent_rev28': rev,
            'V_yi': round(V, 1), 'V_over_mcap': round(ratio, 2),
            'implied_r': '' if ir is None else f'{ir:.1%}',
            'implied_r_note': ir_note,
            'flag': flag,
        })

    out_rows.sort(key=lambda x: -x['V_over_mcap'])
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, f'consensus_screen_{end.strftime("%Y%m%d")}.csv')
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    deep = [r for r in out_rows if r['flag'].startswith('深度')]
    trans = [r for r in out_rows if r['flag'].startswith('叙事')]
    deco = [r for r in out_rows if r['flag'].startswith('共识与定价脱钩')]
    ratios = sorted(float(r['V_over_mcap']) for r in out_rows)
    n = len(ratios)
    pct = lambda p: ratios[min(n - 1, int(n * p / 100))]
    print(f"入表 {len(out_rows)} 只 | 深度分歧 {len(deep)} | 叙事透支(隐含r≤6%) {len(trans)} | 定价脱钩 {len(deco)} | 剔除: {skipped}")
    print(f"V/市值分布: P5={pct(5)} P25={pct(25)} 中位={pct(50)} P75={pct(75)} P95={pct(95)}（中位数偏离 1 越远，说明共识越没被市场全额买账）")
    print(f'已写入 {path}')
    print(f"\n===== 深度分歧 top{a.top}（市场深度怀疑共识——去看市场对还是共识对）=====")
    print(f"{'代码':<10}{'名称':<8}{'行业':<10}{'市值':>7}{'28E中位':>8}{'覆盖':>4}{'V/市值':>7}{'隐含r':>7} 近修")
    for r in deep[:a.top]:
        print(f"{r['code']:<10}{r['name']:<8}{r['industry']:<10}{r['mcap_yi']:>7}{r['np28_yi']:>8}{r['n_orgs28']:>4}{r['V_over_mcap']:>7}{r['implied_r'] or '—':>7} {r['recent_rev28']}")
    print(f"\n===== 叙事透支 top{a.top}（价格超过共识兑现并永续——需独立天花板证据）=====")
    for r in trans[:a.top]:
        print(f"{r['code']:<10}{r['name']:<8}{r['industry']:<10}{r['mcap_yi']:>7}{r['np28_yi']:>8}{r['n_orgs28']:>4}{r['V_over_mcap']:>7}{r['implied_r'] or '—':>7} {r['recent_rev28']}")

    json.dump({'date': end.isoformat(), 'method_status': 'candidate_sandbox_not_formal_valuation',
               'params': {'k': a.k, 'r': a.r, 'window_days': a.window_days, 'min_orgs': a.min_orgs},
               'n_rows': len(rows), 'n_stocks': len(out_rows), 'n_deep': len(deep), 'n_transcendent': len(trans)},
              open(os.path.join(a.out, f'consensus_screen_{end.strftime("%Y%m%d")}_meta.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
