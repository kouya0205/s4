# =============================================================================
# ミクロ人流地図 > 環境の初期化後の処理
#
# 【重要】def initAfter(...) は書かない。以下がそのまま実行される。
# 【重要】from import 不要。外部 .py ファイルは不要。
# =============================================================================

# --- レイヤー名（確定構成） ---
_LAYER_UPPER_GOAL = "階段出口_2F"      # 2F 階段ゴール → ここで 1F へワープ
_LAYER_LOWER_ENTRANCE = "階段入口_1F"  # 1F 合流点（2F から出現）
_LAYER_LOWER_STAIR_GOAL = "階段"       # 1F 階段ゴール（ワープ後の次の目的地）
_DEFAULT_STAIR_TIME = 5.0              # 階段降り時間 [秒]


def _regions_in_layer(layer):
    if layer is None:
        return []
    out = []
    for u in layer:
        if u.isGroup():
            out.extend(u.getUserDefinedRegions())
        else:
            out.append(u)
    return out


def _layer_by_name(env, name):
    for ly in env.getAllLayers():
        if ly.getName() == name:
            return ly
    return None


def _nodes_in_region(env, ureg):
    pg = env.pathgraph
    found = []
    for v in env.getAllPathPoints():
        p = pg.nodes[v]["p"]
        if ureg.includes(float(p[0]), float(p[1])):
            found.append(v)
    return found


def _region_sort_key(env, ureg):
    pg = env.pathgraph
    nodes = _nodes_in_region(env, ureg)
    if nodes:
        p = pg.nodes[nodes[0]]["p"]
        return (float(p[1]), float(p[0]))
    poly = ureg.getPolygon()
    if poly is not None and len(poly) > 0:
        xs = [float(pt[0]) for pt in poly]
        ys = [float(pt[1]) for pt in poly]
        return (sum(ys) / len(ys), sum(xs) / len(xs))
    return (0.0, 0.0)


def _region_stair_id(ureg, index):
    attrs = ureg.getAttrs()
    sid = attrs.get("stair_id")
    if sid is not None and str(sid).strip() != "":
        return str(sid)
    return "stair_%d" % index


def _index_regions_by_stair_id(env, layer):
    regions = _regions_in_layer(layer)
    regions = sorted(regions, key=lambda u: _region_sort_key(env, u))
    out = {}
    for i, ureg in enumerate(regions):
        sid = _region_stair_id(ureg, i)
        nodes = _nodes_in_region(env, ureg)
        if len(nodes) == 0:
            print(
                "WARN [stair_warp]: no path point in layer '%s' stair_id=%s"
                % (layer.getName(), sid)
            )
            continue
        if len(nodes) > 1:
            print(
                "WARN [stair_warp]: multiple points in '%s' stair_id=%s -> use %s"
                % (layer.getName(), sid, nodes[0])
            )
        out[sid] = {"region": ureg, "node": nodes[0]}
    return out


# --- ワープ表の構築 ---
_upper_layer = _layer_by_name(self, _LAYER_UPPER_GOAL)
_lower_ent_layer = _layer_by_name(self, _LAYER_LOWER_ENTRANCE)
_lower_goal_layer = _layer_by_name(self, _LAYER_LOWER_STAIR_GOAL)

if _upper_layer is None:
    print("ERROR [stair_warp]: layer not found:", _LAYER_UPPER_GOAL)
if _lower_ent_layer is None:
    print("ERROR [stair_warp]: layer not found:", _LAYER_LOWER_ENTRANCE)

_upper_map = _index_regions_by_stair_id(self, _upper_layer) if _upper_layer else {}
_lower_ent_map = _index_regions_by_stair_id(self, _lower_ent_layer) if _lower_ent_layer else {}
_lower_goal_map = (
    _index_regions_by_stair_id(self, _lower_goal_layer) if _lower_goal_layer else {}
)

self.STAIR_WARPS_2F_1F = []
for sid, up in _upper_map.items():
    if sid not in _lower_ent_map:
        print(
            "WARN [stair_warp]: no 1F entrance for stair_id=%s" % sid
        )
        continue
    lo_ent = _lower_ent_map[sid]["node"]
    lo_goal = None
    if sid in _lower_goal_map:
        lo_goal = _lower_goal_map[sid]["node"]
    elif _lower_goal_map:
        print(
            "WARN [stair_warp]: no 1F stair goal for stair_id=%s" % sid
        )
    self.STAIR_WARPS_2F_1F.append(
        {
            "stair_id": sid,
            "upper_region": up["region"],
            "upper_node": up["node"],
            "lower_entrance_node": lo_ent,
            "lower_stair_goal_node": lo_goal,
            "t": float(_DEFAULT_STAIR_TIME),
        }
    )

# --- 確認ログ ---
print("=== [MAP] STAIR_WARPS_2F_1F ===")
pg = self.pathgraph
for info in self.STAIR_WARPS_2F_1F:
    up = info["upper_node"]
    ent = info["lower_entrance_node"]
    goal = info.get("lower_stair_goal_node")
    up_p = tuple(pg.nodes[up]["p"])
    ent_p = tuple(pg.nodes[ent]["p"])
    goal_p = tuple(pg.nodes[goal]["p"]) if goal is not None else None
    print(
        info["stair_id"],
        "up", up, up_p,
        "entrance", ent, ent_p,
        "1F_goal", goal, goal_p,
    )
print("=== [MAP] STAIR_WARPS_2F_1F END (count=%d) ===" % len(self.STAIR_WARPS_2F_1F))
