# =============================================================================
# ミクロ人流エージェント > エージェントのステップ処理
#
# 【重要】既存コードの「先頭」に置く（末尾だとゴール到達後に消える場合がある）
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
            _upper_node = _as_node(_info.get("upper_node"))
            _in_upper = _info["upper_region"].includes(_x, _y)
            if _upper_node is not None:
                _in_upper = _in_upper or self.inArea(_upper_node)
            if not _in_upper:
                continue

            _lo_ent = _as_node(_info["lower_entrance_node"])
            _lo_goal = _as_node(_info.get("lower_stair_goal_node"))
            _pos = _env.sampleInnerPathPoint(_lo_ent)
            _pos = (float(_pos[0]), float(_pos[1]))

            # 【重要】階段出口_2F 到達＝人流完了で消えるのを防ぐため、
            # setStaying より先に delayed=False で次の目的地を即時セットする
            if _lo_goal is not None:
                self.setDestination(v=_lo_goal, delayed=False)

            self.setStaying(t=int(_info["t"]), p=_pos, stayType="fix")

            self._stair_warped_2f_1f = True
            print(
                "stair warp 2F->1F:",
                "agent", self.agentid,
                "stair_id", _info["stair_id"],
                "entrance", _lo_ent,
                "next_goal", _lo_goal,
            )
            break
