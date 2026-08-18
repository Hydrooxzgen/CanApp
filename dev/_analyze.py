# -*- coding: utf-8 -*-
"""【调试工具】分析 CanApp.py 中中文字符串规模（f-string / 普通字符串统计）。

用途：评估 i18n 改造工作量，粗略统计含中文的 f-string 与普通字符串数量。

用法：python dev/_analyze.py
输入：CanApp.py       输出：控制台统计报告
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = io.open(os.path.join(ROOT, 'CanApp.py'), encoding='utf-8').read()

# 粗略统计：f-string 中含中文
f_strings = re.findall(r'f["\'](?:[^"\'\\]|\\.)*[\u4e00-\u9fff]', src)
# 普通字符串中含中文（避免匹配 f-string 开头）
plain = re.findall(r'(?<![frb])["\'](?:[^"\'\\]|\\.)*[\u4e00-\u9fff](?:[^"\'\\]|\\.)*["\']', src)

print('含中文的 f-string 数量:', len(f_strings))
print('含中文的普通字符串数量:', len(plain))
print()
print('=== f-string 示例（前 30 个）===')
for s in f_strings[:30]:
    print('  ', s[:80].replace('\n', '\\n'))
