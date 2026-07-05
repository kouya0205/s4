# =============================================================================
# ミクロ人流地図 > 環境の初期化後の処理
# （タブ内に def initAfter(...) を書かない。以下がそのまま実行される）
# =============================================================================

from stair_warp import build_stair_warp_table

# 2F 階段出口_2F -> 1F 階段入口_1F（ワープ先の次ゴールは 1F の「階段」レイヤー）
self.STAIR_WARPS_2F_1F = build_stair_warp_table(
    self,
    upper_goal_layer="階段出口_2F",
    lower_entrance_layer="階段入口_1F",
    lower_stair_goal_layer="階段",
    default_stair_time=5.0,
)

print("=== [MAP] STAIR_WARPS_2F_1F ===")
for info in self.STAIR_WARPS_2F_1F:
    pg = self.pathgraph
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
print("=== [MAP] STAIR_WARPS_2F_1F END ===")
