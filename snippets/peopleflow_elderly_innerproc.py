# =============================================================================
# ミクロ人流エージェント > エージェント集合の人流機能 > proc2
#
# elderlyRate をパラメータから取得し、生成ごとに一般／高齢者を確率的に割り当てる。
# proc2 の先頭に import random を追加し、innerproc を以下に差し替える。
# =============================================================================

# --- proc2 先頭に追加 ---
# import random


# --- proc2 内 innerproc（先頭4スペースから） ---
def innerproc(pp_, n_, lns_):
    ncnt = 0
    _param = self.env.simulator.param
    elderlyRate = float(getattr(_param, "elderlyRate", 0.3))
    v0General = float(getattr(_param, "v0General", 1.2))
    v1General = float(getattr(_param, "v1General", 1.5))
    v0Elderly = float(getattr(_param, "v0Elderly", 0.8))
    v1Elderly = float(getattr(_param, "v1Elderly", 1.0))

    for ng in gen:
        if random.random() < elderlyRate:
            _v0, _v1 = v0Elderly, v1Elderly
        else:
            _v0, _v1 = v0General, v1General

        generateAgentsAndSetDest(int(pp_), lns_[1:], v0=_v0, v1=_v1)
        ncnt += 1
        if ncnt < n_:
            yield pause(ng)
        else:
            break
