# =============================================================================
# ミクロ人流エージェント > エージェントの生成後の処理
#
# v0 に応じて screenColor を設定（一般＝青、高齢者＝オレンジ）。
# 速度の基準値はシミュレーションパラメータから取得（無ければデフォルト）。
# def initAfter(...) は書かない。
# =============================================================================

_COLOR_GENERAL = "#2980B9"
_COLOR_ELDERLY = "#E67E22"

_env = self.agentset.env
_param = _env.simulator.param

_v0_general = float(getattr(_param, "v0General", 1.2))
_v0_elderly = float(getattr(_param, "v0Elderly", 0.8))

_v0 = float(getattr(self, "v0", _v0_general))

if abs(_v0 - _v0_elderly) < abs(_v0 - _v0_general):
    self.screenColor = _COLOR_ELDERLY
    self._ped_category = "elderly"
else:
    self.screenColor = _COLOR_GENERAL
    self._ped_category = "general"
