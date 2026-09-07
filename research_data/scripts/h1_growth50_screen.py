#!/usr/bin/env python3
"""中报增速筛选：全市场 2026H1 归母净利润同比 ≥50% 或营业收入同比 ≥50%。

用法: python3 h1_growth50_screen.py [--period 20260630] [--min-yoy 50] [--out DIR]

数据路由: fina_indicator(period) 全市场财务指标（netprofit_yoy/dt_netprofit_yoy/or_yoy），
income(period) 取营收与归母净利绝对值，stock_basic 补名称行业，daily_basic 补最新市值。
输出: research_data/screen/h1_growth50_<date>.csv + meta.json，stdout 打印摘要。
旗子只表示"增速达标、值得进入下一步研究"，不构成买卖结论。
"""
import argparse
import csv
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ts import call, ROOT

PAGE = 3000  # 单次返回上限 6000 内安全分页

Fi_FIELDS = ['ts_code', 'ann_date', 'end_date', 'netprofit_yoy', 'dt_netprofit_yoy', 'or_yoy']
Inc_FIELDS = ['ts_code', 'ann_date', 'end_date', 'revenue', 'n_income_attr_p']


def fetch_paged(tool, base_args):
    """limit+offset 翻页，直到取空。非结构化返回（含校验错误文本）直接报错。"""
    rows = []
    offset = 0
    while True:
        a = dict(base_args, limit=PAGE, offset=offset)
        d = call(tool, a)
        if not isinstance(d, list):
            raise RuntimeError(f"{tool} 返回非列表: {str(d)[:200]}")
        rows += d
        if len(d) < PAGE:
            return rows
        offset += PAGE


def dedupe_latest(rows):
    """同公司同报告期多轮公告，保留 ann_date 最新一行。"""
    best = {}
    for r in rows:
        k = r.get('ts_code')
        if not k:
            continue
        cur = best.get(k)
        if cur is None or (r.get('ann_date') or '') > (cur.get('ann_date') or ''):
            best[k] = r
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--period', default='20260630')
    ap.add_argument('--min-yoy', type=float, default=50.0)
    ap.add_argument('--out', default=os.path.join(ROOT, 'research_data', 'screen'))
    args = ap.parse_args()
    period, min_yoy, out = args.period, args.min_yoy, args.out
    today = datetime.date.today().isoformat()
    os.makedirs(out, exist_ok=True)

    # 1 全市场财务指标（含同比）
    fi = fetch_paged('fina_indicator_vip', {'period': period, 'fields': Fi_FIELDS})
    fi_map = dedupe_latest(fi)
    print(f"[fina_indicator_vip] {period} 原始{len(fi)}行 -> 公司{len(fi_map)}家", file=sys.stderr)

    # 2 营收/归母绝对值
    inc = fetch_paged('income_vip', {'period': period, 'report_type': '1', 'fields': Inc_FIELDS})
    inc_map = dedupe_latest(inc)
    print(f"[income_vip] {period} 原始{len(inc)}行 -> 公司{len(inc_map)}家", file=sys.stderr)

    # 3 主体信息与最新市值
    basic = call('stock_basic', {'list_status': 'L'})
    basic = {r['ts_code']: r for r in basic} if isinstance(basic, list) else {}
    tdate = today.replace('-', '')
    db = call('daily_basic', {'trade_date': tdate})  # 该工具不支持 fields 过滤，取全列
    if not isinstance(db, list) or not db:  # 当日未收盘则回退上一交易日
        db = call('daily_basic', {'trade_date': '20260902'})
        tdate = '20260902'
    db = {r['ts_code']: r for r in db} if isinstance(db, list) else {}
    print(f"[basic] 上市{len(basic)}家 [daily_basic] {tdate} {len(db)}家", file=sys.stderr)

    # 4 筛选：归母净利同比或营收同比 ≥ min_yoy（仅限当前在市公司）
    hits = []
    for code, r in fi_map.items():
        if code not in basic:
            continue  # 已退市/未上市挂牌主体，无投资意义
        np_yoy, dt_yoy, or_yoy = r.get('netprofit_yoy'), r.get('dt_netprofit_yoy'), r.get('or_yoy')
        np_ok = isinstance(np_yoy, (int, float)) and np_yoy >= min_yoy
        rev_ok = isinstance(or_yoy, (int, float)) and or_yoy >= min_yoy
        if not np_ok and not rev_ok:
            continue
        b = basic.get(code, {})
        d = db.get(code, {})
        i = inc_map.get(code, {})
        hits.append({
            'code': code, 'name': b.get('name', ''), 'industry': b.get('industry', ''),
            'list_date': b.get('list_date', ''),
            'close': d.get('close'), 'mcap_yi': round(d['total_mv'] / 1e4, 1) if d.get('total_mv') else None,
            'rev_yoy': or_yoy, 'np_yoy': np_yoy, 'dnp_yoy': dt_yoy,
            'rev_h1_yi': round(i['revenue'] / 1e8, 2) if i.get('revenue') else None,
            'np_h1_yi': round(i['n_income_attr_p'] / 1e8, 2) if i.get('n_income_attr_p') else None,
            'ann_date': r.get('ann_date', ''),
        })
    hits.sort(key=lambda x: (x['np_yoy'] if isinstance(x['np_yoy'], (int, float)) else -1), reverse=True)

    np_ge = lambda h: isinstance(h['np_yoy'], (int, float)) and h['np_yoy'] >= min_yoy
    rev_ge = lambda h: isinstance(h['rev_yoy'], (int, float)) and h['rev_yoy'] >= min_yoy
    n_np = sum(1 for h in hits if np_ge(h))
    n_rev = sum(1 for h in hits if rev_ge(h))
    n_both = sum(1 for h in hits if np_ge(h) and rev_ge(h))
    n_new = sum(1 for h in hits if h['list_date'] > '20250630')
    n_st = sum(1 for h in hits if 'ST' in h['name'].upper())

    csv_path = os.path.join(out, f'h1_growth50_{today}.csv')
    cols = list(hits[0].keys()) if hits else ['code']
    with open(csv_path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(hits)
    meta = {'date': today, 'period': period, 'min_yoy': min_yoy,
            'n_listed': len(basic), 'n_disclosed_fi': len(fi_map), 'n_disclosed_inc': len(inc_map),
            'n_hits': len(hits), 'n_np_ge': n_np, 'n_rev_ge': n_rev, 'n_both': n_both,
            'n_new_listing': n_new, 'n_st': n_st, 'price_date': tdate}
    json.dump(meta, open(os.path.join(out, f'h1_growth50_{today}_meta.json'), 'w'), ensure_ascii=False, indent=1)

    # 5 stdout 摘要
    print(json.dumps(meta, ensure_ascii=False))
    fmt = lambda v: f"{v:.0f}%" if isinstance(v, (int, float)) else "—"
    top_np = [h for h in hits if isinstance(h['np_yoy'], (int, float))][:25]
    print(f"\n== 归母净利润同比 top {len(top_np)} ==")
    for h in top_np:
        print(f"{h['code']} {h['name']} [{h['industry']}] 市值{h['mcap_yi']}亿 "
              f"净利{fmt(h['np_yoy'])}(扣非{fmt(h['dnp_yoy'])}) 收入{fmt(h['rev_yoy'])} H1归母{h['np_h1_yi']}亿")
    only_rev = [h for h in hits if rev_ge(h) and not np_ge(h)]
    only_rev.sort(key=lambda h: h['rev_yoy'], reverse=True)
    print(f"\n== 收入≥{min_yoy:.0f}%但净利未达标，共{len(only_rev)}家，top {min(len(only_rev), 15)} ==")
    for h in only_rev[:15]:
        print(f"{h['code']} {h['name']} [{h['industry']}] 市值{h['mcap_yi']}亿 "
              f"收入{fmt(h['rev_yoy'])} 净利{fmt(h['np_yoy'])} H1归母{h['np_h1_yi']}亿")
    by_ind = {}
    for h in hits:
        by_ind[h['industry'] or '未知'] = by_ind.get(h['industry'] or '未知', 0) + 1
    print(f"\n== 行业分布 top10 ==\n" +
          "\n".join(f"  {k}: {v}" for k, v in sorted(by_ind.items(), key=lambda x: -x[1])[:10]))
    print(f"\n已写入 {csv_path}")


if __name__ == '__main__':
    main()
