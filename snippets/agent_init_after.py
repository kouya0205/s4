# =============================================================================
# ミクロ人流エージェント > エージェントの初期化処理
#
# elderlyRate で一般／高齢者を確率割当し、v0/v1 と screenColor を設定する。
# generateAgentsAndSetDest は v0 を受け取れないため、ここで速度を設定する。
#
# 【貼り付け先】部品プロパティの「エージェントの初期化処理」→「編集」ボタン
# def initAfter(...) は書かない（タブの内容がそのまま実行される）。
# =============================================================================

import random

_COLOR_GENERAL = "#2980B9"
_COLOR_ELDERLY = "#E67E22"

_env = self.agentset.env
_param = _env.simulator.param

elderlyRate = float(getattr(_param, "elderlyRate", 0.3))
v0General = float(getattr(_param, "v0General", 1.2))
v1General = float(getattr(_param, "v1General", 1.5))
v0Elderly = float(getattr(_param, "v0Elderly", 0.8))
v1Elderly = float(getattr(_param, "v1Elderly", 1.0))

if random.random() < elderlyRate:
    self.v0 = v0Elderly
    self.v1 = v1Elderly
    self.screenColor = _COLOR_ELDERLY
    self._ped_category = "elderly"
else:
    self.v0 = v0General
    self.v1 = v1General
    self.screenColor = _COLOR_GENERAL
    self._ped_category = "general"
