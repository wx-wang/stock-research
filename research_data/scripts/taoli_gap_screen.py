#!/usr/bin/env python3
"""陶博士净利润断层选股：在业绩达标名单上叠加 RPS 强度、跳空断层与趋势层。

用法: python3 taoli_gap_screen.py [--input CSV] [--rps-min 87] [--gap-min 3.0]
                                  [--vol-min 1.5] [--out DIR]

层级（全部用 Tushare 日线，基准日为最近收盘）：
  L1 业绩层   输入名单（默认 h1_growth50_strict，量/利/扣非三口径≥50% 且 H1 归母>1亿）
  L2 强度层   RPS250≥阈值 且 RPS120≥阈值（全市场复权区间涨幅百分位 1-99）
  L3 断层层   公告日次一交易日 跳空≥gap_min%、量≥前5日均量×vol_min%、缺口至今未回补
  L4 趋势层   收盘>MA50>MA200（Stage 2 简化）
输出: research_data/screen/taoli_gap_<date>.csv + meta.json，stdout 打印分层结果。
仅为研究入口，不构成买卖结论。
"""
import argparse
import csv
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ts import call, ROOT

REF_DATE = '20260902'  # 最近收盘基准日
FIELDS = 'ts_code,trade_date,open,high,low,close,vol'


def paged(tool, args):
    rows, off = [], 0
    while True:
        d = call(tool, dict(args, limit=3000, offset=off))
        if not isinstance(d, list):
            raise RuntimeError(f"{tool}: {str(d)[:150]}")
        rows += d
        if len(d) < 3000:
            return rows
        off += 3000


def trading_days():
    d = call('trade_cal', {'exchange': 'SSE', 'is_open': '1',
                           'start_date': '20240101', 'end_date': REF_DATE})
    days = sorted(r['cal_date'] for r in d)
    return days


def market_adj_close(days):
    """全市场指定交易日复权收盘（daily×adj_factor 按日全市场拉取，各1次调用）。"""
    out = {}
    for dt in days:
        px = {r['ts_code']: r for r in call('daily', {'trade_date': dt})}  # 该工具不支持 fields 过滤
        af = {r['ts_code']: r for r in call('adj_factor', {'trade_date': dt})}
        for c, r in px.items():
            if r.get('close') and af.get(c, {}).get('adj_factor'):
                out[(c, dt)] = r['close'] * af[c]['adj_factor']
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', default=os.path.join(ROOT, 'research_data', 'screen',
                                                    'h1_growth50_2026-09-03_strict.csv'))
    ap.add_argument('--rps-min', type=float, default=87.0)
    ap.add_argument('--gap-min', type=float, default=3.0)
    ap.add_argument('--vol-min', type=float, default=1.5)
    ap.add_argument('--out', default=os.path.join(ROOT, 'research_data', 'screen'))
    args = ap.parse_args()
    today = datetime.date.today().isoformat()

    cands = list(csv.DictReader(open(args.input)))
    print(f"[L1] 业绩层输入 {len(cands)} 家", file=sys.stderr)

    # 交易日历与 RPS 全市场收益
    days = trading_days()
    assert days[-1] == REF_DATE
    d250, d120 = days[-251], days[-121]
    px = market_adj_close([d250, d120, REF_DATE])
    print(f"[RPS] 区间 {d250}→{REF_DATE}(250日) {d120}→{REF_DATE}(120日)", file=sys.stderr)
    all_codes = {c for c, _ in px}
    r250, r120 = {}, {}
    for c in all_codes:
        a, b, z = px.get((c, d250)), px.get((c, d120)), px.get((c, REF_DATE))
        if a and z: r250[c] = z / a - 1
        if b and z: r120[c] = z / b - 1

    def rps(rets):
        v = sorted(rets.values())
        n = len(v)
        return {c: (sum(1 for x in v if x < r) + 1) / n * 100 for c, r in rets.items()}
    rp250, rp120 = rps(r250), rps(r120)

    # 逐股日线：断层（中报公告日 + 业绩预告日）+ 趋势
    fc = paged('forecast_vip', {'period': '20260630',
                                'fields': ['ts_code', 'ann_date', 'type', 'p_change_min', 'p_change_max']})
    fc_ann = {}
    for r in fc:
        if r.get('ann_date') and (r['ts_code'] not in fc_ann or r['ann_date'] < fc_ann[r['ts_code']]['ann_date']):
            fc_ann[r['ts_code']] = r  # 同一公司多轮预告取最早（市场首次反应）
    print(f"[forecast] 20260630 预告 {len(fc_ann)} 家", file=sys.stderr)

    def gap_metrics(d, ann):
        """公告日 ann 的断层指标：跳空%、量比、缺口状态、断层后涨跌。"""
        pre = [r for r in d if r['trade_date'] <= ann]
        post = [r for r in d if r['trade_date'] > ann]
        if not pre or not post or not post[0].get('open'):
            return None, None, '无反应数据', None
        prev_close, g = pre[-1]['close'], post[0]
        gap_pct = (g['open'] / prev_close - 1) * 100
        vols5 = [r['vol'] for r in d if r['trade_date'] < g['trade_date']][-5:]
        vol_ratio = g['vol'] / (sum(vols5) / len(vols5)) if vols5 and sum(vols5) > 0 else None
        lows = [r['low'] for r in post if r.get('low') is not None]
        if lows and min(lows) <= prev_close:
            status = '已回补'
        elif lows and min(lows) < g['open']:
            status = '部分回补'
        else:
            status = '未回补'
        since = round((d[-1]['close'] / g['close'] - 1) * 100, 1) if d[-1].get('close') else None
        return round(gap_pct, 2), (round(vol_ratio, 2) if vol_ratio else None), status, since

    start = '20250901'  # 覆盖 MA200 所需约215个交易日
    rows_out = []
    for cand in cands:
        code = cand['code']
        try:
            d = call('daily', {'ts_code': code, 'start_date': start, 'end_date': REF_DATE})
        except Exception as e:
            print(f"  [daily] {code} 失败 {str(e)[:60]}", file=sys.stderr)
            d = []
        if not isinstance(d, list) or not d:
            rows_out.append({**cand, 'rps250': rp250.get(code), 'rps120': rp120.get(code),
                             'gap_pct': None, 'vol_ratio': None, 'gap_status': '无数据',
                             'fc_date': None, 'fc_gap_pct': None, 'fc_gap_status': None,
                             'stage2': '', 'since_gap': None})
            continue
        d.sort(key=lambda r: r['trade_date'])
        gap_pct, vol_ratio, gap_status, since_gap = gap_metrics(d, cand['ann_date'])
        fcr = fc_ann.get(code)
        fc_date = fcr['ann_date'] if fcr else None
        fc_gap = gap_metrics(d, fc_date) if fc_date and fc_date != cand['ann_date'] else (None, None, None, None)
        # 趋势：Stage 2 简化
        closes = [r['close'] for r in d if r.get('close')]
        stage2 = ''
        if len(closes) >= 200:
            ma50 = sum(closes[-50:]) / 50
            ma200 = sum(closes[-200:]) / 200
            if closes[-1] > ma50 > ma200:
                stage2 = 'Y'
        rows_out.append({**cand, 'rps250': round(rp250[code], 1) if code in rp250 else None,
                         'rps120': round(rp120[code], 1) if code in rp120 else None,
                         'gap_pct': gap_pct, 'vol_ratio': vol_ratio, 'gap_status': gap_status,
                         'fc_date': fc_date, 'fc_gap_pct': fc_gap[0], 'fc_vol_ratio': fc_gap[1],
                         'fc_gap_status': fc_gap[2],
                         'stage2': stage2, 'since_gap': since_gap})

    # L1.5 机构背书层：北向持股变化 + 十大流通股东机构占比变化 + 股东户数变化
    INST_KW = ('基金', '资管', '理财', '社保', '养老', 'qfii', '保险', '信托',
               '香港中央结算', '银行', '证金', '汇金', '资本', '投资')
    for r in rows_out:
        code = r['code']
        try:
            hk = call('hk_hold', {'ts_code': code})
            hks = sorted((x for x in hk if isinstance(x, dict) and x.get('ratio') is not None),
                         key=lambda x: x['trade_date']) if isinstance(hk, list) else []
            r['hk_ratio'] = hks[-1]['ratio'] if len(hks) >= 1 else None
            r['hk_chg'] = round(hks[-1]['ratio'] - hks[-2]['ratio'], 2) if len(hks) >= 2 else None
        except Exception:
            r['hk_ratio'], r['hk_chg'] = None, None
        try:
            tf = call('top10_floatholders', {'ts_code': code})
            per_q = {}
            if isinstance(tf, list):
                for x in tf:
                    per_q.setdefault(x.get('end_date'), []).append(x)
            qs = sorted(q for q in per_q if q)[-2:]
            def inst_share(q):
                inst = [x for x in per_q[q]
                        if any(k in (x.get('holder_name') or '').lower() for k in INST_KW)]
                return len(inst), sum(x.get('hold_ratio') or 0 for x in inst)
            if len(qs) == 2:
                n1, s1 = inst_share(qs[0]); n2, s2 = inst_share(qs[1])
                r['inst_n'] = f"{n2}/{n1}"
                r['inst_chg'] = round(s2 - s1, 2)
            else:
                r['inst_n'], r['inst_chg'] = None, None
        except Exception:
            r['inst_n'], r['inst_chg'] = None, None
        try:
            hn = call('stk_holdernumber', {'ts_code': code})
            hns = sorted({x['end_date']: x['holder_num'] for x in hn
                          if isinstance(x, dict) and x.get('holder_num')}.items())
            if len(hns) >= 2 and hns[-2][1]:
                chg = (hns[-1][1] / hns[-2][1] - 1) * 100
                r['holder_chg'] = round(chg, 1)
            else:
                r['holder_chg'] = None
        except Exception:
            r['holder_chg'] = None
        pos = (r['hk_chg'] or 0) > 0 or (r['inst_chg'] or 0) > 0 or (r['holder_chg'] or 0) < 0
        r['inst_pass'] = 'Y' if pos else ''

    # 分层判定：断层在"中报公告日"或"业绩预告日"任一成立即可
    def gap_ok(pct, vol, status):
        return (pct or -99) >= args.gap_min and (vol or 0) >= args.vol_min and status == '未回补'
    def L2(r): return (r['rps250'] or 0) >= args.rps_min and (r['rps120'] or 0) >= args.rps_min
    def L3(r): return gap_ok(r['gap_pct'], r['vol_ratio'], r['gap_status']) or \
        gap_ok(r['fc_gap_pct'], r['fc_vol_ratio'], r['fc_gap_status'])
    for r in rows_out:
        r['pass2'], r['pass3'] = 'Y' if L2(r) else '', 'Y' if L3(r) else ''
        r['all_pass'] = 'Y' if (L2(r) and L3(r) and r['stage2'] == 'Y' and r['inst_pass'] == 'Y') else ''

    rows_out.sort(key=lambda r: (r['all_pass'] == 'Y', r['pass3'] == 'Y', r['gap_pct'] or -99), reverse=True)
    n2 = sum(1 for r in rows_out if r['pass2'])
    n3 = sum(1 for r in rows_out if r['pass3'])
    nall = sum(1 for r in rows_out if r['all_pass'])
    ninst = sum(1 for r in rows_out if r['inst_pass'])

    out_csv = os.path.join(args.out, f'taoli_gap_{today}.csv')
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows_out[0].keys()))
        w.writeheader()
        w.writerows(rows_out)
    meta = {'date': today, 'input': os.path.basename(args.input), 'n_input': len(cands),
            'rps_min': args.rps_min, 'gap_min': args.gap_min, 'vol_min': args.vol_min,
            'rps_window': [d250, d120, REF_DATE], 'n_L1.5_inst': ninst, 'n_L2': n2,
            'n_L3': n3, 'n_all': nall}
    json.dump(meta, open(os.path.join(args.out, f'taoli_gap_{today}_meta.json'), 'w'),
              ensure_ascii=False, indent=1)

    # stdout 摘要
    print(json.dumps(meta, ensure_ascii=False))
    def show(title, rows):
        print(f"\n== {title}（{len(rows)}家）==")
        for r in rows:
            fc = f"预告{r['fc_date']} 跳空{r['fc_gap_pct']}% {r['fc_gap_status']}" if r['fc_date'] else "无预告"
            print(f"{r['code']} {r['name']:<8} RPS {r['rps250']}/{r['rps120']} "
                  f"机构[北向{r['hk_chg']} 十大机构{r['inst_chg']} 户数{r['holder_chg']}% {r['inst_pass'] or '未过'}] "
                  f"中报跳空{r['gap_pct']}% {r['gap_status']} | {fc} | 趋势{r['stage2'] or 'N'}")
    show('L1.5+L2+L3+L4 全过', [r for r in rows_out if r['all_pass']])
    show('业绩×强度×断层×趋势 过、仅缺机构层', [r for r in rows_out
          if r['pass2'] and r['pass3'] and r['stage2'] == 'Y' and not r['all_pass']])
    show('L2 强度+机构 过（断层未成立）', [r for r in rows_out if r['pass2'] and r['inst_pass'] and not r['pass3']])
    print(f"\n已写入 {out_csv}")


if __name__ == '__main__':
    main()
