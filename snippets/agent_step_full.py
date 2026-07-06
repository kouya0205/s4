"""エージェントのステップ処理を記述する。SFM or FFM に従った基本的な動作を行った後に呼ばれる。"""

def _as_node(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        v = v[0]
    return int(v)


# =============================================================================
# 1. 階段ワープ（必ず isStopping 判定より先）
# =============================================================================
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

            if _lo_goal is not None:
                self.setDestination(v=_lo_goal, delayed=False)

            self.setStaying(t=int(_info["t"]), p=_pos, stayType="fix")
            self._stair_warped_2f_1f = True
            print(
                "stair warp 2F->1F:",
                self.agentid,
                _info["stair_id"],
                "next_goal",
                _lo_goal,
            )
            break


# =============================================================================
# 2. 停止・エラー時の処理（デフォルトを修正）
# =============================================================================
if self.isStopping():
    if getattr(self, "_stair_warped_2f_1f", False):
        # ワープ済み：1F「階段」ゴールに着くまで削除しない
        _env = self.agentset.env
        _dest = _as_node(self.getDestination())
        _remove = False
        for _info in getattr(_env, "STAIR_WARPS_2F_1F", []) or []:
            _goal = _as_node(_info.get("lower_stair_goal_node"))
            if _goal is not None and _dest == _goal and self.inArea(_goal):
                _remove = True
                break
        if _remove:
            self.agentset.remove(self)
    else:
        # 1F 直行など、ワープなしの通常終了
        self.agentset.remove(self)

elif self.isInErrorState():
    print(self.state.message)
    self.agentset.remove(self)

else:
    pass
