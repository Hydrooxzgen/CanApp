# -*- coding: utf-8 -*-
"""【语言文件工具】生成 lang/zh_TW.json（繁体中文版）。

用途：读取 lang/zh_CN.json（键=简体原文），用 OpenCC 简->繁转换每个键的值。
- 键保持简体原文不变（tr() 用代码中的简体字符串查找）
- 值转换为繁体中文（含 {0} 等占位符不受影响）
- 未安装 OpenCC 时提示安装命令并退出

用法：python dev/_gen_lang_tw.py
输入：lang/zh_CN.json    输出：lang/zh_TW.json
依赖：pip install opencc-python-reimplemented
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
zh_path = os.path.join(ROOT, "lang", "zh_CN.json")
tw_path = os.path.join(ROOT, "lang", "zh_TW.json")

zh = json.load(io.open(zh_path, encoding="utf-8"))

try:
    import opencc
except ImportError:
    print("未安装 OpenCC，请先执行: pip install opencc-python-reimplemented")
    raise SystemExit(1)

converter = opencc.OpenCC("s2t")  # 简体 -> 繁体（纯字形转换）
tw = {}
changed = 0
for key, value in zh.items():
    trad = converter.convert(value)
    if trad != value:
        changed += 1
    tw[key] = trad

with io.open(tw_path, "w", encoding="utf-8") as f:
    json.dump(tw, f, ensure_ascii=False, indent=2)

print(f"生成完成: {tw_path}")
print(f"总键数: {len(tw)}，转换后内容有变化: {changed}，繁简同形（未变化）: {len(tw) - changed}")
