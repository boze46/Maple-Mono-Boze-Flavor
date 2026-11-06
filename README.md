# Maple Mono Boze Flavor

[Maple Mono](https://github.com/subframe7536/maple-font) v7 的个人定制构建。一套配置产出四套字体：宽度（NR / SL）× 提示（hinted / unhinted）。仓库只存放配置与 CI workflow，字体在 GitHub Actions 构建并发布到 [Releases](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases)。

## 产出

下载表格与 Release notes 中的同款，此处使用 `latest/download` 固定直链——zip 文件名在各次 Release 之间保持不变（nix 用 `fetchurl` 拉取，升级 = 改一次 hash）。

≤1080p 用 hinted 列，≥2K 用 unhinted 列；Variable / OTF / WOFF2 本身不含 hint，任选。NF / NF-CN 的 Nerd Font 图标全部单宽（mono）。hinted 与 unhinted 字体族名相同，同一台机器不要安装同宽度的两套。

### NR（narrow：拉丁 550 / 中文 1100）

| 格式 | hinted（≤1080p） | unhinted（≥2K） |
| :--- | :---: | :---: |
| Variable | — | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorNR-Variable.zip) |
| TTF | [📦 TTF-AutoHint](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorNR-TTF-AutoHint.zip) | [📦 TTF](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorNR-TTF.zip) |
| OTF | — | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorNR-OTF.zip) |
| WOFF2 | — | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorNR-Woff2.zip) |
| NF | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorNR-NF.zip) | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorNR-NF-unhinted.zip) |
| NF-CN | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorNR-NF-CN.zip) | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorNR-NF-CN-unhinted.zip) |

### SL（slim：拉丁 500 / 中文 1000，与 Sarasa Term SC 相同的 2:1 字距）

| 格式 | hinted（≤1080p） | unhinted（≥2K） |
| :--- | :---: | :---: |
| Variable | — | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorSL-Variable.zip) |
| TTF | [📦 TTF-AutoHint](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorSL-TTF-AutoHint.zip) | [📦 TTF](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorSL-TTF.zip) |
| OTF | — | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorSL-OTF.zip) |
| WOFF2 | — | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorSL-Woff2.zip) |
| NF | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorSL-NF.zip) | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorSL-NF-unhinted.zip) |
| NF-CN | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorSL-NF-CN.zip) | [📦 下载](https://github.com/boze46/Maple-Mono-Boze-Flavor/releases/latest/download/MapleMonoBozeFlavorSL-NF-CN-unhinted.zip) |

## 基础信息

- 字体族名：`Maple Mono Boze Flavor NR NFMono` / `Maple Mono Boze Flavor NR NFMono CN`（SL 同理替换后缀）
- 上游：subframe7536/maple-font v7 线，当前 v7.9（commit `5ee93150fbafe59dc805c2f64ad879fd14c3ce78`），workflow 可指定 ref
- 连字开启；未使用 `--normal` 预设
- 原始 playground 导出记录见 [font.md](./font.md)，构建实际读取 [config.json](./config.json)

## Flavor 内容

相对上游默认配置的关键改动：

- `nerd_font.mono: true` — Nerd Font 图标全部单宽，终端图标对齐（与 Sarasa Term SC Nerd 行为一致）
- `cn.narrow: false` — 保持中英 2:1 与等宽字体标志（开启会破坏 2:1 与等宽识别，slim 下还是上游 v7.9 的 no-op 分支）
- `width` 由 CI 按 matrix 注入 `narrow`（550/1100）或 `slim`（500/1000，Sarasa 同款字距）
- 冻结启用（`feature_freeze` 置 `enable`）：`cv01 cv02 cv03 cv07 cv10 cv33 cv34 cv35 cv36 cv40 cv43 cv61 cv62 cv66 ss03 ss04 ss05 ss06 ss07 ss08`

<details>
<summary>完整 config.json</summary>

```json
{
  "$schema": "./source/schema.json",
  "family_name": "Maple Mono Boze Flavor",
  "use_hinted": true,
  "pool_size": 4,
  "enable_ligature": true,
  "ttfautohint_param": {},
  "github_mirror": "github.com",
  "infinite_arrow": null,
  "remove_tag_liga": false,
  "weight_mapping": {
    "thin": 100,
    "extralight": 200,
    "light": 300,
    "regular": 400,
    "medium": 500,
    "semibold": 600,
    "bold": 700,
    "extrabold": 800
  },
  "line_height": 1,
  "width": "narrow",
  "feature_freeze": {
    "cv01": "enable",
    "cv02": "enable",
    "cv03": "enable",
    "cv04": "ignore",
    "cv05": "ignore",
    "cv06": "ignore",
    "cv07": "enable",
    "cv08": "ignore",
    "cv09": "ignore",
    "cv10": "enable",
    "cv11": "ignore",
    "cv31": "ignore",
    "cv32": "ignore",
    "cv33": "enable",
    "cv34": "enable",
    "cv35": "enable",
    "cv36": "enable",
    "cv37": "ignore",
    "cv38": "ignore",
    "cv39": "ignore",
    "cv40": "enable",
    "cv41": "ignore",
    "cv42": "ignore",
    "cv43": "enable",
    "cv44": "ignore",
    "cv61": "enable",
    "cv62": "enable",
    "cv63": "ignore",
    "cv64": "ignore",
    "cv65": "ignore",
    "cv66": "enable",
    "cv96": "ignore",
    "cv97": "ignore",
    "cv98": "ignore",
    "cv99": "ignore",
    "ss01": "ignore",
    "ss02": "ignore",
    "ss03": "enable",
    "ss04": "enable",
    "ss05": "enable",
    "ss06": "enable",
    "ss07": "enable",
    "ss08": "enable",
    "ss09": "ignore",
    "ss10": "ignore",
    "ss11": "ignore",
    "zero": "ignore"
  },
  "nerd_font": {
    "enable": true,
    "version": "3.4.0",
    "mono": true,
    "propo": false,
    "use_font_patcher": false,
    "glyphs": [
      "--complete"
    ],
    "extra_args": []
  },
  "cn": {
    "enable": true,
    "with_nerd_font": true,
    "fix_meta_table": true,
    "clean_cache": false,
    "narrow": false,
    "use_hinted": true,
    "use_static_base_font": true,
    "scale_factor": 1.0
  }
}
```

</details>

## 项目原理

- 仓库不含字体源码与产物，只有 `config.json` 和 [.github/workflows/build.yml](./.github/workflows/build.yml)。
- Actions 手动触发后：checkout 上游 → 用本仓库 `config.json` 覆盖上游的 → matrix 并行构建 `narrow` / `slim` 两个宽度；每个宽度先全量构建 hinted 版（1080p），再把 `use_hinted` / `cn.use_hinted` 切为 `false`，用 `--archive --cache` 复用基字、只重打 NF / NF-CN 的 `-unhinted` 变体（2K）。最小格式（Variable / TTF / TTF-AutoHint / OTF / WOFF2）与 hint 预设无关，每个宽度各出一份。
- 改配置：编辑 `config.json`（playground 导出后需同步；注意 v8 线导出为 `cjk` 结构，与 v7 不兼容）→ 提交 → 重跑 workflow；上游升级同理，改 `upstream_ref`。
- 本地构建：clone 上游 v7 分支，覆盖 `config.json`，`pip install -r requirements.txt && python build.py --archive`。

## 上游鸣谢 / License

- [Maple Mono](https://github.com/subframe7536/maple-font)（@subframe7536）— 字体本体与构建脚本
- [Nerd Fonts](https://github.com/ryanoasis/nerd-fonts) — 图标字形
- [Source Han Sans](https://github.com/adobe-fonts/source-han-sans) 系 — CN 版中文字形（经 Maple Mono CN 基字）
- 派生字体与上游同样以 OFL-1.1 发布，见 [OFL.txt](https://github.com/subframe7536/maple-font/blob/v7/OFL.txt)
