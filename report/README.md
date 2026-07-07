# ゼミ共同研究報告書（LaTeX）

S-quattro 階段ワープ実装の進捗をまとめた報告書です。

## コンパイル方法

LuaLaTeX + ltjsarticle が必要です（TeX Live 等）。

```bash
cd report
lualatex main.tex
lualatex main.tex   # 相互参照のため2回
```

## 画像の配置

`figures/` に SFMMap のスクリーンショットを置いてください。
詳細は `figures/README.md` を参照。

| ファイル | 内容 |
|----------|------|
| `figures/sfmmap_overview.png` | 地図全体 |
| `figures/sfmmap_2f.png` | 2階 |
| `figures/sfmmap_1f.png` | 1階 |
| `figures/sfmmap_layers.png` | レイヤー構成 |
| `figures/simulation_log.png` | シミュレーション画面（任意） |

画像が無くてもプレースホルダ枠付きでコンパイルできます。

## 編集のヒント

- 著者名・日付：`main.tex` の `\author`，`\date`
- 研究室名・モデル名：本文中の該当箇所を修正
