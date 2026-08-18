# -*- coding: utf-8 -*-
"""【全面测试工具 · 编排器】一键运行全部验证脚本 + 单元测试 + 人工清单。

设计原则：**不复制其他脚本的代码**，通过 subprocess 依次调用 dev/ 下的
检查型脚本（_diff_lang.py / _check_i18n.py / _smoke_test.py），
解析其输出关键字判定成败，汇总生成报告 dev/_test_report.md。

覆盖范围：
  A. 静态检查：语法编译 / JSON 合法性 / 关键文件 / [子进程]键同步 / [子进程]残留检查
  B. 单元测试：App 模块纯函数（md5_hex / has_chinese / tr() / _load_lang）
  C. GUI 冒烟：[子进程] _smoke_test.py（26 页 × 三语循环，窗口保留手动关闭）
  D. 人工清单：自动无法覆盖的项目（打印 + 写入报告）

用法：
  python dev/_test_all.py          # 全部（A+B+C+D）
  python dev/_test_all.py A        # 只跑 A 段
  python dev/_test_all.py B        # 只跑 B 段
  python dev/_test_all.py C        # 只跑 C 段
  python dev/_test_all.py D        # 只跑 D 段
输入：CanApp.py + lang/*.json + UserFiles/    输出：控制台报告 + dev/_test_report.md
依赖：dev/_diff_lang.py / dev/_check_i18n.py / dev/_smoke_test.py（需可显示 GUI 环境）
"""
import io
import json
import os
import py_compile
import subprocess
import sys
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
DEV_DIR = os.path.join(ROOT, "dev")
REPORT_PATH = os.path.join(DEV_DIR, "_test_report.md")

RESULTS = []  # (section, name, ok, detail)


def check(section, name, fn):
    """执行一个内联测试项。fn 返回 (ok, detail) 或抛异常。"""
    try:
        ok, detail = fn()
        RESULTS.append((section, name, bool(ok), detail or ""))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"  ({detail})" if detail else ""))
    except Exception as e:
        RESULTS.append((section, name, False, repr(e)))
        print(f"  [FAIL] {name}  (异常: {e!r})")


def run_script(section, name, script, ok_rule, timeout=120):
    """以子进程运行 dev/{script}，按 ok_rule 解析输出判定成败。

    ok_rule: str -> 输出必须包含该关键字才 PASS；callable -> ok_rule(output) -> bool
    退出码非 0 一律 FAIL。
    """
    path = os.path.join(DEV_DIR, script)
    try:
        # 强制子进程以 UTF-8 输出：Windows 某些终端(GBK 代码页)下，子进程默认按
        # locale 编码(cp936)输出，父进程按 utf-8 解码会乱码导致关键字匹配失败误判 FAIL。
        env = dict(os.environ)
        env["PYTHONIOENCODING"] = "utf-8"
        proc = subprocess.run([sys.executable, path], capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=timeout, env=env)
        out = proc.stdout + proc.stderr
        ok = proc.returncode == 0 and (ok_rule(out) if callable(ok_rule) else ok_rule in out)
        RESULTS.append((section, name, ok, f"exit={proc.returncode}"))
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}  (exit={proc.returncode})")
        # 摘要：只显示关键行，不刷屏
        lines = [ln for ln in out.splitlines() if ln.strip()]
        shown = [ln for ln in lines if ("FAIL" in ln or "差异" in ln or "残留" in ln
                                        or "通过" in ln or "失败" in ln or "====" in ln)]
        for ln in shown[-8:]:
            print("        | " + ln.strip()[:100])
    except subprocess.TimeoutExpired:
        RESULTS.append((section, name, False, f"超时({timeout}s)"))
        print(f"  [FAIL] {name}  (超时 {timeout}s)")
    except Exception as e:
        RESULTS.append((section, name, False, repr(e)))
        print(f"  [FAIL] {name}  (异常: {e!r})")


# ============================================================
# A. 静态检查
# ============================================================
def run_static():
    print("\n===== A. 静态检查 =====")

    def a1():
        py_compile.compile(os.path.join(ROOT, "CanApp.py"), doraise=True)
        return True, "CanApp.py 语法 OK"

    def a2():
        langs = [f for f in os.listdir(os.path.join(ROOT, "lang")) if f.endswith(".json")]
        sizes = []
        for f in sorted(langs):
            d = json.load(io.open(os.path.join(ROOT, "lang", f), encoding="utf-8"))
            sizes.append(f"{f}={len(d)}")
        return len(langs) == 3, " / ".join(sizes)

    def a3():
        need = ["CanApp.py", "AppGUI_CHS.py", "lang/zh_CN.json", "lang/en_US.json",
                "lang/zh_TW.json", "UserFiles/template/GuessFist",
                "UserFiles/template/GuessNumbers", "UserFiles/template/BMI"]
        missing = [p for p in need if not os.path.exists(os.path.join(ROOT, p))]
        return not missing, ("缺失: " + ",".join(missing)) if missing else "全部存在"

    check("A", "语法编译", a1)
    check("A", "语言文件 JSON 合法", a2)
    check("A", "关键文件存在", a3)

    # 子进程：复用独立脚本，不复制其逻辑
    run_script("A", "i18n 键同步 (调用 _diff_lang.py)", "_diff_lang.py",
               lambda out: "总计差异: 0" in out)
    run_script("A", "i18n 残留检查 (调用 _check_i18n.py)", "_check_i18n.py",
               lambda out: ("残留含中文 f-string 行: 0" in out
                            and "tr(tr( 残留: 0" in out
                            and "f'. 格式错误残留: 0" in out))


# ============================================================
# B. 单元测试（纯函数，无需 GUI）
# ============================================================
def run_unit():
    print("\n===== B. 单元测试 =====")
    import hashlib
    import CanApp

    def b1():
        got = CanApp.md5_hex("")
        return got == "d41d8cd98f00b204e9800998ecf8427e", got

    def b2():
        s = "Hello 你好 123"
        return CanApp.md5_hex(s) == hashlib.md5(s.encode("utf-8")).hexdigest(), "与 hashlib 一致"

    def b3():
        return (CanApp.has_chinese("你好") and not CanApp.has_chinese("hello") and not CanApp.has_chinese("123")), ""

    def b4():
        CanApp._load_lang("zh_CN")
        return CanApp.tr("【不存在的键_测试】") == "【不存在的键_测试】", "回退原文"

    def b5():
        CanApp._load_lang("zh_CN")
        got = CanApp.tr("Ping 失败：{0}", "timeout")
        return got == "Ping 失败：timeout", got

    def b5b():
        CanApp._load_lang("zh_TW")
        got = CanApp.tr("👤 当前用户：{0}", "Alice")
        return "Alice" in got and "當前用戶" in got, got

    def b6():
        sizes = {}
        for code in CanApp.LANGUAGES:
            CanApp._load_lang(code)
            sizes[code] = len(CanApp._LANG_DICT)
        return all(v > 300 for v in sizes.values()), str(sizes)

    def b7():
        labels = {k: v for k, v in CanApp.LANGUAGES.items()}
        return list(labels.keys()) == ["zh_CN", "zh_TW", "en_US"], str(labels)

    check("B", "md5_hex 空串", b1)
    check("B", "md5_hex 与 hashlib 一致", b2)
    check("B", "has_chinese 判断", b3)
    check("B", "tr() 找不到键回退原文", b4)
    check("B", "tr() 占位符格式化", b5)
    check("B", "tr() 繁体占位符", b5b)
    check("B", "三语 _load_lang 加载", b6)
    check("B", "LANGUAGES 语言列表", b7)


# ============================================================
# C. GUI 冒烟测试（子进程调用 _smoke_test.py，不复制其逻辑）
# ============================================================
def run_gui():
    print("\n===== C. GUI 冒烟测试 =====")
    # 冒烟测试窗口在测试结束后保留（不自动关闭），子进程不会退出，
    # 因此不能用 subprocess.run 等待其结束（会超时），改为 Popen + 逐行读取输出：
    # 检测到"全部通过！"即判 PASS，窗口留给开发者查看后手动关闭。
    path = os.path.join(DEV_DIR, "_smoke_test.py")
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.Popen([sys.executable, "-u", path],
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            encoding="utf-8", errors="replace", env=env)
    lines = []

    def _reader():
        try:
            for line in proc.stdout:
                lines.append(line)
        except Exception:
            pass

    threading.Thread(target=_reader, daemon=True).start()

    timeout = 180
    ok = False
    deadline = time.time() + timeout
    while time.time() < deadline:
        if "全部通过！" in "".join(lines):
            ok = True
            break
        if proc.poll() is not None:
            break
        time.sleep(0.2)

    out = "".join(lines)
    if ok:
        detail = "全部通过！窗口保留，查看后请手动关闭"
    elif time.time() >= deadline:
        proc.kill()
        detail = f"超时({timeout}s)"
    else:
        detail = f"exit={proc.poll()}，输出未见'全部通过！'"
    RESULTS.append(("C", "26 页 × 三语循环 (调用 _smoke_test.py)", ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] 26 页 × 三语循环 (调用 _smoke_test.py)  ({detail})")
    shown = [ln for ln in out.splitlines() if ln.strip()]
    shown = [ln for ln in shown if ("FAIL" in ln or "失败" in ln or "通过" in ln or "====" in ln)]
    for ln in shown[-8:]:
        print("        | " + ln.strip()[:100])


# ============================================================
# D. 人工测试清单（自动无法覆盖）
# ============================================================
MANUAL_ITEMS = [
    ("视觉", "三语界面布局无错位、文字无截断/乱码，侧边栏与内容区比例正常"),
    ("视觉", "三语下按钮颜色/悬停/选中态正常，弹窗样式正常"),
    ("翻译", "繁体用词抽查（如 信息/软件/网络 是否习惯台湾用词，可用 s2twp 重生成）"),
    ("翻译", "英文翻译自然度抽查（按钮、提示语是否地道）"),
    ("账户", "真实注册新用户 → 登录 → 退出 → 再登录全流程，UserFiles 模板文件是否正确复制"),
    ("账户", "错误密码提示、未知用户名提示、游客身份进入"),
    ("游戏", "猜数字 / 石头剪刀布 / 读心术 各玩一局，结果统计正确"),
    ("数学", "进制转换 / 正确率 / 平均数 / 鸡兔同笼 / Collatz / 九九表 / BMI / 凑钱数 / 排序 各输入样例验证结果"),
    ("网络", "中英互译（需联网）、Ping（用 127.0.0.1）"),
    ("文本", "摩斯密码转换、Talk out 朗读（需语音组件）"),
    ("系统", "定时关机：设置后立即取消（勿真关机）"),
    ("系统", "批量创建文件：用临时目录测试后清理"),
    ("系统", "激活Windows / 蓝屏 / 恶搞：危险项建议跳过或确认环境安全"),
    ("其他", "反馈问题、更新日志、关于页显示正常"),
    ("多语言", "三语切换按钮循环顺序 zh_CN→zh_TW→en_US→zh_CN 且当前页/状态栏/标题同步刷新"),
    ("性能", "连续快速切换页面无卡顿、无内存暴涨"),
]


def run_manual_report():
    print("\n===== D. 人工测试清单（自动无法覆盖，请在 GUI 中逐项确认） =====")
    for i, (cat, item) in enumerate(MANUAL_ITEMS, 1):
        print(f"  {i:2d}. [{cat}] {item}")


# ============================================================
# 报告生成
# ============================================================
def write_report():
    from datetime import datetime
    lines = ["# 测试报告（_test_all.py · 编排器）\n",
             f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
             f"- Python: {sys.version.split()[0]}",
             f"- 项目根: {ROOT}\n",
             "## 测试结果汇总\n",
             "| 段 | 测试项 | 结果 | 说明 |",
             "|---|--------|------|------|"]
    for section, name, ok, detail in RESULTS:
        lines.append(f"| {section} | {name} | {'✅ PASS' if ok else '❌ FAIL'} | {detail} |")
    passed = sum(1 for _, _, ok, _ in RESULTS if ok)
    lines.append(f"\n**通过 {passed} / {len(RESULTS)}**\n")
    lines.append("## 人工测试清单\n")
    lines.append("| # | 分类 | 检查项 | 结果 |")
    lines.append("|---|------|--------|------|")
    for i, (cat, item) in enumerate(MANUAL_ITEMS, 1):
        lines.append(f"| {i} | {cat} | {item} | ☐ |")
    with io.open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return REPORT_PATH


def main():
    # 段落选择：python dev/_test_all.py [A|B|C|D|ALL]，默认全部
    section = (sys.argv[1] if len(sys.argv) > 1 else "ALL").upper()
    if section not in ("ALL", "A", "B", "C", "D"):
        print(f"未知段落: {section}（可选 A/B/C/D/ALL）")
        sys.exit(2)

    names = {"A": "A. 静态检查", "B": "B. 单元测试", "C": "C. GUI 冒烟", "D": "D. 人工清单"}
    print("=" * 50)
    print(f" 全面测试 _test_all.py（编排器模式）开始" +
          (f" —— 仅运行 {names[section]}" if section != "ALL" else ""))
    print("=" * 50)

    if section in ("ALL", "A"):
        run_static()
    if section in ("ALL", "B"):
        run_unit()
    if section in ("ALL", "C"):
        try:
            run_gui()
        except Exception as e:
            print(f"\n[C段跳过] GUI 环境不可用: {e!r}")
            RESULTS.append(("C", "GUI 冒烟(整体)", False, f"无法启动: {e!r}"))
    if section in ("ALL", "D"):
        run_manual_report()

    passed = sum(1 for _, _, ok, _ in RESULTS if ok)
    print("\n" + "=" * 50)
    print(f" 自动测试: 通过 {passed} / {len(RESULTS)}")
    report = write_report()
    print(f" 报告已写入: {report}")
    print("=" * 50)
    if passed == len(RESULTS):
        print(" 所有自动测试通过 ✅ 请按上方 D 清单完成人工测试后发布")
    else:
        print(" 存在失败项 ❌ 请先修复再发布")
    print("=" * 50)


if __name__ == "__main__":
    main()
