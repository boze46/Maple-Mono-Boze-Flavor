# MapleMono-BozeFavor

基于 [subframe7536/maple-font](https://github.com/subframe7536/maple-font) v7 稳定线的个人自定义构建：**Boze Flavor**。本仓库只放配置和 CI workflow，不 fork 上游，不提交字体文件；构建在 GitHub Actions 上完成，产物发布到本仓库的 Releases。

配置来自官方 playground（<https://font.subf.dev/en/playground/>）的导出，原始导出记录在 [font.md](./font.md)，构建实际读取的是 [config.json](./config.json)。

## 字体命名对照

构建脚本会把 `family_name` 按空格分词并逐词 `capitalize()`，所以这里写的是 `Boze Flavor`（两个词）而不是 `BozeFlavor`——这样 compact 名才能保留驼峰。宽度会自动追加后缀（`narrow` → `NR`，`slim` → `SL`）；`nerd_font.mono: true` 使 NF 族名带 `NFMono`（图标全部单宽，与 Sarasa Term SC Nerd 行为一致）。最终产物：

| 位置 | 名字 |
|---|---|
| 目录 / 仓库名 | `MapleMono-BozeFavor`（建目录时的拼写，与字体名差一个 l，不影响构建） |
| 字体族名（fontconfig / 应用里显示） | `Maple Mono Boze Flavor NR NFMono` / `… NR NFMono CN`，以及对应的 `SL` 版本 |
| 文件名 / zip / PostScript 前缀 | `MapleMonoBozeFlavor{NR,SL}-NFMono…`（zip 名不带 Mono，如 `MapleMonoBozeFlavorNR-NF-CN.zip`） |

hinted 与 unhinted 产物的**族名完全相同**，只靠 zip 名里的 `-unhinted` 后缀区分——同一台机器不要同时安装同宽度的两套。

## 构建

GitHub Actions → **Build MapleMono-BozeFlavor** → Run workflow：

- `upstream_ref`：上游 ref，默认 `v7` 分支（当前 v7.9，commit `5ee93150fbafe59dc805c2f64ad879fd14c3ce78`）。要严格复现就填 tag（如 `v7.9`）或上面的 SHA；要跟进 v7.x 更新就保持 `v7`。
- 一次触发产出**四套预设**（width × hint）：matrix 并行构建 `narrow`（550/1100）与 `slim`（500/1000，与 Sarasa Term SC 完全一致的 2:1 字距）两个宽度，每个宽度先全量构建 hinted 版（`python build.py --archive`，1080p 用），再把 `use_hinted` / `cn.use_hinted` 切为 `false`，用 `python build.py --archive --cache` 复用基字、只重打 NF / NF-CN（zip 带 `-unhinted` 后缀，2K 用）。最小格式（TTF / TTF-AutoHint / OTF / WOFF2 / Variable）与 hint 预设无关，每个宽度各出一份（TTF 即 unhinted、TTF-AutoHint 即 hinted）。
- 特性冻结、宽度基准、NF mono 全部由 `config.json` 驱动，不传变体 CLI flag，也不用 `--normal`。
- `use_font_patcher: false`，走预编译 NF glyph 合并，**不需要 FontForge**。
- 产物在 `fonts/archive`，每个 zip 配套 `.sha256`；同时上传为 workflow artifact，并发布成 Release（tag 为时间戳，标记 `--latest`），Release notes 里附四套预设各自合并后的完整配置。

## 下载

```bash
# 最新一次构建的全部 zip
gh release download -R boze46/MapleMono-BozeFavor --pattern '*.zip'

# 固定链接（文件名以 Release 里的实际名为准，形如 MapleMonoBozeFlavorNR-NF-CN.zip /
# MapleMonoBozeFlavorSL-NF-CN-unhinted.zip）
curl -LO https://github.com/boze46/MapleMono-BozeFavor/releases/latest/download/<文件名>
```

接 nix flake 时用 `fetchurl` 拉 latest 固定链接即可，升级字体 = 改一次 hash。

## 改配置

1. 回 playground 调整 → 导出 JSON；
2. 更新本仓库 `config.json`（`family_name` 保持 `Maple Mono Boze Flavor` 不动，其余按导出覆盖；两处固定不跟导出：`cn.narrow` 保持 `false`——开它会破坏中英 2:1 与等宽标志（#249），slim 下更是 v7.9 的 no-op 分支；`nerd_font.mono` 保持 `true`。注意 playground 若切到 v8 线，导出格式会变成 `cjk` 结构，与 v7 不兼容）；
3. 提交后在 Actions 重跑 workflow。

上游升级同理：改 `upstream_ref`（workflow 默认值或手动输入）。

## 本地构建（可选）

```bash
git clone https://github.com/subframe7536/maple-font -b v7
cd maple-font && cp /path/to/config.json .
pip install -r requirements.txt
python build.py --archive
```

网络受限环境改 `config.json` 的 `github_mirror`，或设环境变量 `GITHUB=<镜像域名>`。

## License

字体基于上游 [OFL-1.1](https://github.com/subframe7536/maple-font/blob/v7/OFL.txt)，派生版同样遵循 OFL 发布。
