# -*- coding: utf-8 -*-
"""【诊断工具】对比 CanApp.py 的 tr() 键与语言文件键的双向差异。

用途：确保 CanApp.py 与 lang/ 下所有语言文件（zh_CN / en_US / zh_TW）键完全同步。
- "json 有但代码没有"：语言文件中的孤儿键（可清理）
- "代码有但 json 没有"：代码中新增但未补入语言文件的键（需 _gen_lang_zh.py）

用法：python dev/_diff_lang.py
输入：CanApp.py + lang/*.json    输出：控制台差异清单
"""
import ast
import glob
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = io.open(os.path.join(ROOT, "CanApp.py"), encoding="utf-8").read()
tree = ast.parse(src)

keys = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "tr":
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            keys.add(node.args[0].value)

total = 0
for lang_file in sorted(glob.glob(os.path.join(ROOT, "lang", "*.json"))):
    name = os.path.basename(lang_file)
    data = json.load(io.open(lang_file, encoding="utf-8"))
    orphan = [k for k in data if k not in keys]
    missing = [k for k in keys if k not in data]
    print(f"== {name}: 共 {len(data)} 键 | 孤儿(代码没有) {len(orphan)} | 缺失(代码有) {len(missing)}")
    for k in sorted(orphan):
        print("   -", repr(k[:80]))
    for k in sorted(missing):
        print("   +", repr(k[:80]))
    total += len(orphan) + len(missing)
print("总计差异:", total)
