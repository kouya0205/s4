# =============================================================================
# ミクロ人流エージェント > エージェントの次の経路地点決定処理（任意・手順2で消える場合のみ）
#
# ステップ処理だけでは「ゴール到達→消滅」が先に走る場合に使う。
# デフォルトの経路選択を呼んでから、階段出口付近でワープ予約する。
# =============================================================================

def _as_node(v):
    if v is None:
        return None
    if isinstance(v, (list, tuple)):
        v = v[0]
    return int(v)

if not getattr(self, "_stair_warped_2f_1f", False):
    _env = self.agentset.env
    _links = getattr(_env, "STAIR_WARPS_2F_1F", None)
    if _links:
        _pos_agent = self.getPosition()
        _x = float(_pos_agent[0])
        _y = float(_pos_agent[1])
        _dest = self.getDestination()
        for _info in _links:
            _upper_node = _as_node(_info.get("upper_node"))
            if _dest != _upper_node:
                continue
            if not _info["upper_region"].includes(_x, _y) and not self.inArea(_upper_node):
                continue
            _lo_goal = _as_node(_info.get("lower_stair_goal_node"))
            if _lo_goal is not None:
                self.setDestination(v=_lo_goal, delayed=False)
            self._stair_warp_pending = _info["stair_id"]
            break

# 以下、元々の「次の経路地点決定処理」があれば残す（無ければデフォルトに任せる）
