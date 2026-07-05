"""
2F -> 1F 階段ワープ用ヘルパー（S-quattro / ミクロ人流）

レイヤー構成:
  - 部屋              … 両階共通（人流の始点・終点など）
  - 階段出口_2F       … 2F 階段ゴール（ここで 1F へワープ）
  - 階段入口_1F       … 1F 合流点（2F から出現）
  - 階段              … 1F 階段ゴール（1F エージェントの行き先）

各ユーザー定義領域に属性 stair_id（例: BR, TR, CL）を付けると確実にペアリングできます。
属性が無い場合は、各レイヤー内の領域を上から下・左から右の順で対応付けます。
"""


def layer_by_name(env, name):
    for layer in env.getAllLayers():
        if layer.getName() == name:
            return layer
    return None


def regions_in_layer(layer):
    if layer is None:
        return []
    out = []
    for u in layer:
        if u.isGroup():
            out.extend(u.getUserDefinedRegions())
        else:
            out.append(u)
    return out


def region_sort_key(env, ureg):
    pg = env.pathgraph
    nodes = nodes_in_region(env, ureg)
    if nodes:
        p = pg.nodes[nodes[0]]["p"]
        return (float(p[1]), float(p[0]))
    poly = ureg.getPolygon()
    if poly is not None and len(poly) > 0:
        xs = [float(pt[0]) for pt in poly]
        ys = [float(pt[1]) for pt in poly]
        return (sum(ys) / len(ys), sum(xs) / len(xs))
    return (0.0, 0.0)


def nodes_in_region(env, ureg):
    pg = env.pathgraph
    found = []
    for v in env.getAllPathPoints():
        p = pg.nodes[v]["p"]
        if ureg.includes(float(p[0]), float(p[1])):
            found.append(v)
    return found


def region_stair_id(ureg, index):
    attrs = ureg.getAttrs()
    sid = attrs.get("stair_id")
    if sid is not None and str(sid).strip() != "":
        return str(sid)
    return "stair_%d" % index


def index_regions_by_stair_id(env, layer):
    regions = regions_in_layer(layer)
    regions = sorted(regions, key=lambda u: region_sort_key(env, u))
    out = {}
    for i, ureg in enumerate(regions):
        sid = region_stair_id(ureg, i)
        if sid in out:
            raise ValueError(
                "duplicate stair_id '%s' in layer '%s'" % (sid, layer.getName())
            )
        nodes = nodes_in_region(env, ureg)
        if len(nodes) == 0:
            print(
                "WARN [stair_warp]: no path point in layer '%s' stair_id=%s"
                % (layer.getName(), sid)
            )
            continue
        if len(nodes) > 1:
            print(
                "WARN [stair_warp]: multiple path points in layer '%s' stair_id=%s -> use %s"
                % (layer.getName(), sid, nodes[0])
            )
        out[sid] = {"region": ureg, "node": nodes[0]}
    return out


def build_stair_warp_table(
    env,
    upper_goal_layer="階段出口_2F",
    lower_entrance_layer="階段入口_1F",
    lower_stair_goal_layer="階段",
    default_stair_time=5.0,
):
    """
    2F 階段ゴール -> 1F 階段入口 のワープ表を構築する。

    返り値: list[dict]
      各要素:
        stair_id, upper_region, upper_node,
        lower_entrance_node, lower_stair_goal_node, t
    """
    upper_layer = layer_by_name(env, upper_goal_layer)
    lower_ent_layer = layer_by_name(env, lower_entrance_layer)
    lower_goal_layer = layer_by_name(env, lower_stair_goal_layer)

    if upper_layer is None:
        raise ValueError("layer not found: %s" % upper_goal_layer)
    if lower_ent_layer is None:
        raise ValueError("layer not found: %s" % lower_entrance_layer)

    upper_map = index_regions_by_stair_id(env, upper_layer)
    lower_ent_map = index_regions_by_stair_id(env, lower_ent_layer)
    lower_goal_map = {}
    if lower_goal_layer is not None:
        lower_goal_map = index_regions_by_stair_id(env, lower_goal_layer)

    links = []
    for sid, up in upper_map.items():
        if sid not in lower_ent_map:
            print(
                "WARN [stair_warp]: no 1F entrance for stair_id=%s (layer %s)"
                % (sid, lower_entrance_layer)
            )
            continue
        lo_ent = lower_ent_map[sid]["node"]
        lo_goal = None
        if sid in lower_goal_map:
            lo_goal = lower_goal_map[sid]["node"]
        elif lower_goal_map:
            print(
                "WARN [stair_warp]: no 1F stair goal for stair_id=%s (layer %s)"
                % (sid, lower_stair_goal_layer)
            )
        links.append(
            {
                "stair_id": sid,
                "upper_region": up["region"],
                "upper_node": up["node"],
                "lower_entrance_node": lo_ent,
                "lower_stair_goal_node": lo_goal,
                "t": float(default_stair_time),
            }
        )
    return links


def try_stair_warp(agent, env, warped_flag_attr="_stair_warped_2f_1f"):
    """
    エージェントが 2F 階段出口_2F 領域に入ったら 1F 階段入口_1F へワープする。

    戻り値: True ならこのステップでワープ処理を実行した
    """
    if getattr(agent, warped_flag_attr, False):
        return False

    links = getattr(env, "STAIR_WARPS_2F_1F", None)
    if not links:
        return False

    x = float(agent.p[0])
    y = float(agent.p[1])

    for info in links:
        if not info["upper_region"].includes(x, y):
            continue

        lo_ent = info["lower_entrance_node"]
        pos = env.sampleInnerPathPoint(lo_ent)
        pos = (float(pos[0]), float(pos[1]))

        agent.setStaying(t=info["t"], p=pos, stayType="fix")

        lo_goal = info.get("lower_stair_goal_node")
        if lo_goal is not None:
            agent.setDestination(v=lo_goal, delayed=True)

        setattr(agent, warped_flag_attr, True)
        print(
            "stair warp 2F->1F:",
            "agent",
            agent.agentid,
            "stair_id",
            info["stair_id"],
            "entrance",
            lo_ent,
            "next_goal",
            lo_goal,
        )
        return True

    return False
