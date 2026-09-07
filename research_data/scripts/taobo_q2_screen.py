#!/usr/bin/env python3
"""陶博士口径净利润断层选股（原教版 L1）：
  L1 单季净利：Q2 单季归母同比 ≥min_yoy(25%) 且增速比 Q1 加速，基数为正
  L2 强度：RPS250 与 RPS120 双 ≥rps_min(87)
  L3 断层：中报公告日或业绩预告日，次日跳空≥gap_min%、量≥前5日均量×vol_min、缺口未回补
  L4 趋势：收盘>MA50>MA200
  L1.5 机构：北向/十大流通机构/股东户数任一改善
超预期没有直接数据，用"公告/预告日跳空反应"作市场投票代理，预告类型附列。
用法: python3 taobo_q2_screen.py [--min-yoy 25] [--rps-min 87] [--gap-min 3.0] [--vol-min 1.5]
"""
import argparse
import csv
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ts import call, ROOT

REF_DATE = '20260902'
FIELDS = 'ts_code,trade_date,open,high,low,close,vol'
INST_KW = ('基金', '资管', '理财', '社保', '养老', 'qfii', '保险', '信托',
           '香港中央结算', '银行', '证金', '汇金', '资本', '投资')


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


def latest_map(rows):
    """同公司多轮公告取 ann_date 最新。"""
    best = {}
    for r in rows:
        c = r.get('ts_code')
        if not c:
            continue
        if c not in best or (r.get('ann_date') or '') > (best[c].get('ann_date') or ''):
            best[c] = r
    return best


def cum_profit_map(period):
    m = latest_map(paged('income_vip', {'period': period, 'report_type': '1',
                                        'fields': ['ts_code', 'ann_date', 'end_date', 'n_income_attr_p']}))
    return {c: r['n_income_attr_p'] for c, r in m.items() if r.get('n_income_attr_p') is not None}, m


def rps_full():
    days = sorted(r['cal_date'] for r in call('trade_cal', {'exchange': 'SSE', 'is_open': '1',
                                                            'start_date': '20240101', 'end_date': REF_DATE}))
    d250, d120 = days[-251], days[-121]
    px = {}
    for dt in (d250, d120, REF_DATE):
        pxd = {r['ts_code']: r for r in call('daily', {'trade_date': dt})}
        af = {r['ts_code']: r for r in call('adj_factor', {'trade_date': dt})}
        for c, r in pxd.items():
            if r.get('close') and af.get(c, {}).get('adj_factor'):
                px[(c, dt)] = r['close'] * af[c]['adj_factor']
    codes = {c for c, _ in px}
    rets = {}
    for w, dt0 in ((250, d250), (120, d120)):
        rets[w] = {c: px[(c, REF_DATE)] / px[(c, dt0)] - 1 for c in codes
                   if (c, dt0) in px and (c, REF_DATE) in px}
    def rps(ret):
        v = sorted(ret.values())
        return {c: round((sum(1 for x in v if x < r) + 1) / len(v) * 100, 1) for c, r in ret.items()}
    return rps(rets[250]), rps(rets[120]), d250, d120


def gap_metrics(d, ann):
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--min-yoy', type=float, default=25.0)
    ap.add_argument('--rps-min', type=float, default=87.0)
    ap.add_argument('--gap-min', type=float, default=3.0)
    ap.add_argument('--vol-min', type=float, default=1.5)
    ap.add_argument('--out', default=os.path.join(ROOT, 'research_data', 'screen'))
    args = ap.parse_args()
    today = datetime.date.today().isoformat()

    # L1 单季净利同比与加速
    h1_26, m26 = cum_profit_map('20260630')
    q1_26, _ = cum_profit_map('20260331')
    fy25, _ = cum_profit_map('20251231')
    h1_25, _ = cum_profit_map('20250630')
    q1_25, _ = cum_profit_map('20250331')
    fy24, _ = cum_profit_map('20241231')
    rows = []
    for c in {r for r in m26}:
        need = (q1_26.get(c), fy25.get(c), h1_25.get(c), q1_25.get(c), fy24.get(c))
        if any(v is None for v in need) or c not in m26 or not m26[c].get('n_income_attr_p'):
            continue
        q2_26 = m26[c]['n_income_attr_p'] - need[0]; q1_26s = need[0] - need[1]
        q2_25 = need[2] - need[3]; q1_25s = need[3] - need[4]
        if min(q2_25, q1_25s) <= 0:
            continue
        q2_yoy = (q2_26 / q2_25 - 1) * 100
        q1_yoy = (q1_26s / q1_25s - 1) * 100
        if q2_yoy >= args.min_yoy and q2_yoy > q1_yoy:
            rows.append({'code': c, 'ann_date': m26[c].get('ann_date') or '',
                         'q2_yoy': round(q2_yoy, 1), 'q1_yoy': round(q1_yoy, 1)})
    print(f"[L1] 单季Q2同比≥{args.min_yoy}%且加速: {len(rows)}家", file=sys.stderr)

    # L2 强度
    rp250, rp120, d250, d120 = rps_full()
    cands = []
    for r in rows:
        c = r['code']
        if (rp250.get(c) or 0) >= args.rps_min and (rp120.get(c) or 0) >= args.rps_min:
            r.update(rps250=rp250[c], rps120=rp120[c])
            cands.append(r)
    print(f"[L2] RPS双≥{args.rps_min}: {len(cands)}家", file=sys.stderr)

    # 预告日
    fc = latest_map(paged('forecast_vip', {'period': '20260630',
                                           'fields': ['ts_code', 'ann_date', 'type', 'p_change_min', 'p_change_max']}))
    basic = {r['ts_code']: r for r in call('stock_basic', {'list_status': 'L'})}
    db = {r['ts_code']: r for r in call('daily_basic', {'trade_date': REF_DATE})}

    # L3/L4 逐股日线；L1.5 机构只对 L3 过线者计算
    out = []
    for r in cands:
        c = r['code']
        try:
            d = sorted(call('daily', {'ts_code': c, 'start_date': '20250901', 'end_date': REF_DATE}),
                       key=lambda x: x['trade_date'])
        except Exception:
            d = []
        if not isinstance(d, list) or not d:
            continue
        gap_pct, vol_ratio, gstatus, since = gap_metrics(d, r['ann_date'])
        fcr = fc.get(c)
        fc_date = fcr.get('ann_date') if fcr else None
        fc_g = gap_metrics(d, fc_date) if fc_date and fc_date != r['ann_date'] else (None, None, None, None)
        closes = [x['close'] for x in d if x.get('close')]
        stage2 = 'Y' if len(closes) >= 200 and closes[-1] > sum(closes[-50:]) / 50 > sum(closes[-200:]) / 200 else ''

        def ok(pct, vol, st):
            return (pct or -99) >= args.gap_min and (vol or 0) >= args.vol_min and st == '未回补'
        pass3 = ok(gap_pct, vol_ratio, gstatus) or ok(fc_g[0], fc_g[1], fc_g[2])
        row = {**r, 'name': basic.get(c, {}).get('name', ''),
               'industry': basic.get(c, {}).get('industry', ''),
               'mcap_yi': round(db[c]['total_mv'] / 1e4, 1) if c in db and db[c].get('total_mv') else None,
               'ann_date': r['ann_date'], 'fc_date': fc_date, 'fc_type': (fcr or {}).get('type'),
               'gap_pct': gap_pct, 'vol_ratio': vol_ratio, 'gap_status': gstatus,
               'fc_gap_pct': fc_g[0], 'fc_gap_status': fc_g[2],
               'stage2': stage2, 'since_gap': since, 'pass3': 'Y' if pass3 else ''}
        if pass3:
            try:
                hk = call('hk_hold', {'ts_code': c})
                hks = sorted((x for x in hk if isinstance(x, dict) and x.get('ratio') is not None),
                             key=lambda x: x['trade_date']) if isinstance(hk, list) else []
                row['hk_chg'] = round(hks[-1]['ratio'] - hks[-2]['ratio'], 2) if len(hks) >= 2 else None
            except Exception:
                row['hk_chg'] = None
            try:
                tf = paged('top10_floatholders', {'ts_code': c})
                per_q = {}
                for x in tf:
                    per_q.setdefault(x.get('end_date'), []).append(x)
                qs = sorted(q for q in per_q if q)[-2:]
                if len(qs) == 2:
                    def share(q):
                        inst = [x for x in per_q[q]
                                if any(k in (x.get('holder_name') or '').lower() for k in INST_KW)]
                        return sum(x.get('hold_ratio') or 0 for x in inst)
                    row['inst_chg'] = round(share(qs[1]) - share(qs[0]), 2)
                else:
                    row['inst_chg'] = None
            except Exception:
                row['inst_chg'] = None
            try:
                hn = call('stk_holdernumber', {'ts_code': c})
                hns = sorted({x['end_date']: x['holder_num'] for x in hn
                              if isinstance(x, dict) and x.get('holder_num')}.items())
                row['holder_chg'] = round((hns[-1][1] / hns[-2][1] - 1) * 100, 1) if len(hns) >= 2 and hns[-2][1] else None
            except Exception:
                row['holder_chg'] = None
            row['inst_pass'] = 'Y' if (row.get('hk_chg') or 0) > 0 or (row.get('inst_chg') or 0) > 0 \
                or (row.get('holder_chg') or 0) < 0 else ''
        else:
            row.update(hk_chg=None, inst_chg=None, holder_chg=None, inst_pass='')
        out.append(row)

    out.sort(key=lambda r: (r['pass3'] == 'Y', r['q2_yoy']), reverse=True)
    n3 = sum(1 for r in out if r['pass3'])
    out_csv = os.path.join(args.out, f'taobo_q2_{today}.csv')
    with open(out_csv, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    meta = {'date': today, 'min_yoy': args.min_yoy, 'rps_min': args.rps_min, 'gap_min': args.gap_min,
            'vol_min': args.vol_min, 'rps_window': [d250, d120, REF_DATE],
            'n_L1': len(rows), 'n_L2': len(cands), 'n_L3': n3,
            'n_full': sum(1 for r in out if r['pass3'] and r['stage2'] == 'Y' and r['inst_pass'] == 'Y')}
    json.dump(meta, open(os.path.join(args.out, f'taobo_q2_{today}_meta.json'), 'w'), ensure_ascii=False, indent=1)
    print(json.dumps(meta, ensure_ascii=False))
    print(f"\n== L3 断层成立（{n3}家）==")
    for r in out:
        if r['pass3'] != 'Y':
            continue
        print(f"{r['code']} {r['name']} [{r['industry']}] 市值{r['mcap_yi']}亿 Q2同比{r['q2_yoy']}%(Q1 {r['q1_yoy']}%) "
              f"RPS {r['rps250']}/{r['rps120']} 中报跳空{r['gap_pct']}%{r['gap_status']} "
              f"预告{r['fc_date']}{r['fc_type'] or ''}跳空{r['fc_gap_pct']}%{r['fc_gap_status']} "
              f"趋势{r['stage2'] or 'N'} 机构{r['inst_pass'] or '?'}[北向{r['hk_chg']} 十大{r['inst_chg']} 户数{r['holder_chg']}%]")
    print(f"\n已写入 {out_csv}")


if __name__ == '__main__':
    main()
