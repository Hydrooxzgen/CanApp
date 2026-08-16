# -*- coding: utf-8 -*-
"""【验证工具】App.py GUI 冒烟测试：遍历所有页面 + 三语（简/繁/英）循环切换。

用途：
  1. 导入 App 模块并启动 App()
  2. 遍历全部 26 个页面逐个构建（打桩弹窗/危险操作，不真弹窗）
  3. 依次切换 zh_CN -> zh_TW -> en_US -> zh_CN，每轮重建全部页面并打印当前语言，全程无异常即通过

用法：python dev/_smoke_test.py
输入：App.py       输出：控制台逐页 OK/FAIL 报告
依赖：重建管线（_rebuild.py + _fstring_convert.py）之后运行
"""
import io
import os
import sys
import traceback

# 项目根加入 sys.path，确保 import App 可用
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

print("项目根目录:", ROOT)
print("Python 版本:", sys.version)
print("Tkinter 版本:", __import__("tkinter").Tcl().eval('info patchlevel'))
print("开始smoke test!!")
# ---- 打桩：避免弹窗阻塞与危险操作 ----
import tkinter.messagebox as _mb
_mb.showinfo = lambda *a, **k: print("[msgbox-info]", str(a[1])[:40])
_mb.showwarning = lambda *a, **k: print("[msgbox-warn]", str(a[1])[:40])
_mb.showerror = lambda *a, **k: print("[msgbox-err ]", str(a[1])[:40])
_mb.askyesno = lambda *a, **k: False
_mb.askokcancel = lambda *a, **k: False

import tkinter.simpledialog as _sd
_sd.askstring = lambda *a, **k: "test"
_sd.askinteger = lambda *a, **k: 5
_sd.askfloat = lambda *a, **k: 1.5

import tkinter.filedialog as _fd
_fd.askdirectory = lambda *a, **k: "C:/Users"
_fd.askopenfilename = lambda *a, **k: "C:/test.txt"

import subprocess as _sp
_sp.Popen = lambda *a, **k: print("[subprocess]", str(a)[:60])
_sp.run = lambda *a, **k: print("[subprocess.run]", str(a)[:60])

import importlib
print("尝试导入App...")
import App

# 打桩登录对话框：冒烟测试全自动，不弹出模态登录框。
# 若不打桩，App 启动 300ms 后会自动弹 LoginDialog（wait_window + grab_set），
# 模态锁定主窗口导致页面切换在后台进行、观感上"页面不自动切换"，
# 且手动输入用户名密码会真实创建用户目录，污染 UserFiles/ 测试环境。
App.App.open_login = lambda self: None

print("模块导入成功")

app = App.App()
app.update()

errors = []
print("登录对话框已打桩（不弹出），开始遍历页面...")


def try_page(pid):
    try:
        app.show_page(pid)
        app.update()
        return True
    except Exception:
        errors.append((pid, traceback.format_exc()))
        print("  页面失败:", pid)
        return False


def run_tests():
    # 1. 首页
    print("首页:", "OK" if try_page("home") else "FAIL")
    print("  状态栏:", app.status_user.cget("text"))
    print("  语言按钮:", app.btn_lang.cget("text"))

    # 2. 遍历所有导航页面
    pids = [pid for pid, _ in App.App.PAGE_BUILDERS.items()]
    print("总页面数:", len(pids))
    ok = 0
    for pid in pids:
        if try_page(pid):
            ok += 1
    print("构建成功:", ok, "/", len(pids))

    # 3-5. 三语循环切换：zh_CN -> zh_TW -> en_US -> zh_CN
    langs = ["简体(zh_CN)", "繁体(zh_TW)", "英文(en_US)"]
    for i in range(3):
        try:
            app._switch_lang()
            app.update()
            cur = App._CURRENT_LANG
            print(f"[{langs[i]}] 当前语言:{cur} 语言按钮:{app.btn_lang.cget('text')}")
            print(f"[{langs[i]}] 状态栏:{app.status_user.cget('text')}")
            print(f"[{langs[i]}] 首页标题:{app.nav.item(app.nav.get_children()[0], 'text')}")
        except Exception:
            errors.append((f"switch_{langs[i]}", traceback.format_exc()))

        # 该语言下重建所有页面
        ok2 = 0
        for pid in pids:
            if try_page(pid):
                ok2 += 1
        print(f"[{langs[i]}] 构建成功: {ok2}/{len(pids)}")

    print("=" * 40)
    if errors:
        print("失败", len(errors), "项：")
        for pid, tb in errors:
            print("----", pid)
            print(tb[:1500])
    else:
        print("全部通过！")

    app.destroy()


app.after(200, run_tests)
app.mainloop()
