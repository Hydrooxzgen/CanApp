# -*- coding: utf-8 -*-
"""【调试工具】列出 App.py 中所有含中文的 f-string（含行号和内容）。

用途：排查哪些 f-string 尚未被 _fstring_convert.py 转换。

用法：python dev/_list_fstrings.py
输入：App.py       输出：控制台逐条列出（行号 + 源码片段）
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
lines = io.open(os.path.join(ROOT, 'App.py'), encoding='utf-8').read().splitlines()

pat = re.compile(r'.*f["\']')
for i, line in enumerate(lines, 1):
    # 行内找 f-string（简单启发式：包含 f" 或 f' 且含中文）
    if re.search(r'f["\']', line) and re.search(r'[\u4e00-\u9fff]', line):
        print(f'{i:5d} | {line.strip()[:110]}')
