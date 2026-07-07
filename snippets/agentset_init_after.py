# =============================================================================
# ミクロ人流エージェント > エージェント集合の初期化後の処理（任意）
#
# 速度定数を環境に記録し、ログで確認できるようにする。
# 色分けは snippets/agent_init_after.py で行う。
# def initAfter(...) は書かない。
# =============================================================================

_AGENT_SPEEDS = {
    "general": {"v0": 1.2, "v1": 1.5, "label": "一般"},
    "elderly": {"v0": 0.8, "v1": 1.0, "label": "高齢者"},
}

self.env.AGENT_SPEED_PROFILES = _AGENT_SPEEDS

print("=== [AGENT] speed profiles ===")
for _key, _prof in _AGENT_SPEED_PROFILES.items():
    print(
        _key,
        _prof["label"],
        "v0=", _prof["v0"],
        "v1=", _prof["v1"],
    )
print("=== [AGENT] speed profiles END ===")
