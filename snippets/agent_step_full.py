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
# 1. 2F -> 1F ワープ（最優先）
#    setStaying ではなく setDestination(v, p) で 1F 座標へ付け替える
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
                # p= で 1F 座標を起点に、v= で 1F ゴールへ（ワープ本体）
                self.setDestination(v=_lo_goal, p=_pos, delayed=False)
            else:
                self.setDestination(p=_pos, delayed=False)

            self._stair_warped_2f_1f = True
            self._stair_1f_goal = _lo_goal
            print(
                "stair warp 2F->1F:",
                self.agentid,
                _info["stair_id"],
                "pos",
                _pos,
                "next_goal",
                _lo_goal,
            )
            break


# =============================================================================
# 2. 停止・エラー
# =============================================================================
if self.isStopping():
    _env = self.agentset.env

    if getattr(self, "_stair_warped_2f_1f", False):
        _lo_goal = _as_node(getattr(self, "_stair_1f_goal", None))
        if _lo_goal is not None and self.inArea(_lo_goal):
            self.agentset.remove(self)

    elif _is_upper_stair_dest(_env, self.getDestination()):
        # 2F 階段出口到達直後：ワープ待ちなので削除しない
        pass

    else:
        self.agentset.remove(self)

elif self.isInErrorState():
    print(self.state.message)
    self.agentset.remove(self)

else:
    pass
