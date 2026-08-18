# -*- coding: utf-8 -*-
"""【验证工具】i18n 转换完整性检查。

用途：检查 CanApp.py 中是否存在转换残留/错误：
  1. 含中文的 f-string（应全部转成 tr()，只允许 f"{total}" 这类无中文的）
  2. tr(tr( 双重包裹残留
  3. 格式说明符错误（如 f'.2f'）
  4. tr( 调用总数统计

用法：python dev/_check_i18n.py
输入：CanApp.py       输出：控制台检查报告
"""
import ast
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = io.open(os.path.join(ROOT, 'CanApp.py'), encoding='utf-8').read()
tree = ast.parse(s)


def has_cn(text):
    return any('\u4e00' <= ch <= '\u9fff' for ch in text)


# 1. 残留含中文的 f-string（ast 精确判断：f-string 的字面量部分含中文才计入，
#    避免 f"{total}" 与 tr("中文") 同行被正则误报）
f_res = []
for node in ast.walk(tree):
    if isinstance(node, ast.JoinedStr):
        lit = ''.join(v.value if isinstance(v, ast.Constant) and isinstance(v.value, str)
                      else '' for v in node.values)
        if has_cn(lit):
            f_res.append((node.lineno, ast.get_source_segment(s, node)))
print('残留含中文 f-string 行:', len(f_res))
for ln, seg in f_res[:10]:
    print(f'   行{ln}: {seg.strip()[:100]}')

# 2. tr(tr( 双包
print('tr(tr( 残留:', s.count('tr(tr('))

# 3. 格式说明符错误 f'.2f'
print("f'. 格式错误残留:", len(re.findall(r"f'\.\d", s)))

# 4. 统计 tr( 调用数
print('tr( 调用数:', len(re.findall(r'\btr\(', s)))
