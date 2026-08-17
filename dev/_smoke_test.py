# -*- coding: utf-8 -*-
"""【验证工具】App.py GUI 冒烟测试：遍历所有页面 + 三语（简/繁/英）循环切换。

用途：
  1. 导入 App 模块并启动 App()
  2. 遍历全部 26 个页面逐个构建（打桩弹窗/危险操作，不真弹窗）
  3. 依次切换 zh_CN -> zh_TW -> en_US -> zh_CN，每轮重建全部页面并打印当前语言，全程无异常即通过
  4. 测试窗口标题显示"测试中"，测试结束窗口保留不自动关闭，手动关闭后进程退出
  5. 测试窗口可配置（文件顶部手动改，不询问用户）：
     show_dev_tab              —— 是否显示 Dev 开发者工具页（默认 False）
     home_message              —— 主页顶部提示条（默认"窗口仅为测试用"，设 None/"" 关闭）
     allow_login_and_account_page —— 是否允许登录与账户页（默认 False）
     always_login_dev_account  —— 仅当 allow_login_and_account_page=True 时生效（默认 True）：
                                  True=弹出登录窗口但强制登录 dev（用户名锁定 dev、无密码直接登录，
                                  与 App.py 强制登录处理方式一致）；False=正常登录窗口。
                                  allow_login_and_account_page=False 时优先级最高，直接禁止登录，
                                  忽略本配置的值。

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

# ============================================================
# 测试窗口配置（永久手动更改，不询问用户）
# ============================================================
show_dev_tab = False                  # True=测试窗口导航中显示 Dev 开发者工具页
home_message = "窗口仅为冒烟测试用，所有box类弹窗都将输出至控制台"        # 主页顶部提示条；设为 None 或 "" 则不显示；设为其他字符串则显示该内容
allow_login_and_account_page = False  # True=允许登录对话框与账户页（False=禁止登录、隐藏账户页与登录按钮）
always_login_dev_account = True       # 仅当 allow_login_and_account_page=True 时生效：
                                      #   True=弹出登录窗口但强制登录 dev（用户名锁定 dev、无需密码，
                                      #   与 App.py 强制登录处理方式一致）；False=正常登录窗口
APP_TITLE = "测试结束前不要关闭这个窗口，以防测试结果错误！"                  # 测试窗口标题（手动改即可）
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

# ---- 按配置调整 App 行为（monkey-patch，仅本进程生效） ----

# 登录打桩：allow_login_and_account_page=False 时禁止登录，不弹模态登录框。
# 若不打桩，App 启动 300ms 后会自动弹 LoginDialog（wait_window + grab_set），
# 模态锁定主窗口导致页面切换在后台进行、观感上"页面不自动切换"，
# 且手动输入用户名密码会真实创建用户目录，污染 UserFiles/ 测试环境。
if not allow_login_and_account_page:
    App.App.open_login = lambda self: None

# 强制 dev 登录：allow_login_and_account_page 优先级始终最高。
#  - alacp=False：上面已打桩禁止登录，完全不考虑 always_login_dev_account 的值。
#  - alacp=True 且 always_login_dev_account=True：与 App.py 处理方式一致——
#    弹出登录窗口但强制为 dev（patch _force_dev_login 使 LoginDialog 进入 forced_dev 分支：
#    用户名锁定 dev、不显示密码栏、无需密码直接登录）；同时自动完成 dev 登录，
#    避免模态登录窗口阻塞自动测试。
#  - alacp=True 且 always_login_dev_account=False：正常登录窗口（人工验证）。
if allow_login_and_account_page and always_login_dev_account:
    App._force_dev_login = lambda: True
    _orig_open_login = App.App.open_login

    def _auto_dev_open_login(self):
        dialog = App.LoginDialog(self)
        # 强制 dev 登录窗口：短暂显示（便于人工确认 UI）后自动以 dev 身份登录
        self.after(1500, lambda: dialog.do_login() if dialog.winfo_exists() else None)
        self.wait_window(dialog)

    App.App.open_login = _auto_dev_open_login

# 隐藏不需要的页面（show_dev_tab / allow_login_and_account_page 开关）
# show_dev_tab=True 时强制打开 App 的 dev_enabled，使 Dev 页在测试窗口可见
if show_dev_tab:
    App.dev_enabled = True
_hidden = set()
if not show_dev_tab:
    _hidden.add("dev")
if not allow_login_and_account_page:
    _hidden.add("account")
if _hidden:
    App.App.PAGE_BUILDERS = {k: v for k, v in App.App.PAGE_BUILDERS.items() if k not in _hidden}
    _orig_nav_groups = App.App._nav_groups

    def _nav_groups_filtered(self):
        return [(g, [it for it in items if it[0] not in _hidden])
                for g, items in _orig_nav_groups(self)]

    App.App._nav_groups = _nav_groups_filtered

# 主页顶部提示条（home_message 配置）
if home_message:
    _orig_build_home = App.App._build_home_page

    def _build_home_with_msg(self, frame):
        _orig_build_home(self, frame)
        children = frame.winfo_children()
        lbl = App.tk.Label(frame, text=home_message, font=(App.FONT, 10, "bold"),
                           bg=App.COLORS["warning"], fg="white", anchor="w",
                           padx=12, pady=6)
        if children:
            lbl.pack(fill="x", before=children[0])
        else:
            lbl.pack(fill="x")

    App.App._build_home_page = _build_home_with_msg

print("模块导入成功")

app = App.App()
app.title(APP_TITLE)
app.update()

# allow_login_and_account_page=False 时隐藏状态栏的"登录 / 切换账户"按钮
if not allow_login_and_account_page:
    app.btn_switch.pack_forget()

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

    # 测试结束不关闭窗口：保留界面供开发者查看，手动关闭窗口后 mainloop 返回、进程自然退出。
    print("测试完成，窗口保留（标题：测试中），查看后请手动关闭。")


app.after(200, run_tests)
app.mainloop()
