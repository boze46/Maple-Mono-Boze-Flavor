#!/usr/bin/env python3
"""缩减上游生成的字体族名,并把所有字重归入同一 family。

两件事:

1. family 命名:上游把技术后缀拼进 NameID1 —— 宽度(NR/SL,来自
   `_update_family_names`)、Nerd Font(`NFMono`)、中文字集(`CN`)。
   加上 config.json 里的 `Flavor`,最终是
   "Maple Mono Boze Flavor NR NFMono CN"。本脚本去掉 NF/CN 两段,
   配合 config.json 的 `family_name: "Maple Boze"` 得到
   "Maple Boze NR" / "Maple Boze SL"。宽度后缀必须保留:workflow
   的 matrix 同时构建两套,zip 名 = family_name_compact + 目录名,
   去掉后两套 zip 会重名。

2. 字重:上游 parse_style_name() 对非 RIBBI 字重(Thin/Light/Medium/…)
   沿用旧 Windows 做法,NameID1 拼字重后缀、基础名塞进 NameID16,
   fontconfig 会把两者都注册成 family。改成 NameID1 为统一族名、
   NameID2 存字重、不写 NameID16/17。

3. 文件名与 PostScript 名:去掉 `NFMono`/`NFMono-CN` 前缀,产物叫
   `MapleBozeNR-Regular.ttf`,PS 名为 `MapleBozeNR-Regular`。zip 包名
   仍保留变体区分(同一 Release 要放 TTF/NF/NF-CN 多个包,重名会发布失败)。

上游代码变动导致任一处匹配失败时直接报错,避免静默退化成旧命名。
"""
import pathlib
import sys

# (原片段, 替换后)
REPLACEMENTS = [
    # ① 非 RIBBI 字重:不再把字重拼进 NameID1
    (
        '''    else:
        return (
            " " + style_name_compact.replace("Italic", ""),
            "Italic" if is_italic else "Regular",
            _style_name,
            False,
            is_italic,
        )''',
        '''    else:
        # BozeFlavor: 非 RIBBI 字重也用基础家族名作 NameID1,字重放
        # NameID2 且不写 NameID16/17,让 fontconfig 归为一个 family。
        return (
            "",
            _style_name,
            _style_name,
            True,
            is_italic,
        )''',
    ),
    # ② NF 构建:族名不再拼 NFMono
    (
        'family_name=f"{font_config.family_name} {nf_sym}{style_nf_with_prefix_space}",',
        'family_name=f"{font_config.family_name}{style_nf_with_prefix_space}",',
    ),
    (
        'full_name=f"{font_config.family_name} {nf_sym} {style_in_17}",',
        'full_name=f"{font_config.family_name} {style_in_17}",',
    ),
    (
        'preferred_family_name=f"{font_config.family_name} {nf_sym}",',
        "preferred_family_name=font_config.family_name,",
    ),
    # ③ CN 构建:族名不再拼 NFMono CN / CN
    (
        'family_name=f"{font_config.family_name} {build_option.cn_suffix}{style_cn_with_prefix_space}",',
        'family_name=f"{font_config.family_name}{style_cn_with_prefix_space}",',
    ),
    (
        'full_name=f"{font_config.family_name} {build_option.cn_suffix} {style_in_17}",',
        'full_name=f"{font_config.family_name} {style_in_17}",',
    ),
    (
        'preferred_family_name=f"{font_config.family_name} {build_option.cn_suffix}",',
        "preferred_family_name=font_config.family_name,",
    ),
    # ④ 文件名与 PostScript 名:去掉 NFMono / NFMono-CN 前缀。
    # PS 名仍由「族名-字重」组成,唯一性只在同宽度多套变体共存时才需要,
    # 而 workflow 的产物本来就要求同宽度只装一套。
    (
        'postscript_name = f"{font_config.family_name_compact}-{nf_sym}-{style_compact_nf}"',
        'postscript_name = f"{font_config.family_name_compact}-{style_compact_nf}"',
    ),
    (
        'postscript_name = f"{font_config.family_name_compact}-{build_option.cn_suffix_compact}-{style_compact_cn}"',
        'postscript_name = f"{font_config.family_name_compact}-{style_compact_cn}"',
    ),
    # ⑤ 只发布 NF-CN 基底:OTF / WOFF2 改从 NF-CN 静态 TTF 转换,
    #    归档时跳过纯拉丁 TTF / NF / Variable / CN 目录。
    (
        """    # Build variants
    build_nerd_fonts(font_config, build_option, target_styles)
    build_chinese_fonts(font_config, build_option, target_styles)
""",
        """    # Build variants
    build_nerd_fonts(font_config, build_option, target_styles)
    build_chinese_fonts(font_config, build_option, target_styles)
    if not should_use_cache:
        convert_cn_formats(build_option)
""",
    ),
    (
        """# Now, refactor the main function to use these
def main(""",
        '''def convert_cn_formats(build_option: BuildOption):
    """BozeFlavor: OTF / WOFF2 改以 NF-CN 静态 TTF 为基底。

    上游这两种格式只从纯拉丁 base TTF 转换,不含 Nerd 图标与中文。
    清空后重新从 output_cn 生成;必须在 archive 之前调用,且只在
    hinted 那一轮执行,避免 unhinted 轮把已归档内容覆盖。
    """
    if not build_option.is_cn_built:
        return
    for d in (build_option.output_otf, build_option.output_woff2):
        shutil.rmtree(d, ignore_errors=True)
        makedirs(d, exist_ok=True)
    for f in listdir(build_option.output_cn):
        if not f.endswith(".ttf"):
            continue
        src = joinPaths(build_option.output_cn, f)
        run(f"ftcli converter ttf2otf {src} -out {build_option.output_otf}")
        run(f"ftcli converter ft2wf {src} -out {build_option.output_woff2} -f woff2")


# Now, refactor the main function to use these
def main(''',
    ),
    (
        """        for f in listdir(build_option.output_dir):
            if f == archive_dir_name or f.endswith(".json"):
                continue
""",
        """        for f in listdir(build_option.output_dir):
            if f == archive_dir_name or f.endswith(".json"):
                continue
            if f in ("TTF", "TTF-AutoHint", "NF", "CN", "Variable"):
                continue
""",
    ),
]


def main() -> int:
    root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "maple")
    utils_path = root / "source" / "py" / "utils.py"
    build_path = root / "build.py"

    targets = {
        utils_path: [REPLACEMENTS[0]],
        build_path: REPLACEMENTS[1:],
    }

    for path, pairs in targets.items():
        text = path.read_text()
        changed = 0
        for old, new in pairs:
            # 先查新文本:插入型替换(新内容包含旧内容)也要能判幂等
            if new in text:
                continue
            if old not in text:
                print(
                    f"错误: {path} 里找不到待替换片段,上游可能已改动:\n{old[:80]}",
                    file=sys.stderr,
                )
                return 1
            text = text.replace(old, new, 1)
            changed += 1
        if changed:
            path.write_text(text)
            print(f"已应用 {changed} 处命名补丁: {path}")
        else:
            print(f"已打过补丁,跳过: {path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
