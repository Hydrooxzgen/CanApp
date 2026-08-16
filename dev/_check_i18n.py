# -*- coding: utf-8 -*-
"""【验证工具】i18n 转换完整性检查。

用途：检查 App.py 中是否存在转换残留/错误：
  1. 含中文的 f-string（应全部转成 tr()，只允许 f"{total}" 这类无中文的）
  2. tr(tr( 双重包裹残留
  3. 格式说明符错误（如 f'.2f'）
  4. tr( 调用总数统计

用法：python dev/_check_i18n.py
输入：App.py       输出：控制台检查报告
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = io.open(os.path.join(ROOT, 'App.py'), encoding='utf-8').read()

# 1. 残留含中文的 f-string
f_res = [l for i, l in enumerate(s.splitlines(), 1)
         if re.search(r'f["\']', l) and re.search(r'[\u4e00-\u9fff]', l)]
print('残留含中文 f-string 行:', len(f_res))
for l in f_res[:10]:
    print('   ', l.strip()[:100])

# 2. tr(tr( 双包
print('tr(tr( 残留:', s.count('tr(tr('))

# 3. 格式说明符错误 f'.2f'
print("f'. 格式错误残留:", len(re.findall(r"f'\.\d", s)))

# 4. 统计 tr( 调用数
print('tr( 调用数:', len(re.findall(r'\btr\(', s)))
