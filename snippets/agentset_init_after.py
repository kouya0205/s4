# =============================================================================
# ミクロ人流エージェント > エージェント集合の初期化後の処理（任意）
#
# シミュレーションパラメータを読み込み、env に速度プロファイルを載せる。
# def initAfter(...) は書かない。
# =============================================================================

_param = self.env.simulator.param

elderlyRate = float(getattr(_param, "elderlyRate", 0.3))
v0General = float(getattr(_param, "v0General", 1.2))
v1General = float(getattr(_param, "v1General", 1.5))
v0Elderly = float(getattr(_param, "v0Elderly", 0.8))
v1Elderly = float(getattr(_param, "v1Elderly", 1.0))

self.env.AGENT_SPEED_PROFILES = {
    "general": {"v0": v0General, "v1": v1General, "label": "一般"},
    "elderly": {"v0": v0Elderly, "v1": v1Elderly, "label": "高齢者"},
}
self.env.ELDERLY_RATE = elderlyRate

print("=== [AGENT] param profiles ===")
print("elderlyRate =", elderlyRate)
for _key, _prof in self.env.AGENT_SPEED_PROFILES.items():
    print(_key, _prof["label"], "v0=", _prof["v0"], "v1=", _prof["v1"])
print("=== [AGENT] param profiles END ===")
