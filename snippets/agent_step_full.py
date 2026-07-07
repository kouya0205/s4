"""エージェントのステップ処理を記述する。SFM or FFM に従った基本的な動作を行った後に呼ばれる。"""

def _as_node(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        v = v[0]
    return int(v)


def _is_upper_stair_dest(_env, _dest):
    _dest = _as_node(_dest)
    if _dest is None:
        return False
    for _info in getattr(_env, "STAIR_WARPS_2F_1F", []) or []:
        if _as_node(_info.get("upper_node")) == _dest:
            return True
    return False


# =============================================================================
# 1. 2F -> 1F ワープ（座標転移のみ。ゴールは次ステップから）
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

            self.setStaying(t=0, p=_pos, stayType="float")
            self._stair_warped_2f_1f = True
            self._stair_1f_ent = _lo_ent
            self._stair_1f_goal = _lo_goal
            self._stair_warp_phase = 1
            self.setDestination(v=_lo_ent, delayed=False)

            print(
                "stair warp 2F->1F:",
                self.agentid,
                _info["stair_id"],
                "pos",
                _pos,
                "ent",
                _lo_ent,
                "goal",
                _lo_goal,
            )
            break


# =============================================================================
# 2. 1F：入口ノード到着後に階段ゴールへ（2段階ルート）
# =============================================================================
if getattr(self, "_stair_warped_2f_1f", False):
    _phase = getattr(self, "_stair_warp_phase", 0)
    _lo_ent = _as_node(getattr(self, "_stair_1f_ent", None))
    _lo_goal = _as_node(getattr(self, "_stair_1f_goal", None))

    if _phase == 1 and _lo_ent is not None and self.inArea(_lo_ent):
        if _lo_goal is not None and _lo_goal != _lo_ent:
            self.setDestination(v=_lo_goal, delayed=False)
            self._stair_warp_phase = 2
            print("stair 1F phase2:", self.agentid, "-> goal", _lo_goal)
        else:
            self._stair_warp_phase = 2


# =============================================================================
# 3. 停止・エラー
# =============================================================================
if self.isStopping():
    _env = self.agentset.env

    if getattr(self, "_stair_warped_2f_1f", False):
        _lo_goal = _as_node(getattr(self, "_stair_1f_goal", None))
        if _lo_goal is not None and self.inArea(_lo_goal):
            self.agentset.remove(self)

    elif _is_upper_stair_dest(_env, self.getDestination()):
        pass

    else:
        self.agentset.remove(self)

elif self.isInErrorState():
    print(self.state.message)
    self.agentset.remove(self)

else:
    pass
