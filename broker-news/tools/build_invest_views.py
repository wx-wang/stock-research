#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
投资视图重建: 把通用知识图谱(kb_W34/data.json)转换为"投资主图谱 + 三个视图"。

核心设计(用户方案):
- 主图谱只保留 8 类节点: 上市公司/行业/细分赛道/投资主题/产品技术/产业链环节/催化事件/指标变量
- 公司用"市场+代码"统一身份, 名称/简称/英文名/旧名全部映射到同一身份
- 晋级机制: 上市公司(有代码)必进; 其他实体度>=2 或 与股票相连 才进主图谱; 其余进候选区
- 关系映射为 10 类投资语义
- 输出: 主图谱 JSON + 候选区 JSON + 三个视图 HTML(市场雷达图/公司研究图/观点证据图)

用法: python3 build_invest_views.py <data.json> <输出目录> [公司研究图中心股票]
"""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
DICT = json.loads((TOOLS / "stock_dict.json").read_text(encoding="utf-8"))


def norm(s: str) -> str:
    s = (s or "").replace(" ", "").replace("\u3000", "")
    return "".join(chr(ord(c) - 0xFEE0) if 0xFF01 <= ord(c) <= 0xFF5E else c for c in s).upper()


# ---------- 股票身份映射 ----------
def build_stock_map():
    """node 名称 -> (market, code, canonical_name)"""
    m = {}
    for market in ("A股", "港股通"):
        for s in DICT[market]:
            key = s["norm"]
            m.setdefault(key, (market, s["code"], s["name"]))
    # 附带: 名称含代码的变体, 如 "宁德时代(300750)"
    return m


STOCK_MAP = build_stock_map()

# ---------- 8 类节点分类 ----------
CAT_STOCK = "上市公司"
CAT_INDUSTRY = "行业"
CAT_SECTOR = "细分赛道"
CAT_THEME = "投资主题"
CAT_PRODTECH = "产品/技术"
CAT_CHAIN = "产业链环节"
CAT_EVENT = "催化/事件"
CAT_METRIC = "指标/变量"

TYPE_MAP = [
    # (关键词列表, 类别)
    (["行业", "细分行业", "赛道"], CAT_INDUSTRY),
    (["主题", "板块", "概念"], CAT_THEME),
    (["产品", "技术", "工艺", "材料"], CAT_PRODTECH),
    (["产业链"], CAT_CHAIN),
    (["事件", "政策", "制度", "项目"], CAT_EVENT),
    (["指标", "数据", "变量", "金融概念", "商品", "能源产品", "化工产品", "市场"], CAT_METRIC),
]
NOISE_TYPE = ["人物", "地点", "组织", "券商", "团队", "机构"]

def classify(node_name: str, node_type: str):
    """返回 (类别, 是否主节点候选)。"""
    nt = node_type or ""
    # 股票身份优先
    if norm(node_name) in STOCK_MAP or node_name in STOCK_MAP:
        return CAT_STOCK
    code = re.search(r"[(（]?(\d{5,6})[)）]?", node_name)
    if code and norm(node_name) in STOCK_MAP:
        return CAT_STOCK
    for keys, cat in TYPE_MAP:
        for k in keys:
            if k in nt:
                return cat
    # 组织: 券商/机构不进主图谱
    if any(k in nt for k in ["券商", "团队", "机构", "研究所", "证券"]):
        return None
    if nt in NOISE_TYPE or nt in ("",):
        return None
    # 泛化词
    if node_name in ("公司", "相关", "企业", "客户", "行业", "市场"):
        return None
    return CAT_THEME  # 兜底: 概念/主题


# ---------- 关系映射(10 类) ----------
REL_MAP = [
    (["属于", "归类", "包含", "组成"], "属于行业"),
    (["位于", "环节", "产业链"], "位于产业链"),
    (["受益", "拉动", "需求", "利好", "驱动", "增长", "提价", "涨价"], "受益于"),
    (["供货", "供应", "生产", "提供", "出货", "采购", "配套"], "供应产品"),
    (["竞争", "对标", "替代"], "竞争于"),
    (["催化", "事件", "公告", "发布", "政策", "获批", "中标", "投产"], "受到催化"),
    (["推荐", "关注", "看好", "支持", "布局", "涉及", "相关", "合作"], "支持观点"),
    (["风险", "警告", "下跌", "利空", "质疑", "反驳", "谨慎"], "反驳观点"),
    (["目标价", "估值", "评级", "定价", "市值", "市盈率", "预测"], "被市场定价"),
]

def map_rel(rel_type: str) -> str:
    for keys, cat in REL_MAP:
        for k in keys:
            if k in (rel_type or ""):
                return cat
    return "相关"


# ---------- 主流程 ----------
def main() -> int:
    data_path = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    center_company = sys.argv[3] if len(sys.argv) > 3 else "中际旭创"
    out_dir.mkdir(parents=True, exist_ok=True)

    d = json.loads(data_path.read_text(encoding="utf-8"))
    nodes, edges = d["nodes"], d["edges"]

    # 1. 分类 + 身份
    node_cat = {}
    node_stock = {}
    for n in nodes:
        name = n["name"]
        cat = classify(name, n.get("type", ""))
        if cat:
            node_cat[name] = cat
        key = norm(name)
        if key in STOCK_MAP:
            mkt, code, cname = STOCK_MAP[key]
            node_stock[name] = f"{mkt}:{code}"

    # 2. 度统计 + 与股票的连接
    deg = Counter()
    stock_link = Counter()
    edge_map = defaultdict(list)
    for e in edges:
        s, t = e["source"], e["target"]
        if s in node_cat and t in node_cat:
            deg[s] += 1
            deg[t] += 1
            edge_map[(s, t)].append(e)
            for x in (s, t):
                if node_cat[x] == CAT_STOCK:
                    stock_link[s if x == t else t] += 1

    # 3. 晋级规则
    main_nodes, candidates = [], []
    for name, cat in node_cat.items():
        if cat == CAT_STOCK:
            main_nodes.append((name, cat))
        elif deg[name] >= 2 or stock_link[name] >= 1:
            main_nodes.append((name, cat))
        else:
            candidates.append((name, cat, deg[name]))
    main_names = {n for n, _ in main_nodes}

    # 4. 主图谱关系(两端都是主节点, 映射为 10 类)
    main_edges = []
    for (s, t), es in edge_map.items():
        if s not in main_names or t not in main_names:
            continue
        e = es[0]
        main_edges.append({
            "source": s, "target": t,
            "type": map_rel(e.get("type", "")),
            "description": (e.get("description") or "")[:120],
        })

    # 5. 输出
    (out_dir / "data.json").write_text(json.dumps(
        {"nodes": [{"name": n, "type": c, "identity": node_stock.get(n)} for n, c in main_nodes],
         "edges": main_edges}, ensure_ascii=False), encoding="utf-8")
    (out_dir / "candidates.json").write_text(json.dumps(
        [{"name": n, "category": c, "degree": deg[n]} for n, c, _ in candidates], ensure_ascii=False),
        encoding="utf-8")

    print(f"主图谱: {len(main_nodes)} 节点 / {len(main_edges)} 关系")
    print(f"候选区: {len(candidates)} 实体")
    cc = Counter(c for _, c in main_nodes)
    print("主图谱类别分布:", dict(cc))
    print(f"股票节点: {sum(1 for _, c in main_nodes if c == CAT_STOCK)}")
    print(f"关系类型分布:", dict(Counter(e['type'] for e in main_edges)))

    # 6. 三个视图 HTML
    build_views(main_nodes, main_edges, node_stock, out_dir, center_company)
    print(f"视图输出到: {out_dir}")
    return 0


def _vis_html(title, nodes, edges, out_file, node_color, legend):
    js_nodes = json.dumps([{"id": n, "label": n, "color": {"background": node_color(n), "border": "#333"},
                            "value": min(v, 60), "font": {"size": 13}, "shape": "box"}
                           for n, v in nodes], ensure_ascii=False)
    js_edges = json.dumps([{"from": s, "to": t, "label": ty, "arrows": "to",
                            "font": {"size": 10, "align": "middle"}, "smooth": {"type": "continuous"}}
                           for s, t, ty in edges], ensure_ascii=False)
    lg = "".join(f'<span class="lg"><span class="dot" style="background:{c}"></span>{k}</span>' for k, c in legend.items())
    html = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8"><title>{title}</title>
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>body{{font-family:-apple-system,'PingFang SC',sans-serif;margin:0;background:#f7f8fa}}
#header{{padding:12px 20px;background:#fff;border-bottom:1px solid #e3e6ea}}
#header h1{{margin:0;font-size:16px}} #header p{{margin:4px 0 0;color:#666;font-size:12px}}
.lg{{display:inline-block;margin-right:10px;font-size:12px;margin-top:6px}}
.dot{{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:4px;vertical-align:-1px}}
#net{{width:100%;height:calc(100vh - 130px)}}</style></head><body>
<div id="header"><h1>{title}</h1><p>{len(nodes)} 节点 · {len(edges)} 关系 · 拖拽/缩放</p><div>{lg}</div></div>
<div id="net"></div><script>
const nodes = new vis.DataSet({js_nodes});
const edges = new vis.DataSet({js_edges});
const data = {{nodes, edges}};
const options = {{ physics: {{ barnesHut: {{ gravitationalConstant: -5000, centralGravity: 0.06 }}, stabilization: {{ iterations: 250 }} }},
  interaction: {{ hover: true }}, edges: {{ color: {{ color: '#a0a6ad', highlight: '#e15759' }}, smooth: {{ type: 'continuous' }} }},
  nodes: {{ shape: 'box', shadow: true }} }};
new vis.Network(document.getElementById('net'), data, options);
</script></body></html>"""
    out_file.write_text(html, encoding="utf-8")


def build_views(main_nodes, main_edges, node_stock, out_dir, center_company):
    cat = {n: c for n, c in main_nodes}
    deg = Counter()
    for e in main_edges:
        deg[e["source"]] += 1
        deg[e["target"]] += 1

    C = {"上市公司": "#e15759", "行业": "#59a14f", "细分赛道": "#76b7b2", "投资主题": "#edc948",
         "产品/技术": "#4e79a7", "产业链环节": "#b07aa1", "催化/事件": "#ff9da7", "指标/变量": "#9c755f"}
    color = lambda n: C.get(cat.get(n, "投资主题"), "#9c755f")

    # 视图1: 市场雷达图 —— 行业/主题/催化 + 受益公司(度 Top 60)
    keep1 = [n for n in main_names_of(main_nodes) if cat[n] in ("行业", "投资主题", "催化/事件", "上市公司")]
    keep1 = sorted(keep1, key=lambda n: -deg[n])[:60]
    k1 = set(keep1)
    edges1 = [(e["source"], e["target"], e["type"]) for e in main_edges
              if e["source"] in k1 and e["target"] in k1 and e["type"] in ("受益于", "供应产品", "受到催化", "属于行业", "支持观点")]
    _vis_html("市场雷达图 · 行业/主题→受益公司→催化", [(n, deg[n]) for n in keep1], edges1, out_dir / "view1_市场雷达图.html", color, C)

    # 视图2: 公司研究图 —— 中心公司 2 跳 ego 网络
    center = center_company if center_company in cat else next((n for n, c in main_nodes if c == "上市公司"), None)
    if center:
        hops = {center}
        for e in main_edges:
            if e["source"] == center: hops.add(e["target"])
            if e["target"] == center: hops.add(e["source"])
        hops2 = set(hops)
        for e in main_edges:
            if e["source"] in hops and e["target"] in main_names_of(main_nodes):
                hops2.add(e["target"])
            if e["target"] in hops and e["source"] in main_names_of(main_nodes):
                hops2.add(e["source"])
        if len(hops2) > 120:
            hops2 = sorted(hops2, key=lambda n: -deg[n])[:120]
        edges2 = [(e["source"], e["target"], e["type"]) for e in main_edges if e["source"] in hops2 and e["target"] in hops2]
        _vis_html(f"公司研究图 · {center}", [(n, deg[n]) for n in hops2], edges2, out_dir / "view2_公司研究图.html", color, C)

    # 视图3: 观点证据图 —— 受益/支持/反驳/催化 类关系
    keep3 = [n for n in main_names_of(main_nodes) if cat[n] in ("投资主题", "上市公司", "催化/事件")]
    k3 = set(keep3)
    edges3 = [(e["source"], e["target"], f"{e['type']}|{(e.get('description') or '')[:24]}") for e in main_edges
              if e["source"] in k3 and e["target"] in k3 and e["type"] in ("受益于", "受到催化", "支持观点", "反驳观点", "被市场定价")]
    _vis_html("观点证据图 · 主题/公司×催化×市场定价", [(n, deg[n]) for n in k3 if n in dict(deg)], edges3, out_dir / "view3_观点证据图.html", color, C)


def main_names_of(main_nodes):
    return [n for n, _ in main_nodes]


if __name__ == "__main__":
    sys.exit(main())