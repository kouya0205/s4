# =============================================================================
# ミクロ人流エージェント > エージェント集合の人流機能 > proc2
#
# 【重要】generateAgentsAndSetDest() は v0 引数を受け取れない。
# 一般／高齢者の速度差は snippets/agent_init_after.py（生成後の処理）で設定する。
#
# proc2 の innerproc は位置ばらつきのみ担当し、生成行は次の形にする：
#   generateAgentsAndSetDest(_rp, lns_[1:])
# =============================================================================

# --- proc2 先頭 ---
# import random


# --- innerproc 例（部屋内ランダム位置 + 通常生成） ---
def innerproc(pp_, n_, lns_):
    ncnt = 0
    for ng in gen:
        _env = self.env
        _pp = int(pp_)
        _pg = _env.pathgraph
        _p = _pg.nodes[_pp]["p"]
        _x, _y = float(_p[0]), float(_p[1])
        _rp = _pp

        for _lname in ("部屋_2F", "部屋_1F", "部屋"):
            _layer = None
            for _ly in _env.getAllLayers():
                if _ly.getName() == _lname:
                    _layer = _ly
                    break
            if _layer is None:
                continue

            _ureg_hit = None
            for _u in _layer:
                if _u.isGroup():
                    _uregs = _u.getUserDefinedRegions()
                else:
                    _uregs = [_u]
                for _ureg in _uregs:
                    if _ureg.includes(_x, _y):
                        _ureg_hit = _ureg
                        break
                if _ureg_hit is not None:
                    break

            if _ureg_hit is None:
                continue

            _cands = []
            for _v in _env.getAllPathPoints():
                _vn = int(_v)
                _pv = _pg.nodes[_vn]["p"]
                if _ureg_hit.includes(float(_pv[0]), float(_pv[1])):
                    _cands.append(_vn)

            if len(_cands) > 0:
                _rp = random.choice(_cands)
                break

        generateAgentsAndSetDest(_rp, lns_[1:])
        ncnt += 1
        if ncnt < n_:
            yield pause(ng)
        else:
            break
