# =============================================================================
# ミクロ人流エージェント > エージェントの生成後の処理
#
# 【目的】
#   エージェントタイプごとの v0（最適速度）に応じて screenColor を設定し、
#   シミュレーション画面で一般／高齢者を色分け表示する。
#
# 【前提】
#   エージェントタイプタブで v0 を設定しておく（下記 README 参照）。
#   def initAfter(...) は書かない。
# =============================================================================

# --- 速度パラメータ（論文値に合わせて変更） ---
_V0_GENERAL = 1.2   # 一般 [m/s]
_V0_ELDERLY = 0.8   # 高齢者 [m/s]

# --- 表示色（#RRGGBB） ---
_COLOR_GENERAL = "#2980B9"   # 青：一般
_COLOR_ELDERLY = "#E67E22"   # オレンジ：高齢者

_v0 = float(getattr(self, "v0", _V0_GENERAL))

# v0 が高齢者設定に近い場合は高齢者とみなす（±0.05 m/s の誤差を許容）
if abs(_v0 - _V0_ELDERLY) < abs(_v0 - _V0_GENERAL):
    self.screenColor = _COLOR_ELDERLY
    self._ped_category = "elderly"
else:
    self.screenColor = _COLOR_GENERAL
    self._ped_category = "general"
