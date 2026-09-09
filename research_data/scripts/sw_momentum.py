#!/usr/bin/env python3
"""申万一级行业动量与拥挤度速览（预期差初筛C层）。
用法: python3 sw_momentum.py
输出: research_data/screen/sw_momentum_<date>.csv + stdout 排序表
指标: 20/60/120日区间收益、相对沪深300超额、量能比(近20日成交额/前40日)、
      距120日高点距离、最新PE/PB。基准日=数据中最新交易日。
"""
import csv
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ts import call, ROOT

END = '20260908'
START = '20260101'
N20, N60, N120 = 20, 60, 120

# 1. 枚举申万一级：全量单日快照，按名称去Ⅱ/Ⅲ级
snap = call('sw_daily', {'trade_date': END})
l1 = sorted({(r['ts_code'], r['name']) for r in snap
             if r['ts_code'].startswith('801') and 'Ⅱ' not in r['name'] and 'Ⅲ' not in r['name']})
print(f"[枚举] {END} 申万一级候选 {len(l1)} 个", file=sys.stderr)

# 2. 沪深300基准
hs = call('index_daily', {'ts_code': '000300.SH', 'start_date': START, 'end_date': END})
hs_close = {r['trade_date']: r['close'] for r in sorted(hs, key=lambda x: x['trade_date'])}

def ret(series, n):
    """series: 按日期升序的close列表；返回n个交易日区间收益%"""
    if len(series) <= n:
        return None
    return (series[-1] / series[-1 - n] - 1) * 100

hs_dates = sorted(hs_close)
hs_ret = {n: ret([hs_close[d] for d in hs_dates], n) for n in (N20, N60, N120)}

rows = []
for code, name in l1:
    try:
        d = call('sw_daily', {'ts_code': code, 'start_date': START, 'end_date': END})
    except Exception as e:
        print(f"[skip] {code} {name}: {str(e)[:60]}", file=sys.stderr)
        continue
    d.sort(key=lambda r: r['trade_date'])
    closes = [r['close'] for r in d]
    amounts = [r.get('amount') or 0 for r in d]
    last = d[-1]
    if len(closes) < N60 + 5:
        print(f"[skip] {code} {name}: 序列过短 {len(closes)}", file=sys.stderr)
        continue
    r20, r60, r120 = ret(closes, N20), ret(closes, N60), ret(closes, N120)
    a20 = sum(amounts[-N20:]) / N20
    a_prev40 = sum(amounts[-N20 - 40:-N20]) / 40 if len(amounts) >= N60 else None
    amt_ratio = a20 / a_prev40 if a_prev40 else None
    hi120 = max(closes[-N120:]) if len(closes) >= N120 else max(closes)
    off_hi = (closes[-1] / hi120 - 1) * 100
    rows.append({
        'code': code, 'name': name, 'asof': last['trade_date'],
        'r20': round(r20, 1), 'r60': round(r60, 1), 'r120': round(r120, 1),
        'ex20': round(r20 - hs_ret[N20], 1), 'ex60': round(r60 - hs_ret[N60], 1),
        'ex120': round(r120 - hs_ret[N120], 1),
        'amt_ratio': round(amt_ratio, 2) if amt_ratio else None,
        'off_120d_high': round(off_hi, 1),
        'pe': last.get('pe'), 'pb': last.get('pb'),
    })

rows.sort(key=lambda r: r['ex20'], reverse=True)
out_dir = os.path.join(ROOT, 'research_data', 'screen')
os.makedirs(out_dir, exist_ok=True)
out_csv = os.path.join(out_dir, f"sw_momentum_{END}.csv")
with open(out_csv, 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

print(f"沪深300: 20日{hs_ret[N20]:.1f}% 60日{hs_ret[N60]:.1f}% 120日{hs_ret[N120]:.1f}%  (截至{hs_dates[-1]})")
print(f"{'行业':<6}{'20日%':>7}{'60日%':>8}{'120日%':>8}{'超额20':>7}{'超额60':>7}{'超额120':>8}{'量能比':>7}{'距高%':>7}{'PE':>8}{'PB':>6}")
for r in rows:
    print(f"{r['name']:<6}{r['r20']:>7}{r['r60']:>8}{r['r120']:>8}{r['ex20']:>7}{r['ex60']:>7}{r['ex120']:>8}"
          f"{r['amt_ratio']:>7}{r['off_120d_high']:>7}{str(r['pe']):>8}{str(r['pb']):>6}")
print(f"\n已写入 {out_csv}")
