# =============================================================================
# ミクロ人流エージェント > エージェントのステップ処理（末尾に追記）
# =============================================================================

def _as_node(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        v = v[0]
    return int(v)

# --- 2F -> 1F 階段ワープ ---
if not getattr(self, "_stair_warped_2f_1f", False):
    _env = self.agentset.env
    _links = getattr(_env, "STAIR_WARPS_2F_1F", None)
    if _links:
        _pos_agent = self.getPosition()
        _x = float(_pos_agent[0])
        _y = float(_pos_agent[1])
        for _info in _links:
            if not _info["upper_region"].includes(_x, _y):
                continue

            _lo_ent = _as_node(_info["lower_entrance_node"])
            _pos = _env.sampleInnerPathPoint(_lo_ent)
            _pos = (float(_pos[0]), float(_pos[1]))

            self.setStaying(t=int(_info["t"]), p=_pos, stayType="fix")

            _lo_goal = _as_node(_info.get("lower_stair_goal_node"))
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
