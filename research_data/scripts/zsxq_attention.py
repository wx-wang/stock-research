#!/usr/bin/env python3
"""知识星球行业关注度扫描（预期差初筛B层）。
对指定星球按行业关键词全文检索，统计近7天/30天主题数与总命中数。
输出: research_data/screen/zsxq_attention_<date>.json + stdout 表
注意：搜索接口可能只返回部分结果，此为关注度代理指标，非精确计数。
"""
import datetime
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TODAY = datetime.date.today()

GROUPS = {
    '15525241828412': '观察者03',
    '48885244111858': '每日投研',
}

# 行业/主题关键词（多个同义词合并为一个主题桶）
THEMES = {
    '存储芯片': ['存储', 'DRAM', 'NAND', '内存'],
    '光伏': ['光伏'],
    '锂电': ['锂电', '碳酸锂', '固态电池'],
    '风电': ['风电'],
    'AI算力/光模块': ['光模块', '算力', 'AIDC', '液冷'],
    '农业养殖': ['猪价', '生猪', '白羽鸡', '养殖', '种业', '转基因'],
    '创新药': ['创新药', 'BD'],
    'CXO': ['CXO', '药明'],
    '黄金贵金属': ['黄金', '金价', '贵金属'],
    '航运油运': ['油运', '集运', '运价', 'VLCC'],
    '氟化工制冷剂': ['制冷剂', '氟化工'],
    '电网特高压': ['电网', '特高压'],
    '军工': ['军工', '国防'],
    '工程机械': ['工程机械', '挖掘机'],
    '白酒食品': ['白酒', '茅台'],
    '电力核电': ['核电', '用电量', '电价'],
    '房地产': ['地产', '房地产'],
    '有色铜铝稀土': ['铜价', '电解铝', '稀土', '锡'],
    '煤炭钢铁': ['煤价', '动力煤', '钢铁', '钢价'],
    '存储之外半导体': ['半导体', '晶圆', '中芯'],
    '机器人': ['机器人', '人形机器人', '宇树'],
    '消费电子': ['AI眼镜', '折叠屏', '果链'],
    '信创计算机': ['信创', '华为链', '鸿蒙'],
    '出海/跨境': ['出海', '跨境', '关税'],
}

def search(gid, kw):
    cmd = ['zsxq-cli', 'topic', '+search', '--group-id', gid, '--query', kw, '--json']
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if out.returncode != 0:
            return None, out.stderr[:100]
        txt = out.stdout.strip()
        dec = json.JSONDecoder()
        return dec.raw_decode(txt[txt.index('{'):])[0], None
    except Exception as e:
        return None, str(e)[:100]

result = {}
for gid, gname in GROUPS.items():
    gres = {}
    for theme, kws in THEMES.items():
        dates, total = [], 0
        for kw in kws:
            data, err = search(gid, kw)
            if data is None:
                print(f"[warn] {gname} {kw}: {err}", file=sys.stderr)
                continue
            topics = data if isinstance(data, list) else (data.get('topics_brief') or data.get('topics') or [])
            if isinstance(topics, dict):
                topics = topics.get('topics') or []
            for t in topics:
                ct = (t.get('create_time') or '')[:10]
                if ct:
                    dates.append(ct)
            total += len(topics)
        d7 = sum(1 for d in dates if d >= str(TODAY - datetime.timedelta(days=7)))
        d30 = sum(1 for d in dates if d >= str(TODAY - datetime.timedelta(days=30)))
        gres[theme] = {'hits_total': total, 'last7d': d7, 'last30d': d30,
                       'latest': max(dates) if dates else ''}
        print(f"[done] {gname} {theme}: 总{total} 7天{d7} 30天{d30} 最新{gres[theme]['latest']}", file=sys.stderr)
    result[gname] = gres

out = os.path.join(ROOT, 'research_data', 'screen', f'zsxq_attention_{TODAY.strftime("%Y%m%d")}.json')
json.dump(result, open(out, 'w'), ensure_ascii=False, indent=1)

print(f"\n{'主题':<12}{'观察者03(7天/30天/总)':>22}{'每日投研(7天/30天/总)':>22}")
for theme in THEMES:
    a = result['观察者03'][theme]
    b = result['每日投研'][theme]
    print(f"{theme:<12}{a['last7d']:>8}/{a['last30d']:>3}/{a['hits_total']:<6}{b['last7d']:>10}/{b['last30d']:>3}/{b['hits_total']:<6}")
print(f"\n已写入 {out}")
