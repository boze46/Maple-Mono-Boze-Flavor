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
   `MapleBozeNR-Regular.ttf`,PS 名为 `MapleBozeNR-Regular`。只归档
   NF-CN 静态 TTF;OTF 转 CFF 对部分中文字重会静默失败,WOFF2 单字重
   压缩约 80 秒,两者都不发布。

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
    # ⑤ 只发布 NF-CN 的 TTF:归档时跳过纯拉丁 TTF / TTF-AutoHint /
    #    NF / CN / Variable / OTF / Woff2 目录。
    #    OTF 转换对部分中文字重会报 CorrectContoursError 但退出码为 0,
    #    产出残缺且不报错;WOFF2 单字重压缩约 80 秒。两者都不发布。
    (
        """        for f in listdir(build_option.output_dir):
            if f == archive_dir_name or f.endswith(".json"):
                continue
""",
        """        for f in listdir(build_option.output_dir):
            if f == archive_dir_name or f.endswith(".json"):
                continue
            if f in (
                "TTF",
                "TTF-AutoHint",
                "NF",
                "CN",
                "Variable",
                "OTF",
                "Woff2",
            ):
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
