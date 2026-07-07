# =============================================================================
# ミクロ人流エージェント > エージェント集合の人流機能 > proc2
#
# 【変更するのは2か所だけ】
#   1. proc2 の先頭に import random を1行追加
#   2. proc2 内の innerproc 関数を丸ごと差し替え
#
# 【触らないもの】
#   - generateAgentsCaller 本体
#   - proc0 / proc1 / proc2 の innerproc 以外
#   - generateAgentsAndSetDest に座標 (x,y) を渡す処理
# =============================================================================

# --- proc2 の先頭（yield alwaysTrue() の直前か直後）に追加 ---
# import random


# --- proc2 内の innerproc を以下に差し替え ---
# ※ S4 では proc2 の中身なので、def innerproc の行は先頭4スペースから始める
# ※ innerproc の中身は先頭8スペース

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
