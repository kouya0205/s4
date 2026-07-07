# =============================================================================
# ミクロ人流地図 > 環境のエージェントの描画処理
#
# screenColor だけでは地図上の色は変わらないため、ここで _ped_category から
# 色とマーカーを指定して描画する。
# def drawAgents(...) は書かない（タブの内容がそのまま実行される）。
#
# 【貼り付け方】
#   ミクロ人流地図 > 「環境のエージェントの描画処理」> 編集
#   既存コードをこの全文に差し替え（または既存ループ内の色指定だけ差し替え）
# =============================================================================

for _agent in agents:
    _pos = _agent.getPosition()
    _x = float(_pos[0])
    _y = float(_pos[1])
    _r = float(getattr(_agent, "r", 0.25))

    _cat = getattr(_agent, "_ped_category", None)
    if _cat == "elderly":
        _color = "#E67E22"
        _marker = "^"
        _size = 10
    elif _cat == "general":
        _color = "#2980B9"
        _marker = "o"
        _size = 8
    else:
        _color = getattr(_agent, "screenColor", "b")
        _marker = getattr(_agent, "screenMarker", "o")
        _size = 8

    _scr = panel.screen if hasattr(panel, "screen") else panel
    _scr.point(
        _x, _y,
        color=_color,
        marker=_marker,
        size=_size,
        edgecolor="k",
        linewidth=0.5,
        alpha=0.95,
        zorder=5,
    )
