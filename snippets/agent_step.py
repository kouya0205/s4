# =============================================================================
# ミクロ人流エージェント > エージェントのステップ処理
#
# 【重要】既存のステップ処理の「末尾」に以下を追記する。
# 【重要】from import 不要。外部 .py ファイルは不要。
# =============================================================================

# --- 2F -> 1F 階段ワープ ---
if not getattr(self, "_stair_warped_2f_1f", False):
    _env = self.env
    _links = getattr(_env, "STAIR_WARPS_2F_1F", None)
    if _links:
        _x = float(self.p[0])
        _y = float(self.p[1])
        for _info in _links:
            if not _info["upper_region"].includes(_x, _y):
                continue

            _lo_ent = _info["lower_entrance_node"]
            _pos = _env.sampleInnerPathPoint(_lo_ent)
            _pos = (float(_pos[0]), float(_pos[1]))

            # SFM では setStaying(p=...) で座標ワープ
            self.setStaying(t=_info["t"], p=_pos, stayType="fix")

            _lo_goal = _info.get("lower_stair_goal_node")
            if _lo_goal is not None:
                self.setDestination(v=_lo_goal, delayed=True)

            self._stair_warped_2f_1f = True
            print(
                "stair warp 2F->1F:",
                "agent", self.agentid,
                "stair_id", _info["stair_id"],
                "entrance", _lo_ent,
                "next_goal", _lo_goal,
            )
            break
