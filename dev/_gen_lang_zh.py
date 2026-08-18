# -*- coding: utf-8 -*-
"""【语言文件工具】清理/补齐 lang/zh_CN.json。

用途：
  1. 从 CanApp.py 用 ast 提取全部 tr('...') 键
  2. 与现有 zh_CN.json 合并，删除代码中已不存在的键、补齐新键（新键值=原文）
  3. 导出键清单到 dev/_lang_keys.txt（调试用）

用法：python dev/_gen_lang_zh.py
输入：CanApp.py + lang/zh_CN.json    输出：lang/zh_CN.json（原地重写）
依赖：先运行 _gen_lang_en.py 可生成对应的 en_US.json
"""
import ast
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "CanApp.py")
LANG = os.path.join(ROOT, "lang", "zh_CN.json")

src = io.open(SRC, encoding="utf-8").read()
tree = ast.parse(src)

keys = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "tr":
        if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
            keys.add(node.args[0].value)

existing = json.load(io.open(LANG, encoding="utf-8"))
new_dict = {}
for k in sorted(keys):
    new_dict[k] = existing.get(k, k)

with io.open(LANG, "w", encoding="utf-8") as f:
    json.dump(new_dict, f, ensure_ascii=False, indent=2)

with io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lang_keys.txt"), "w", encoding="utf-8") as f:
    for k in sorted(keys):
        f.write(repr(k) + "\n")

print("清理后 zh_CN.json 条目:", len(new_dict))
print("键清单已导出到 _lang_keys.txt")
