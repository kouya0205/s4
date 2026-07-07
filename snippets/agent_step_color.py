# =============================================================================
# ミクロ人流エージェント > エージェントのステップ処理（末尾に追記）
#
# 毎ステップ色・マーカーを再設定（描画側が screenColor を読む場合の保険）
# =============================================================================

if getattr(self, "_ped_category", "general") == "elderly":
    self.screenColor = "#E67E22"
    self.screenMarker = "^"
    self.screenSize = 10
else:
    self.screenColor = "#2980B9"
    self.screenMarker = "o"
    self.screenSize = 8
