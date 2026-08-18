# -*- coding: utf-8 -*-
"""【重建管线 · 第 2 步】把 CanApp.py 中含中文的 f-string 转换为 tr('模板', 参数...)。

用途：_rebuild.py 执行后，将剩余的 f-string 翻译为 i18n 调用。
注：i18n的作用是通过key找到对应语言的翻译文本
- 用 ast 解析每个 f-string（含跨行隐式拼接组）为 模板 + 参数列表
- 位置参数占位符 {}；格式说明符保留如 {0:.2f}
- 无中文字面量的 f-string 跳过（如 f"{total}"）

用法：python dev/_fstring_convert.py
输入：CanApp.py       输出：CanApp.py（原地修改）
依赖：先运行 _rebuild.py，之后建议运行 _smoke_test.py 验证
"""
import ast
import io
import os
import token
import tokenize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "CanApp.py")


def has_cn(text):
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def convert_group(src_text):
    """解析一组拼接的字符串/f-string 源码 -> tr('...', args) 或 None"""
    try:
        # 用括号包裹：跨行隐式拼接在括号内才是合法表达式
        node = ast.parse("(" + src_text + ")", mode="eval").body
    except SyntaxError:
        return None
    if isinstance(node, ast.Constant):
        if not has_cn(node.value):
            return None
        tpl = node.value.replace("{", "{{").replace("}", "}}")
        return "tr(" + repr(tpl) + ")"
    if not isinstance(node, ast.JoinedStr):
        return None
    has_cn_any = any(
        isinstance(v, ast.Constant) and isinstance(v.value, str) and has_cn(v.value)
        for v in node.values)
    if not has_cn_any:
        return None

    def spec_text(fv):
        """手动提取格式说明符文本（unparse 会把 JoinedStr 输出成 f'...'）"""
        if fv.format_spec is None:
            return ""
        parts = []
        for v in fv.format_spec.values:
            if isinstance(v, ast.Constant):
                parts.append(v.value)
            else:
                parts.append("{" + ast.unparse(v.value) + "}")
        return "".join(parts)

    template = []
    args = []
    for v in node.values:
        if isinstance(v, ast.Constant):
            template.append(v.value.replace("{", "{{").replace("}", "}}"))
        else:  # ast.FormattedValue
            idx = len(args)
            args.append(ast.unparse(v.value))
            spec = spec_text(v)
            template.append("{" + str(idx) + (":" + spec if spec else "") + "}")
    code = "tr(" + repr("".join(template))
    if args:
        code += ", " + ", ".join(args)
    code += ")"
    return code


def main():
    src = io.open(SRC, encoding="utf-8").read()
    lines = src.splitlines(keepends=True)
    line_offsets = []
    off = 0
    for ln in lines:
        line_offsets.append(off)
        off += len(ln)

    def offset(row, col):
        return line_offsets[row - 1] + col

    tokens = list(tokenize.generate_tokens(io.StringIO(src).readline))

    # 收集拼接组：STRING / FSTRING 跨度 连续出现（允许 NL/COMMENT 间隔）
    groups = []  # list of [start_off, end_off]
    i = 0
    n = len(tokens)
    while i < n:
        typ = tokens[i][0]
        is_str = typ == token.STRING
        is_fstart = typ == token.FSTRING_START
        if is_str or is_fstart:
            # 找到组尾
            j = i
            end_tok = tokens[i]
            while True:
                if tokens[j][0] == token.STRING:
                    end_tok = tokens[j]
                    j += 1
                elif tokens[j][0] == token.FSTRING_START:
                    while j < n and tokens[j][0] != token.FSTRING_END:
                        j += 1
                    end_tok = tokens[j] if j < n else end_tok
                    j += 1
                elif tokens[j][0] in (token.NL, token.COMMENT):
                    j += 1
                else:
                    break
                if j >= n:
                    break
            start_off = offset(*tokens[i][2])
            end_off = offset(*end_tok[3])
            groups.append([start_off, end_off, False])  # False = 未处理
            i = j
        else:
            i += 1

    # 转换：只处理含 FSTRING_START 的组（普通字符串组已在重建脚本处理过）
    replacements = []
    for g in groups:
        start_off, end_off, _ = g
        seg = src[start_off:end_off]
        # 检查组内是否含 f-string
        seg_tokens = list(tokenize.generate_tokens(io.StringIO(seg).readline))
        has_f = any(t[0] == token.FSTRING_START for t in seg_tokens)
        if not has_f:
            continue
        code = convert_group(seg)
        if code:
            replacements.append((start_off, end_off, code))

    # 应用替换（从后往前）
    out = src
    for start_off, end_off, code in sorted(replacements, reverse=True):
        out = out[:start_off] + code + out[end_off:]

    with io.open(SRC, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    print("已转换 f-string 组:", len(replacements), "处")


if __name__ == "__main__":
    main()
