#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Author: Hydrooxygen
# Github: github.com/Hydrooxzgen
# ------------------------------------------------------------
"""
App_GUI v1.0.0 Single Language Version
此为单语言版本不再更新
"""

import hashlib
import os
import random
import shutil
import socket
import subprocess
import sys
import threading



# ------------------------------------------------------------
# 提醒:
# 必须在 import tkinter 之前设置 TCL_LIBRARY / TK_LIBRARY绑定输入
# ------------------------------------------------------------
def _fix_tcl_library():
    if os.environ.get("TCL_LIBRARY") and os.environ.get("TK_LIBRARY"):
        return
    candidates = [sys.prefix, os.path.dirname(sys.executable)]
    if hasattr(sys, "base_prefix") and sys.base_prefix not in candidates:
        candidates.append(sys.base_prefix)
    for base in candidates:
        tcl_dir = os.path.join(base, "tcl", "tcl8.6")
        tk_dir = os.path.join(base, "tcl", "tk8.6")
        if os.path.isfile(os.path.join(tcl_dir, "init.tcl")):
            os.environ.setdefault("TCL_LIBRARY", tcl_dir)
        if os.path.isdir(tk_dir):
            os.environ.setdefault("TK_LIBRARY", tk_dir)
        if os.environ.get("TCL_LIBRARY") and os.environ.get("TK_LIBRARY"):
            return


_fix_tcl_library()

import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk


try:
    import requests
except ImportError:
    requests = None

try:
    from pythonping import ping as py_ping
except ImportError:
    py_ping = None

APP_SHORT_NAME = "NiceProgram"          # shorname for 侧边栏
APP_TITLE = "NiceProgram App"           # fullname for title & about page
APP_VERSION = "1.0.0 单语言简体中文版-不再更新"                   # version here
APP_AUTHOR = "Hydrooxygen"                 # Author: Hydrooxygen

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERFILES_DIR = os.path.join(BASE_DIR, "UserFiles")
TEMPLATE_DIR = os.path.join(USERFILES_DIR, "template")

MORSE_CODES = {
    "a": ".-", "b": "-...", "c": "-.-.", "d": "-..", "e": ".",
    "f": "..-.", "g": "--.", "h": "....", "i": "..", "j": ".---",
    "k": "-.-", "l": ".-..", "m": "--", "n": "-.", "o": "---",
    "p": ".--.", "q": "--.-", "r": ".-.", "s": "...", "t": "-",
    "u": "..-", "v": "...-", "w": ".--", "x": "-..-", "y": "-.--",
    "z": "--..",
}

# **颜色主题**
COLORS = {
    "bg": "#F1F5F9",
    "sidebar": "#1E293B",
    "sidebar_text": "#E2E8F0",
    "sidebar_sel": "#2563EB",
    "card": "#FFFFFF",
    "primary": "#2563EB",
    "primary_dark": "#1D4ED8",
    "success": "#16A34A",
    "danger": "#DC2626",
    "warning": "#D97706",
    "text": "#0F172A",
    "text_light": "#64748B",
    "border": "#E2E8F0",
    "console": "#0B1220",
    "console_text": "#E2E8F0",
    "statusbar": "#0F172A",
}

FONT = "Microsoft YaHei UI"
MONO = "Consolas"


def md5_hex(text: str) -> str:
    """返回字符串的md5十六进制"""
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def has_chinese(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


def ensure_user_dirs(username: str) -> None:
    """!!creat template dirs for new user!!"""
    user_dir = os.path.join(USERFILES_DIR, username)
    os.makedirs(user_dir, exist_ok=True)
    for sub in ("GuessFist", "GuessNumbers", "BMI"):
        dst = os.path.join(user_dir, sub)
        os.makedirs(dst, exist_ok=True)
        src = os.path.join(TEMPLATE_DIR, sub)
        if os.path.isdir(src):
            for name in os.listdir(src):
                src_file = os.path.join(src, name)
                if os.path.isfile(src_file):
                    shutil.copy2(src_file, dst)


# ============================================================
# 登录 / 注册 enter box
# ============================================================
class LoginDialog(tk.Toplevel):
    RESULT_CANCEL = 0
    RESULT_GUEST = 1
    RESULT_OK = 2

    def __init__(self, master):
        super().__init__(master)
        self.title("登录")
        self.configure(bg=COLORS["bg"])
        self.resizable(False, False)
        self.transient(master)
        self.result = LoginDialog.RESULT_CANCEL

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self._build()
        self._center(master)
        self.grab_set()
        self.entry_user.focus_set()
        self.bind("<Return>", lambda e: self.do_login())

    def _center(self, master):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = master.winfo_rootx() + (master.winfo_width() - w) // 2
        y = master.winfo_rooty() + (master.winfo_height() - h) // 2
        self.geometry(f"+{max(x, 0)}+{max(y, 0)}")

    def _build(self):
        outer = tk.Frame(self, bg=COLORS["bg"], padx=36, pady=28)
        outer.pack(fill="both", expand=True)

        tk.Label(outer, text="👋 欢迎使用", font=(FONT, 18, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w")
        tk.Label(outer, text=APP_TITLE, font=(FONT, 10),
                 bg=COLORS["bg"], fg=COLORS["text_light"]).pack(anchor="w", pady=(2, 18))

        tk.Label(outer, text="用户名", font=(FONT, 10), bg=COLORS["bg"],
                 fg=COLORS["text_light"]).pack(anchor="w")
        self.entry_user = self._mk_entry(outer, textvariable=self.username_var)
        self.entry_user.pack(fill="x", pady=(4, 12), ipady=4)

        tk.Label(outer, text="密码", font=(FONT, 10), bg=COLORS["bg"],
                 fg=COLORS["text_light"]).pack(anchor="w")
        self.entry_pwd = self._mk_entry(outer, show="•", textvariable=self.password_var)
        self.entry_pwd.pack(fill="x", pady=(4, 18), ipady=4)

        btns = tk.Frame(outer, bg=COLORS["bg"])
        btns.pack(fill="x")
        self._mk_btn(btns, "登  录", self.do_login, "primary").pack(side="left", fill="x", expand=True)
        self._mk_btn(btns, "注  册", self.do_signup, "ghost").pack(side="left", padx=(10, 0), fill="x", expand=True)

        self._mk_btn(outer, "以游客身份进入", lambda: self._finish(LoginDialog.RESULT_GUEST),
                     "ghost").pack(fill="x", pady=(10, 0))

    def _mk_entry(self, parent, show=None, textvariable=None):
        return tk.Entry(parent, show=show, textvariable=textvariable, font=(FONT, 12),
                        relief="solid", bd=1,
                        highlightthickness=1,
                        highlightbackground=COLORS["border"],
                        highlightcolor=COLORS["primary"],
                        bg="white", fg=COLORS["text"])

    def _mk_btn(self, parent, text, cmd, kind="primary"):
        cfg = {
            "primary": (COLORS["primary"], "white", COLORS["primary_dark"]),
            "ghost": (COLORS["card"], COLORS["text"], COLORS["border"]),
        }[kind]
        return tk.Button(parent, text=text, command=cmd, bg=cfg[0], fg=cfg[1],
                         activebackground=cfg[2], activeforeground=cfg[1],
                         font=(FONT, 10, "bold"), relief="flat", bd=0,
                         cursor="hand2", padx=12, pady=7)

    def _finish(self, result):
        self.result = result
        self.destroy()

    def do_login(self):
        name = self.username_var.get().strip()
        pwd = self.password_var.get()
        if not name or not pwd:
            messagebox.showerror("错误", "请输入用户名和密码！", parent=self)
            return
        user_dir = os.path.join(USERFILES_DIR, name)
        pwd_file = os.path.join(user_dir, "password.txt")
        if not os.path.isdir(user_dir):
            messagebox.showerror("未知用户", f"用户名 {name} 不存在！", parent=self)
            return
        if not os.path.isfile(pwd_file):
            reset = messagebox.askyesno(
                "密码文件丢失",
                "注意：你的密码文件丢失了，需要重新设置密码，你的用户数据将会丢失。确定吗？",
                parent=self)
            if not reset:
                return
            ensure_user_dirs(name)
            new_pwd = simpledialog.askstring("新密码", "输入新密码：", parent=self, show="•")
            if not new_pwd:
                return
            with open(pwd_file, "w", encoding="utf-8") as f:
                f.write(md5_hex(new_pwd))
            messagebox.showinfo("成功", "密码已重置，请重新登录！", parent=self)
            return
        with open(pwd_file, "r", encoding="utf-8") as f:
            stored = f.read().strip()
        if md5_hex(pwd) == stored:
            self.master.login_success(name)
            self._finish(LoginDialog.RESULT_OK)
        else:
            messagebox.showerror("密码错误", "密码错误，请重试！", parent=self)

    def do_signup(self):
        name = self.username_var.get().strip()
        pwd = self.password_var.get()
        if not name or not pwd:
            messagebox.showerror("错误", "请输入用户名和密码！", parent=self)
            return
        user_dir = os.path.join(USERFILES_DIR, name)
        if os.path.isdir(user_dir):
            messagebox.showerror("用户名存在", "用户名已经存在了！", parent=self)
            return
        os.makedirs(user_dir, exist_ok=True)
        with open(os.path.join(user_dir, "password.txt"), "w", encoding="utf-8") as f:
            f.write(md5_hex(pwd))
        ensure_user_dirs(name)
        messagebox.showinfo("注册成功", "注册成功，请重新登录！", parent=self)
        self.entry_pwd.delete(0, "end")


# ============================================================
# Main App
# ============================================================
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_TITLE} V{APP_VERSION}")
        self.geometry("1150x740")
        self.minsize(980, 640)
        self.configure(bg=COLORS["bg"])

        # ---- login status（启动时为游客，登录后通过 login_success() 切换）----
        self.logged = False
        self.username = "游客"
        self.userpath = None
        self.userpath_win = None

        # ---- 各个功能的temp status ----
        self.game = {}

        self._setup_style()
        self._build_layout()
        self._register_pages()
        self.show_page("home")
        self.after(300, self.open_login)

    # --------------------------------------------------------
    # 样式&布局
    # --------------------------------------------------------
    def _setup_style(self):
        self.option_add("*Font", (FONT, 10))
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Nav.Treeview",
                        background=COLORS["sidebar"],
                        fieldbackground=COLORS["sidebar"],
                        foreground=COLORS["sidebar_text"],
                        borderwidth=0,
                        rowheight=32,
                        font=(FONT, 10))
        style.map("Nav.Treeview",
                  background=[("selected", COLORS["sidebar_sel"])],
                  foreground=[("selected", "white")])
        style.configure("TCombobox", fieldbackground="white")

    def _build_layout(self):
        # ---- side bar ----
        self.sidebar = tk.Frame(self, bg=COLORS["sidebar"], width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        logo = tk.Frame(self.sidebar, bg=COLORS["sidebar"])
        logo.pack(fill="x", pady=(22, 12))
        tk.Label(logo, text=APP_SHORT_NAME, font=(FONT, 15, "bold"),
                 bg=COLORS["sidebar"], fg="white").pack()
        tk.Label(logo, text=f"VERSION {APP_VERSION}", font=(FONT, 9),
                 bg=COLORS["sidebar"], fg="#94A3B8").pack()

        self.nav = ttk.Treeview(self.sidebar, show="tree", style="Nav.Treeview")
        self.nav.pack(fill="both", expand=True, padx=8, pady=(4, 8))
        self.nav.bind("<<TreeviewSelect>>", self._on_nav_select)

        # ---- 内容区域(右侧) ----
        right = tk.Frame(self, bg=COLORS["bg"])
        right.pack(side="left", fill="both", expand=True)

        self.content = tk.Frame(right, bg=COLORS["bg"])
        self.content.pack(fill="both", expand=True)

        self._build_statusbar(right)

    def _build_statusbar(self, parent):
        bar = tk.Frame(parent, bg=COLORS["statusbar"], height=36)
        bar.pack(fill="x", side="bottom")
        bar.pack_propagate(False)

        self.status_user = tk.Label(bar, text="👤 当前用户：游客", bg=COLORS["statusbar"],
                                    fg="#E2E8F0", font=(FONT, 9))
        self.status_user.pack(side="left", padx=14)

        self.btn_switch = tk.Button(bar, text="登录 / 切换账户", command=self.open_login,
                                    bg=COLORS["statusbar"], fg="#93C5FD",
                                    activebackground=COLORS["statusbar"],
                                    activeforeground="white", bd=0, relief="flat",
                                    cursor="hand2", font=(FONT, 9))
        self.btn_switch.pack(side="right", padx=(0, 8))

        self.btn_logout = tk.Button(bar, text="退出登录", command=self.logout,
                                    bg=COLORS["statusbar"], fg="#FCA5A5",
                                    activebackground=COLORS["statusbar"],
                                    activeforeground="white", bd=0, relief="flat",
                                    cursor="hand2", font=(FONT, 9))
        self.btn_logout.pack(side="right", padx=8)
        self.btn_logout.pack_forget()

    # --------------------------------------------------------
    # 页面注册&切换逻辑
    # --------------------------------------------------------
    #注册不同类别
    NAV_GROUPS = [
        ("首页", [("home", "  首页")]),
        ("游戏娱乐", [("guess", "  猜数字"), ("fist", "  石头剪刀布"), ("mind", "  读心术")]),
        ("数学工具", [("base", "  进制转换"), ("accuracy", "  计算正确率"),
                    ("average", "  计算平均数"), ("rabbit", "  鸡兔同笼"),
                    ("collatz", "  Collatz数列"), ("table", "  九九乘法表"),
                    ("bmi", "  BMI检测"), ("money", "  凑钱数"),
                    ("sort", "  按升/降排序数列")]),
        ("网络工具", [("translate", "  中英互译机"), ("ping", "  Ping")]),
        ("文本工具", [("morse", "  摩斯密码转换器"), ("talk", "  Talk out")]),
        ("系统工具", [("shutdown", "  定时关机"), ("batch", "  批量创建文件"),
                    ("activate", "  激活Windows"), ("bsod", "  让你的设备蓝屏"),
                    ("prank", "  恶搞")]),
        ("账户", [("account", "  账户相关")]),
        ("其他", [("feedback", "  反馈问题"), ("changelog", "  更新日志"),
                ("about", "  关于")]),
    ]

    PAGE_BUILDERS = {
        "home": "_build_home_page",
        "guess": "_build_guess_page",
        "fist": "_build_fist_page",
        "mind": "_build_mind_page",
        "base": "_build_base_page",
        "accuracy": "_build_accuracy_page",
        "average": "_build_average_page",
        "rabbit": "_build_rabbit_page",
        "collatz": "_build_collatz_page",
        "table": "_build_table_page",
        "bmi": "_build_bmi_page",
        "money": "_build_money_page",
        "sort": "_build_sort_page",
        "translate": "_build_translate_page",
        "ping": "_build_ping_page",
        "morse": "_build_morse_page",
        "talk": "_build_talk_page",
        "shutdown": "_build_shutdown_page",
        "batch": "_build_batch_page",
        "activate": "_build_activate_page",
        "bsod": "_build_bsod_page",
        "prank": "_build_prank_page",
        "account": "_build_account_page",
        "feedback": "_build_feedback_page",
        "changelog": "_build_changelog_page",
        "about": "_build_about_page",
    }

    def _register_pages(self):
        self.page_frames = {}
        self.page_builders = {}
        for pid, builder in self.PAGE_BUILDERS.items():
            self.page_builders[pid] = getattr(self, builder)
        for group, items in self.NAV_GROUPS:
            gid = self.nav.insert("", "end", text=group, open=True)
            for pid, label in items:
                self.nav.insert(gid, "end", iid=pid, text=label)

    def _on_nav_select(self, _event):
        sel = self.nav.selection()
        if sel and sel[0] in self.page_builders:
            self.show_page(sel[0])

    def show_page(self, pid):
        if pid not in self.page_frames:
            frame = tk.Frame(self.content, bg=COLORS["bg"])
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.page_builders[pid](frame)
            self.page_frames[pid] = frame
        for f in self.page_frames.values():
            f.tkraise()
        self.page_frames[pid].tkraise()

    # --------------------------------------------------------
    # global控件
    # --------------------------------------------------------
    def _card(self, parent, title, subtitle=""):
        card = tk.Frame(parent, bg=COLORS["card"],
                        highlightbackground=COLORS["border"], highlightthickness=1)
        tk.Label(card, text=title, font=(FONT, 12, "bold"),
                 bg=COLORS["card"], fg=COLORS["text"]).pack(anchor="w", padx=16, pady=(12, 2))
        if subtitle:
            tk.Label(card, text=subtitle, font=(FONT, 9),
                     bg=COLORS["card"], fg=COLORS["text_light"]).pack(anchor="w", padx=16)
        body = tk.Frame(card, bg=COLORS["card"])
        body.pack(fill="both", expand=True, padx=16, pady=(6, 14))
        return card, body

    def _header(self, parent, title, subtitle=""):
        header = tk.Frame(parent, bg=COLORS["bg"])
        header.pack(fill="x", padx=24, pady=(20, 10))
        tk.Label(header, text=title, font=(FONT, 17, "bold"),
                 bg=COLORS["bg"], fg=COLORS["text"]).pack(anchor="w")
        if subtitle:
            tk.Label(header, text=subtitle, font=(FONT, 9),
                     bg=COLORS["bg"], fg=COLORS["text_light"]).pack(anchor="w")

    def _mk_entry(self, parent, width=26, show=None, textvariable=None):
        return tk.Entry(parent, width=width, show=show, textvariable=textvariable,
                        font=(FONT, 11), relief="solid", bd=1,
                        highlightthickness=1,
                        highlightbackground=COLORS["border"],
                        highlightcolor=COLORS["primary"],
                        bg="white", fg=COLORS["text"])

    def _mk_btn(self, parent, text, cmd, kind="primary", width=None):
        cfg = {
            "primary": (COLORS["primary"], "white", COLORS["primary_dark"]),
            "success": (COLORS["success"], "white", "#15803D"),
            "danger": (COLORS["danger"], "white", "#B91C1C"),
            "warning": (COLORS["warning"], "white", "#B45309"),
            "ghost": (COLORS["card"], COLORS["text"], COLORS["border"]),
        }[kind]
        return tk.Button(parent, text=text, command=cmd, bg=cfg[0], fg=cfg[1],
                         activebackground=cfg[2], activeforeground=cfg[1],
                         font=(FONT, 10, "bold"), relief="flat", bd=0,
                         cursor="hand2", padx=14, pady=7, width=width)

    def _mk_text(self, parent, height=10, width=None, state="normal"):
        return tk.Text(parent, height=height, width=width, font=(MONO, 10),
                       bg=COLORS["console"], fg=COLORS["console_text"],
                       relief="flat", bd=0, wrap="word",
                       highlightbackground=COLORS["border"], highlightthickness=1,
                       insertbackground="white", state=state)

    def _row(self, parent, label_text, factory, *args, padx=0, **kwargs):
        """创建一行"标签 + 输入控件"。

        factory 在 row 容器内创建控件（master 直接就是 row），
        避免 pack(in_=...) 的 reparent 导致输入框消失/错位。！！！重要，警惕！！！
        返回 (row, widget)，row 可用于整行显示/隐藏。
        """
        row = tk.Frame(parent, bg=COLORS["card"])
        row.pack(fill="x", pady=4)
        if label_text:
            tk.Label(row, text=label_text, font=(FONT, 10), bg=COLORS["card"],
                     fg=COLORS["text"], width=14, anchor="w").pack(side="left")
        widget = factory(row, *args, **kwargs)
        widget.pack(side="left", padx=padx)
        return row, widget

    def _mk_spinbox(self, parent, from_, to, width=16):
        return tk.Spinbox(parent, from_=from_, to=to, font=(FONT, 11), width=width)

    @staticmethod
    def _set_text(widget, text):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", text)
        widget.configure(state="disabled")

    @staticmethod
    def _append_text(widget, text):
        widget.configure(state="normal")
        widget.insert("end", text)
        widget.see("end")
        widget.configure(state="disabled")

    # --------------------------------------------------------
    # 登录 / 账户
    # --------------------------------------------------------
    def open_login(self):
        dialog = LoginDialog(self)
        self.wait_window(dialog)

    def login_success(self, username):
        self.username = username
        self.userpath = os.path.join(USERFILES_DIR, username)
        self.userpath_win = self.userpath
        self.logged = True
        self._update_statusbar()
        if "account" in self.page_frames:
            self._rebuild_account_page()

    def logout(self):
        self.logged = False
        self.username = "游客"
        self.userpath = None
        self.userpath_win = None
        self._update_statusbar()
        if "account" in self.page_frames:
            self._rebuild_account_page()
        messagebox.showinfo("已退出", "你已退出登录，当前为游客身份。")

    def _update_statusbar(self):
        self.status_user.config(text=f"👤 当前用户：{self.username}" +
                                ("（已登录）" if self.logged else "（游客）"))
        if self.logged:
            self.btn_logout.pack(side="right", padx=8)
        else:
            self.btn_logout.pack_forget()
        # 同步更新主页上的账户状态卡片与欢迎语
        if getattr(self, "home_stat_user", None) and self.home_stat_user.winfo_exists():
            self.home_stat_user.config(
                text="已登录" if self.logged else "游客",
                fg=COLORS["success"] if self.logged else COLORS["warning"])
        if getattr(self, "home_hero_user", None) and self.home_hero_user.winfo_exists():
            self.home_hero_user.config(
                text=f"VERSION {APP_VERSION}  ·  当前用户：{self.username}")

    def _rebuild_account_page(self):
        pid = "account"
        if pid in self.page_frames:
            self.page_frames[pid].destroy()
            del self.page_frames[pid]
        if pid in self.game:
            del self.game[pid]
        self.show_page(pid)

    # --------------------------------------------------------
    # Main Page
    # --------------------------------------------------------
    def _build_home_page(self, frame):
        self._header(frame, "首页", f"欢迎使用 {APP_TITLE}")

        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        hero = tk.Frame(wrap, bg=COLORS["primary"], padx=28, pady=24)
        hero.pack(fill="x")
        tk.Label(hero, text=f"欢迎来到 {APP_TITLE}", font=(FONT, 20, "bold"),
                 bg=COLORS["primary"], fg="white").pack(anchor="w")
        self.home_hero_user = tk.Label(hero, text=f"VERSION {APP_VERSION}  ·  当前用户：{self.username}",
                 font=(FONT, 11), bg=COLORS["primary"], fg="#DBEAFE")
        self.home_hero_user.pack(anchor="w", pady=(6, 0))

        cards_row = tk.Frame(wrap, bg=COLORS["bg"])
        cards_row.pack(fill="x", pady=(16, 0))

        def stat_card(title, value, color):
            card = tk.Frame(cards_row, bg=COLORS["card"], highlightbackground=COLORS["border"],
                            highlightthickness=1)
            card.pack(side="left", fill="x", expand=True, padx=(0, 12))
            tk.Label(card, text=title, font=(FONT, 10), bg=COLORS["card"],
                     fg=COLORS["text_light"]).pack(anchor="w", padx=16, pady=(12, 2))
            val = tk.Label(card, text=value, font=(FONT, 16, "bold"), bg=COLORS["card"],
                           fg=color)
            val.pack(anchor="w", padx=16, pady=(0, 12))
            return val

        total = sum(len(items) for _, items in self.NAV_GROUPS)
        stat_card("功能总数", f"{total}", COLORS["primary"])
        self.home_stat_user = stat_card("账户状态", "已登录" if self.logged else "游客",
                                        COLORS["success"] if self.logged else COLORS["warning"])
        stat_card("数据目录", "UserFiles", COLORS["text_light"])

        card, body = self._card(wrap, "快速开始", "从左侧导航选择一个功能开始使用")
        tk.Label(body, text="·  🎯 猜数字 —— 与计算机斗智斗勇\n"
                            "·  ✊ 石头剪刀布 —— 经典对决\n"
                            "·  🌐 中英互译机 —— 在线翻译\n"
                            "·  📶 Ping —— 网络连通性测试\n"
                            "·  更多功能尽在左侧导航…",
                 font=(FONT, 10), bg=COLORS["card"], fg=COLORS["text"],
                 justify="left").pack(anchor="w")

    # --------------------------------------------------------
    # 猜数字实现
    # --------------------------------------------------------
    def _build_guess_page(self, frame):
        self._header(frame, "猜数字", "输入范围开始游戏，看看你能用多少次猜中")
        self.game["guess"] = {"target": None, "tries": 0, "min": None, "max": None,
                              "history": []}
        g = self.game["guess"]

        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        left, left_body = self._card(wrap, "游戏设置")
        left.pack(side="left", fill="y", padx=(0, 12))
        left_body.config(width=300)

        _, self.guess_min = self._row(left_body, "最小数", self._mk_entry, width=12)
        _, self.guess_max = self._row(left_body, "最大数", self._mk_entry, width=12)
        self._mk_btn(left_body, "开始新游戏", self.guess_start, "success").pack(fill="x", pady=(10, 4))
        self.guess_status = tk.Label(left_body, text="状态：等待开始", font=(FONT, 10),
                                     bg=COLORS["card"], fg=COLORS["text_light"], anchor="w")
        self.guess_status.pack(fill="x", pady=(8, 0))
        tk.Label(left_body, text="提示：输入 exit 退出本轮，输入 empty 清空历史记录",
                 font=(FONT, 9), bg=COLORS["card"], fg=COLORS["text_light"],
                 wraplength=260, justify="left").pack(anchor="w", pady=(10, 0))

        right, right_body = self._card(wrap, "猜测记录")
        right.pack(side="left", fill="both", expand=True)

        input_row = tk.Frame(right_body, bg=COLORS["card"])
        input_row.pack(fill="x", pady=(0, 8))
        self.guess_input = self._mk_entry(input_row, width=20)
        self.guess_input.pack(side="left", ipady=3)
        self._mk_btn(input_row, "猜", self.guess_submit, "primary").pack(side="left", padx=(8, 0))
        self.guess_input.bind("<Return>", lambda e: self.guess_submit())

        self.guess_log = self._mk_text(right_body, height=16)
        self.guess_log.pack(fill="both", expand=True)

    def guess_start(self):
        g = self.game["guess"]
        try:
            low = int(self.guess_min.get().strip())
            high = int(self.guess_max.get().strip())
        except ValueError:
            messagebox.showerror("数值错误", "请在左侧「最小数 / 最大数」输入框中填写整数（如 1 和 100）！")
            self.guess_min.focus_set()
            return
        if low > high:
            low, high = high, low
        g.update(target=random.randint(low, high), tries=0, min=low, max=high,
                 history=[f"新游戏：范围 {low} ~ {high}"])
        self.guess_status.config(text=f"状态：已开始，范围 {low} ~ {high}", fg=COLORS["success"])
        self._set_text(self.guess_log, f"计算机已经创建了 {low}~{high} 中的数字，开始猜吧！\n")
        self.guess_input.focus_set()

    def guess_submit(self):
        g = self.game["guess"]
        if g["target"] is None:
            messagebox.showinfo("提示", "请先点击「开始新游戏」！")
            return
        raw = self.guess_input.get().strip()
        self.guess_input.delete(0, "end")
        if raw.lower() == "exit":
            self.guess_status.config(text="状态：已退出本轮", fg=COLORS["warning"])
            self._append_text(self.guess_log, "已退出本轮。\n")
            return
        if raw.lower() == "empty":
            if not self.logged:
                messagebox.showerror("失败", "你暂未登录！此操作无效")
                return
            path = os.path.join(self.userpath, "GuessNumbers", "GuessNumbers.txt")
            with open(path, "w", encoding="utf-8") as f:
                f.write("GuessNumber FREQUENCY")
            messagebox.showinfo("成功", "清除成功！")
            return
        if not raw.isdecimal():
            messagebox.showerror("数值错误", "你输入的不是数字")
            return
        n = int(raw)
        if not (g["min"] <= n <= g["max"]):
            messagebox.showerror("超出范围", "输入的数值超出范围！")
            return
        if n == g["target"]:
            g["tries"] += 1
            self._append_text(self.guess_log, f"🎉 猜对了！数字是 {g['target']}，共用了 {g['tries']} 次。\n")
            self.guess_status.config(text=f"状态：猜中！用时 {g['tries']} 次", fg=COLORS["success"])
            if self.logged:
                try:
                    with open(os.path.join(self.userpath, "GuessNumbers", "GuessNumbers.txt"),
                              "a", encoding="utf-8") as f:
                        f.write(f"""\n错误次数：{g['tries']}
正确数字：{g['target']}
日期：{datetime.today()}
范围：{g['min']}~{g['max']}
---------""")
                except OSError as e:
                    messagebox.showerror("错误", f"写入记录失败：{e}")
            g["target"] = None
        elif n > g["target"]:
            g["tries"] += 1
            self._append_text(self.guess_log, f"第 {g['tries']} 次：{n} —— 猜大了！\n")
        else:
            g["tries"] += 1
            self._append_text(self.guess_log, f"第 {g['tries']} 次：{n} —— 猜小了！\n")

    # --------------------------------------------------------
    # 石头剪刀布实现
    # --------------------------------------------------------
    def _build_fist_page(self, frame):
        self._header(frame, "石头剪刀布", "与计算机来一场经典对决")
        self.game["fist"] = {"win": 0, "lose": 0, "tie": 0, "last": ""}
        f = self.game["fist"]

        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        arena, arena_body = self._card(wrap, "对战区")
        arena.pack(fill="x")

        self.fist_last = tk.Label(arena_body, text="点击下方按钮出拳！", font=(FONT, 13),
                                  bg=COLORS["card"], fg=COLORS["text"])
        self.fist_last.pack(pady=8)

        btn_row = tk.Frame(arena_body, bg=COLORS["card"])
        btn_row.pack(pady=10)
        for text, kind in (("✊ 石头", "danger"), ("✌️ 剪刀", "warning"), ("🖐 布", "success")):
            self._mk_btn(btn_row, text, lambda t=text.split(" ")[1]: self.fist_play(t),
                         kind).pack(side="left", padx=10, ipady=10)

        score, score_body = self._card(wrap, "计分板")
        score.pack(fill="x", pady=(14, 0))
        self.fist_score = tk.Label(score_body, text="赢：0   输：0   平局：0",
                                   font=(FONT, 14, "bold"), bg=COLORS["card"], fg=COLORS["text"])
        self.fist_score.pack(anchor="w")
        self._mk_btn(score_body, "结束并保存记录", self.fist_save, "primary").pack(anchor="w", pady=(10, 0))

    def fist_play(self, user_choice):
        f = self.game["fist"]
        comp = random.choice(["石头", "剪刀", "布"])
        if user_choice == comp:
            f["tie"] += 1
            result = "打平了，旗鼓相当。"
        elif (user_choice, comp) in (("石头", "剪刀"), ("剪刀", "布"), ("布", "石头")):
            f["win"] += 1
            result = "你赢了！牛逼！"
        else:
            f["lose"] += 1
            result = "你输了。再接再厉！"
        f["last"] = f"你出：{user_choice}    计算机出：{comp}    ——  {result}"
        self.fist_last.config(text=f["last"])
        self.fist_score.config(text=f"赢：{f['win']}   输：{f['lose']}   平局：{f['tie']}")

    def fist_save(self):
        f = self.game["fist"]
        if f["win"] == 0 and f["lose"] == 0 and f["tie"] == 0:
            messagebox.showinfo("提示", "还没有任何比赛记录。")
            return
        if f["win"] > f["lose"]:
            state = "赢"
        elif f["win"] == f["lose"]:
            state = "平局"
        else:
            state = "输"
        if self.logged:
            try:
                with open(os.path.join(self.userpath, "GuessFist", "GuessFist.txt"),
                          "a", encoding="utf-8") as file:
                    file.write(f"\n赢:{f['win']}\n输:{f['lose']}\n平局:{f['tie']}\n综合:{state}\n时间：{datetime.today()}")
                    file.write("\n----------------")
                messagebox.showinfo("已保存", "比赛记录已保存！")
            except OSError as e:
                messagebox.showerror("保存失败", f"写入失败：{e}")
        else:
            messagebox.showwarning("未保存", "你暂未登录，记录未保存。")

    # --------------------------------------------------------
    # 读心术实现
    # --------------------------------------------------------
    # 通过二进制来计算
    def _build_mind_page(self, frame):
        self._header(frame, "读心术", "想一个 1~31 的数字，让我猜出来")
        self.game["mind"] = {"step": 0, "result": 0, "pow": 1, "cards": None}

        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "数字卡片")
        card.pack(fill="both", expand=True)

        self.mind_tip = tk.Label(body, text="请你想一个 1~31 的数字，然后点击开始！",
                                 font=(FONT, 12), bg=COLORS["card"], fg=COLORS["text"])
        self.mind_tip.pack(pady=(6, 4))
        self.mind_cards = tk.Label(body, text="", font=(MONO, 13), bg=COLORS["card"],
                                   fg=COLORS["primary"], justify="left")
        self.mind_cards.pack(pady=8)

        btns = tk.Frame(body, bg=COLORS["card"])
        btns.pack(pady=12)
        self.mind_btn_yes = self._mk_btn(btns, "有我的数字 ✓", lambda: self.mind_answer(1), "success")
        self.mind_btn_yes.pack(side="left", padx=8)
        self.mind_btn_no = self._mk_btn(btns, "没有 ✗", lambda: self.mind_answer(0), "ghost")
        self.mind_btn_no.pack(side="left", padx=8)
        self._mk_btn(btns, "重新开始", self.mind_reset, "warning").pack(side="left", padx=8)

    def mind_reset(self):
        m = self.game["mind"]
        cards = []
        for i in range(1, 33):
            temp, bits = i, ["0"] * 6
            j = 0
            while temp >= 1:
                bits[j] = str(temp % 2)
                j += 1
                temp //= 2
            cards.append(bits)
        m.update(step=0, result=0, pow=1, cards=cards)
        self.mind_tip.config(text="请你想一个 1~31 的数字，然后点击「有我的数字 ✓ / 没有 ✗」回答每一组。")
        self.mind_cards.config(text="")
        self.mind_next()

    def mind_next(self):
        m = self.game["mind"]
        if m["cards"] is None:
            self.mind_reset()
            return
        j = m["step"]
        if j >= 5:
            self.mind_tip.config(text=f"🎉 你想的数是：{m['result']}！", fg=COLORS["success"])
            self.mind_cards.config(text="")
            self.mind_btn_yes.config(state="disabled")
            self.mind_btn_no.config(state="disabled")
            return
        nums = [i + 1 for i in range(32) if int(m["cards"][i][j]) == 1]
        self.mind_cards.config(text="  ".join(str(n) for n in nums))
        self.mind_tip.config(text=f"第 {j + 1} 组（共 5 组）：下面这些数字里有你想的数吗？")
        self.mind_btn_yes.config(state="normal")
        self.mind_btn_no.config(state="normal")

    def mind_answer(self, answer):
        m = self.game["mind"]
        m["result"] += m["pow"] * answer
        m["pow"] *= 2
        m["step"] += 1
        self.mind_next()

    # --------------------------------------------------------
    # 进制转换
    # --------------------------------------------------------
    def _build_base_page(self, frame):
        self._header(frame, "进制转换", "十进制与任意进制互转")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "转换器")
        card.pack(fill="x")

        self.base_mode = tk.StringVar(value="dec2bin")
        mode_row = tk.Frame(body, bg=COLORS["card"])
        mode_row.pack(anchor="w", pady=(0, 8))
        ttk.Radiobutton(mode_row, text="十进制 → 二进制", variable=self.base_mode,
                        value="dec2bin").pack(side="left", padx=(0, 16))
        ttk.Radiobutton(mode_row, text="任意进制 → 十进制", variable=self.base_mode,
                        value="any2dec").pack(side="left")

        _, self.base_num = self._row(body, "数字", self._mk_entry, width=24)

        self.base_base_row, self.base_base = self._row(body, "进制", self._mk_entry, width=8)
        self.base_base_row.pack_forget()
        self.base_base_tip = tk.Label(body, text="进制如 2、8、16（仅任意进制转十进制时填写）",
                                      font=(FONT, 9), bg=COLORS["card"], fg=COLORS["text_light"])
        self.base_base_tip.pack(anchor="w", pady=(0, 4))
        self.base_base_tip.pack_forget()

        def toggle_mode(*_):
            if self.base_mode.get() == "dec2bin":
                self.base_base_row.pack_forget()
                self.base_base_tip.pack_forget()
            else:
                self.base_base_row.pack(fill="x", pady=4)
                self.base_base_tip.pack(anchor="w", pady=(0, 4))
        self.base_mode.trace_add("write", toggle_mode)

        self._mk_btn(body, "转 换", self.base_convert, "primary").pack(anchor="w", pady=(10, 0))
        self.base_result = tk.Label(body, text="", font=(MONO, 13, "bold"),
                                    bg=COLORS["card"], fg=COLORS["primary"])
        self.base_result.pack(anchor="w", pady=(12, 0))

    def base_convert(self):
        try:
            if self.base_mode.get() == "dec2bin":
                num = int(self.base_num.get().strip())
                self.base_result.config(text=f"二进制结果：{bin(num)[2:]}")
            else:
                num = self.base_num.get().strip()
                base = int(self.base_base.get().strip())
                self.base_result.config(text=f"十进制结果：{int(num, base)}")
        except (ValueError, TypeError):
            messagebox.showerror("错误", "输入的数字或进制不合法！")

    # --------------------------------------------------------
    # 计算正确率
    # --------------------------------------------------------
    def _build_accuracy_page(self, frame):
        self._header(frame, "计算正确率", "根据题目总数与正确数计算正确率")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "正确率计算器")
        card.pack(fill="x")

        _, self.acc_total = self._row(body, "题目总数", self._mk_spinbox, from_=1, to=10 ** 9)
        _, self.acc_right = self._row(body, "正确题目数", self._mk_spinbox, from_=0, to=10 ** 9)
        self._mk_btn(body, "计 算", self.accuracy_calc, "primary").pack(anchor="w", pady=(10, 0))
        self.acc_result = tk.Label(body, text="", font=(FONT, 14, "bold"),
                                   bg=COLORS["card"], fg=COLORS["primary"])
        self.acc_result.pack(anchor="w", pady=(12, 0))

    def accuracy_calc(self):
        try:
            total = int(self.acc_total.get())
            right = int(self.acc_right.get())
            if right > total:
                raise ValueError
            rate = right / total * 100
            self.acc_result.config(text=f"正确率：{rate:.2f}%")
        except ValueError:
            messagebox.showerror("错误", "输入不合法（正确数不能大于总数）！")

    # --------------------------------------------------------
    # 计算平均数
    # --------------------------------------------------------
    def _build_average_page(self, frame):
        self._header(frame, "计算平均数", "输入一组数字并计算它们的平均数")
        self.game["average"] = {"numbers": []}

        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        left, left_body = self._card(wrap, "数字列表")
        left.pack(side="left", fill="both", expand=True, padx=(0, 12))

        input_row = tk.Frame(left_body, bg=COLORS["card"])
        input_row.pack(fill="x")
        self.avg_input = self._mk_entry(input_row, width=14)
        self.avg_input.pack(side="left", ipady=3)
        self._mk_btn(input_row, "添加", self.avg_add, "primary").pack(side="left", padx=(8, 0))
        self.avg_input.bind("<Return>", lambda e: self.avg_add())

        self.avg_list = tk.Listbox(left_body, height=12, font=(FONT, 11),
                                   bg="white", fg=COLORS["text"],
                                   highlightbackground=COLORS["border"], highlightthickness=1,
                                   selectbackground=COLORS["primary"], selectforeground="white",
                                   relief="flat")
        self.avg_list.pack(fill="both", expand=True, pady=(8, 0))

        btns = tk.Frame(left_body, bg=COLORS["card"])
        btns.pack(fill="x", pady=(8, 0))
        self._mk_btn(btns, "删除选中", self.avg_remove, "warning").pack(side="left")
        self._mk_btn(btns, "清空", self.avg_clear, "ghost").pack(side="left", padx=(8, 0))

        right, right_body = self._card(wrap, "计算")
        right.pack(side="left", fill="y")
        right_body.config(width=260)

        self.avg_delmax = tk.BooleanVar(value=True)
        ttk.Checkbutton(right_body, text="去除最大值和最小值", variable=self.avg_delmax).pack(anchor="w")
        self._mk_btn(right_body, "计 算 平 均 数", self.avg_calc, "success").pack(fill="x", pady=(12, 0))
        self.avg_result = tk.Label(right_body, text="", font=(FONT, 12, "bold"),
                                   bg=COLORS["card"], fg=COLORS["primary"], wraplength=240)
        self.avg_result.pack(anchor="w", pady=(12, 0))

    def avg_add(self):
        raw = self.avg_input.get().strip()
        self.avg_input.delete(0, "end")
        if not raw:
            return
        if raw.lower() == "exit":
            return
        if raw.isdecimal():
            self.game["average"]["numbers"].append(int(raw))
            self.avg_list.insert("end", raw)
        else:
            messagebox.showwarning("错误", "请输入整数！")

    def avg_remove(self):
        sel = self.avg_list.curselection()
        if not sel:
            return
        idx = sel[0]
        self.avg_list.delete(idx)
        del self.game["average"]["numbers"][idx]

    def avg_clear(self):
        self.game["average"]["numbers"] = []
        self.avg_list.delete(0, "end")
        self.avg_result.config(text="")

    def avg_calc(self):
        nums = self.game["average"]["numbers"]
        if not nums:
            messagebox.showerror("错误", "请先添加数字！")
            return
        values = nums[:]
        note = ""
        if self.avg_delmax.get():
            if len(values) <= 2:
                messagebox.showwarning("提示", "数字太少，无法去除最大最小值！")
                return
            for v in (max(values), min(values)):
                while v in values:
                    values.remove(v)
            note = f"（已去除最大/最小值）"
        average = sum(values) / len(values)
        self.avg_result.config(text=f"平均数：{average:.4f} {note}")

    # --------------------------------------------------------
    # 鸡兔同笼
    # --------------------------------------------------------
    def _build_rabbit_page(self, frame):
        self._header(frame, "计算鸡兔同笼问题", "根据头数与脚数求解鸡兔数量")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "求解器")
        card.pack(fill="x")

        self.rabbit_mode = tk.StringVar(value="normal")
        mode_row = tk.Frame(body, bg=COLORS["card"])
        mode_row.pack(anchor="w", pady=(0, 10))
        ttk.Radiobutton(mode_row, text="普通（鸡2条腿、兔4条腿）", variable=self.rabbit_mode,
                        value="normal").pack(side="left", padx=(0, 16))
        ttk.Radiobutton(mode_row, text="自定义（如自行车与三轮车）", variable=self.rabbit_mode,
                        value="custom").pack(side="left")

        self.rabbit_normal = tk.Frame(body, bg=COLORS["card"])
        self.rabbit_normal.pack(fill="x")
        self.rabbit_custom = tk.Frame(body, bg=COLORS["card"])

        _, self.rb_head = self._row(self.rabbit_normal, "头数", self._mk_entry, width=14)
        _, self.rb_feet = self._row(self.rabbit_normal, "脚数", self._mk_entry, width=14)

        _, self.rb_a_name = self._row(self.rabbit_custom, "a 名称", self._mk_entry, width=10)
        _, self.rb_a_feet = self._row(self.rabbit_custom, "a 脚数", self._mk_entry, width=10)
        _, self.rb_b_name = self._row(self.rabbit_custom, "b 名称", self._mk_entry, width=10)
        _, self.rb_b_feet = self._row(self.rabbit_custom, "b 脚数", self._mk_entry, width=10)
        _, self.rb_sum_head = self._row(self.rabbit_custom, "头数总和", self._mk_entry, width=10)
        _, self.rb_sum_feet = self._row(self.rabbit_custom, "脚数总和", self._mk_entry, width=10)
        self.rabbit_custom.pack_forget()

        def toggle(*_):
            if self.rabbit_mode.get() == "normal":
                self.rabbit_custom.pack_forget()
                self.rabbit_normal.pack(fill="x")
            else:
                self.rabbit_normal.pack_forget()
                self.rabbit_custom.pack(fill="x")
        self.rabbit_mode.trace_add("write", toggle)

        self._mk_btn(body, "求 解", self.rabbit_solve, "primary").pack(anchor="w", pady=(10, 0))
        self.rabbit_result = tk.Label(body, text="", font=(FONT, 13, "bold"),
                                      bg=COLORS["card"], fg=COLORS["primary"])
        self.rabbit_result.pack(anchor="w", pady=(12, 0))

    def rabbit_solve(self):
        try:
            if self.rabbit_mode.get() == "normal":
                head = int(self.rb_head.get())
                feet = int(self.rb_feet.get())
                chickens = (head * 4 - feet) / 2
                rabbits = head - chickens
                if chickens < 0 or rabbits < 0 or chickens != int(chickens):
                    raise ValueError
                self.rabbit_result.config(text=f"鸡有 {int(chickens)} 只，兔有 {int(rabbits)} 只")
            else:
                a_feet = int(self.rb_a_feet.get())
                b_feet = int(self.rb_b_feet.get())
                head = int(self.rb_sum_head.get())
                feet = int(self.rb_sum_feet.get())
                a_heads = (b_feet * head - feet) / (b_feet - a_feet)
                b_heads = head - a_heads
                if a_heads < 0 or b_heads < 0 or a_heads != int(a_heads):
                    raise ValueError
                self.rabbit_result.config(
                    text=f"{self.rb_a_name.get()} 有 {int(a_heads)} 个，"
                         f"{self.rb_b_name.get()} 有 {int(b_heads)} 个")
        except (ValueError, ZeroDivisionError):
            messagebox.showerror("错误！", "输入不合法或该问题无解。")

    # --------------------------------------------------------
    # Collatz 数列
    # --------------------------------------------------------
    def _build_collatz_page(self, frame):
        self._header(frame, "Collatz 数列", "输入一个正整数，观察 Collatz 猜想数列")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "计算")
        card.pack(fill="x")
        row = tk.Frame(body, bg=COLORS["card"])
        row.pack(fill="x")
        self.collatz_input = self._mk_entry(row, width=16)
        self.collatz_input.pack(side="left", ipady=3)
        self._mk_btn(row, "开 始", self.collatz_run, "primary").pack(side="left", padx=(8, 0))
        self.collatz_input.bind("<Return>", lambda e: self.collatz_run())

        log, log_body = self._card(wrap, "输出")
        log.pack(fill="both", expand=True, pady=(14, 0))
        self.collatz_log = self._mk_text(log_body, height=14)
        self.collatz_log.pack(fill="both", expand=True)

    def collatz_run(self):
        try:
            num = int(self.collatz_input.get().strip())
            if num < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "请输入正整数！")
            return
        steps, cur = [num], num
        guard = 0
        while cur != 1 and guard < 100000:
            cur = cur // 2 if cur % 2 == 0 else 3 * cur + 1
            steps.append(cur)
            guard += 1
        self._set_text(self.collatz_log,
                       "----- 计算开始 -----\n" +
                       "  ".join(str(s) for s in steps[:60]) +
                       ("\n...（步数过多，仅显示前 60 项）" if len(steps) > 60 else "") +
                       f"\n\n----- 计算结束，共 {len(steps)} 项 -----")

    # --------------------------------------------------------
    # 九九乘法表(控制台输出，实际上print to文本框)
    # --------------------------------------------------------
    def _build_table_page(self, frame):
        self._header(frame, "九九乘法表", "一键生成九九乘法表")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "生成")
        card.pack(fill="x")
        self._mk_btn(body, "生成九九乘法表", self.table_run, "primary").pack(anchor="w")

        log, log_body = self._card(wrap, "输出")
        log.pack(fill="both", expand=True, pady=(14, 0))
        self.table_log = self._mk_text(log_body, height=16)
        self.table_log.pack(fill="both", expand=True)

    def table_run(self):
        lines = []
        for i in range(1, 10):
            lines.append("   ".join(f"{j}x{i}={i * j}" for j in range(1, i + 1)))
        self._set_text(self.table_log, "\n".join(lines))

    # --------------------------------------------------------
    # BMI 检测
    # --------------------------------------------------------
    def _build_bmi_page(self, frame):
        self._header(frame, "BMI 检测", "输入身高体重，检测你的体型")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "数据输入")
        card.pack(fill="x")

        _, self.bmi_high = self._row(body, "身高 (m)", self._mk_entry, width=14)
        _, self.bmi_weight = self._row(body, "体重 (kg)", self._mk_entry, width=14)
        self._mk_btn(body, "计 算", self.bmi_calc, "primary").pack(anchor="w", pady=(10, 0))

        self.bmi_result = tk.Label(body, text="", font=(FONT, 14, "bold"),
                                   bg=COLORS["card"], fg=COLORS["primary"])
        self.bmi_result.pack(anchor="w", pady=(14, 0))

    def bmi_calc(self):
        try:
            high = float(self.bmi_high.get())
            weight = float(self.bmi_weight.get())
            if not (0.1 <= high <= 2.0 and 2.5 <= weight <= 640.0):
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "请输入合法数值！")
            return
        bmi = weight / (high ** 2)
        if bmi <= 18.4:
            tip, color = "温馨提示：你的体型偏瘦，要注意营养哦~", COLORS["warning"]
        elif bmi <= 23.9:
            tip, color = "温馨提示：标准体型，继续保持哦~", COLORS["success"]
        elif bmi <= 27.9:
            tip, color = "温馨提示：你的体型过胖，要注意身体哦~", COLORS["warning"]
        else:
            tip, color = "温馨提示：你的体型肥胖，要注意饮食哦~", COLORS["danger"]
        self.bmi_result.config(text=f"你的 BMI 值：{bmi:.2f}\n{tip}", fg=color)
        if self.logged:
            try:
                with open(os.path.join(self.userpath, "BMI", "BMI Log.log"),
                          "a", encoding="utf-8") as f:
                    f.write(f"""\n时间:{datetime.today()}
你的身高：{high}m
你的体重：{weight}kg
BMI:{bmi:.2f}
{tip}
---------""")
            except OSError:
                pass

    # --------------------------------------------------------
    # 凑钱数实现
    # --------------------------------------------------------
    def _build_money_page(self, frame):
        self._header(frame, "凑钱数", "计算用 1、2、5 元凑成指定钱数有几种可能")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "计算")
        card.pack(fill="x")
        row = tk.Frame(body, bg=COLORS["card"])
        row.pack(fill="x")
        self.money_input = self._mk_entry(row, width=14)
        self.money_input.pack(side="left", ipady=3)
        self._mk_btn(row, "计 算", self.money_calc, "primary").pack(side="left", padx=(8, 0))
        self.money_input.bind("<Return>", lambda e: self.money_calc())
        self.money_result = tk.Label(body, text="", font=(FONT, 13, "bold"),
                                     bg=COLORS["card"], fg=COLORS["primary"])
        self.money_result.pack(anchor="w", pady=(12, 0))

    def money_calc(self):
        try:
            total = int(self.money_input.get())
            if total < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "请输入正整数！")
            return
        # 数学解法：对每个 5 元张数 f，2 元张数 t 从 0 到 (n-5f)//2，1 元张数唯一确定
        count = sum((total - 5 * f) // 2 + 1 for f in range(total // 5 + 1))
        self.money_result.config(text=f"共有 {count} 种凑法（1元、2元、5元）")

    # --------------------------------------------------------
    # 排列实现
    # --------------------------------------------------------
    def _build_sort_page(self, frame):
        self._header(frame, "按升/降排序数列", "输入用空格分隔的数列进行排序")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "排序")
        card.pack(fill="x")

        self.sort_mode = tk.StringVar(value="asc")
        mode_row = tk.Frame(body, bg=COLORS["card"])
        mode_row.pack(anchor="w", pady=(0, 8))
        ttk.Radiobutton(mode_row, text="升序", variable=self.sort_mode, value="asc").pack(side="left", padx=(0, 16))
        ttk.Radiobutton(mode_row, text="降序", variable=self.sort_mode, value="desc").pack(side="left")

        _, self.sort_input = self._row(body, "数列", self._mk_entry, width=40)
        self._mk_btn(body, "排 序", self.sort_run, "primary").pack(anchor="w", pady=(10, 0))
        self.sort_result = tk.Label(body, text="", font=(MONO, 12, "bold"),
                                    bg=COLORS["card"], fg=COLORS["primary"])
        self.sort_result.pack(anchor="w", pady=(12, 0))

    def sort_run(self):
        try:
            nums = [int(x) for x in self.sort_input.get().strip().split()]
            if not nums:
                raise ValueError
        except ValueError:
            messagebox.showerror("错误", "你输入的数列有些不是数字！")
            return
        nums.sort(reverse=(self.sort_mode.get() == "desc"))
        self.sort_result.config(text=f"排序结果：{nums}")

    # --------------------------------------------------------
    # translate 翻译实现
    # --------------------------------------------------------
    def _build_translate_page(self, frame):
        self._header(frame, "中英互译机", "支持中英文互译（在线服务）")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "翻译")
        card.pack(fill="x")

        self.translate_input = self._mk_text(body, height=4, width=60)
        self.translate_input.pack(fill="x", pady=(0, 8))
        self._mk_btn(body, "翻 译", self.translate_do, "primary").pack(anchor="w")

        result, result_body = self._card(wrap, "翻译结果")
        result.pack(fill="both", expand=True, pady=(14, 0))
        self.translate_output = self._mk_text(result_body, height=8)
        self.translate_output.pack(fill="both", expand=True)

    def translate_do(self):
        if requests is None:
            messagebox.showerror("错误", "未安装 requests 库，请运行：pip install requests")
            return
        text = self.translate_input.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("提示", "请输入要翻译的内容！")
            return
        self._set_text(self.translate_output, "翻译中...\n")

        def worker():
            try:
                target = "en" if has_chinese(text) else "zh-CN"
                url = "https://translate.googleapis.com/translate_a/single"
                params = {"client": "gtx", "sl": "auto", "tl": target, "dt": "t", "q": text}
                r = requests.get(url, params=params, timeout=10)
                data = r.json()
                result = "".join(seg[0] for seg in data[0] if seg and seg[0])
                self.after(0, lambda: self._set_text(self.translate_output, result or "(无结果)"))
            except Exception:
                self.after(0, lambda: self._set_text(self.translate_output, "翻译失败：网络异常或服务不可用。"))

        threading.Thread(target=worker, daemon=True).start()

    # --------------------------------------------------------
    # Ping
    # --------------------------------------------------------
    def _build_ping_page(self, frame):
        self._header(frame, "Ping", "网络连通性测试")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "测试")
        card.pack(fill="x")

        self.ping_mode = tk.StringVar(value="system")
        mode_row = tk.Frame(body, bg=COLORS["card"])
        mode_row.pack(anchor="w", pady=(0, 8))
        ttk.Radiobutton(mode_row, text="系统 Ping（Windows）", variable=self.ping_mode,
                        value="system").pack(side="left", padx=(0, 16))
        ttk.Radiobutton(mode_row, text="Python Ping", variable=self.ping_mode,
                        value="python").pack(side="left")

        row = tk.Frame(body, bg=COLORS["card"])
        row.pack(fill="x")
        self.ping_input = self._mk_entry(row, width=28)
        self.ping_input.pack(side="left", ipady=3)
        self._mk_btn(row, "Ping", self.ping_do, "primary").pack(side="left", padx=(8, 0))
        self.ping_input.bind("<Return>", lambda e: self.ping_do())

        log, log_body = self._card(wrap, "输出")
        log.pack(fill="both", expand=True, pady=(14, 0))
        self.ping_log = self._mk_text(log_body, height=14)
        self.ping_log.pack(fill="both", expand=True)

    def ping_do(self):
        host = self.ping_input.get().strip()
        if not host:
            messagebox.showwarning("提示", "请输入网址！")
            return
        mode = self.ping_mode.get()
        self._set_text(self.ping_log, f"正在 Ping {host}...\n")
        threading.Thread(target=self._ping_worker, args=(host, mode), daemon=True).start()

    def _ping_worker(self, host, mode):
        if mode == "system":
            if sys.platform != "win32":
                out = "系统 Ping 仅支持 Windows！"
            else:
                try:
                    proc = subprocess.run(["ping", host], capture_output=True, text=True,
                                          encoding="gbk", errors="ignore", timeout=30)
                    out = proc.stdout + proc.stderr
                except Exception as e:
                    out = f"Ping 失败：{e}"
        else:
            if py_ping is None:
                out = "未安装 pythonping，请运行：pip install pythonping"
            else:
                try:
                    out = str(py_ping(host))
                except Exception as e:
                    out = f"Ping 失败：{e}"
        out = out + "\n（结束）"
        self.after(0, lambda: self._set_text(self.ping_log, out))

    # --------------------------------------------------------
    # Morse Code Transfer
    # --------------------------------------------------------
    def _build_morse_page(self, frame):
        self._header(frame, "摩斯密码转换器", "将小写字母转换为摩斯密码")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "转换")
        card.pack(fill="x")

        row = tk.Frame(body, bg=COLORS["card"])
        row.pack(fill="x")
        self.morse_input = self._mk_entry(row, width=28)
        self.morse_input.pack(side="left", ipady=3)
        self._mk_btn(row, "转 换", self.morse_do, "primary").pack(side="left", padx=(8, 0))
        self.morse_input.bind("<Return>", lambda e: self.morse_do())

        self.morse_result = tk.Label(body, text="", font=(MONO, 13, "bold"),
                                     bg=COLORS["card"], fg=COLORS["primary"], wraplength=700,
                                     justify="left")
        self.morse_result.pack(anchor="w", pady=(12, 0))
        tk.Label(body, text="只能输入小写字母，否则将不返回大写字母、特殊符号。",
                 font=(FONT, 9), bg=COLORS["card"], fg=COLORS["text_light"]).pack(anchor="w")

    def morse_do(self):
        text = self.morse_input.get().strip()
        parts = []
        for ch in text:
            if ch in MORSE_CODES:
                parts.append(MORSE_CODES[ch])
        self.morse_result.config(text="   ".join(parts) if parts else "(没有可转换的字符)")

    # --------------------------------------------------------
    # Say anything...
    # --------------------------------------------------------
    def _build_talk_page(self, frame):
        self._header(frame, "Talk out", "输入 EXIT 退出 · CLEAN 清屏 · HELP 帮助")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "聊天")
        card.pack(fill="both", expand=True)

        self.talk_log = self._mk_text(body, height=16)
        self.talk_log.pack(fill="both", expand=True)
        self._set_text(self.talk_log,
                       "Talk out\n---------\nIf you are happy, you can enter \"EXIT\" to exit.\n"
                       "Enter \"CLEAN\" to clean the enter area.\nEnter \"HELP\" to print the help words.\n\n")

        row = tk.Frame(body, bg=COLORS["card"])
        row.pack(fill="x", pady=(8, 0))
        self.talk_input = self._mk_entry(row, width=40)
        self.talk_input.pack(side="left", ipady=3)
        self._mk_btn(row, "发送", self.talk_send, "primary").pack(side="left", padx=(8, 0))
        self.talk_input.bind("<Return>", lambda e: self.talk_send())

    def talk_send(self):
        line = self.talk_input.get()
        self.talk_input.delete(0, "end")
        if not line:
            return
        if line == "EXIT":
            self._append_text(self.talk_log, "（已退出 Talk out）\n")
        elif line == "CLEAN":
            self._set_text(self.talk_log, "")
        elif line == "HELP":
            self._append_text(self.talk_log,
                              "If you are happy, you can enter \"EXIT\" to exit.\n"
                              "Enter \"CLEAN\" to clean the enter area.\n"
                              "Enter \"HELP\" to print the help words.\n")
        else:
            self._append_text(self.talk_log, f"你说：{line}\n")

    # --------------------------------------------------------
    # 定时关机
    # --------------------------------------------------------
    def _build_shutdown_page(self, frame):
        self._header(frame, "定时关机", "设置或取消系统关机计划")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "操作")
        card.pack(fill="x")

        self.shutdown_mode = tk.StringVar(value="local")
        mode_row = tk.Frame(body, bg=COLORS["card"])
        mode_row.pack(anchor="w", pady=(0, 8))
        ttk.Radiobutton(mode_row, text="当前计算机定时关机", variable=self.shutdown_mode,
                        value="local").pack(side="left", padx=(0, 12))
        ttk.Radiobutton(mode_row, text="远程关机（局域网）", variable=self.shutdown_mode,
                        value="remote").pack(side="left", padx=(0, 12))
        ttk.Radiobutton(mode_row, text="取消关机计划", variable=self.shutdown_mode,
                        value="cancel").pack(side="left")

        self.shutdown_opts = tk.Frame(body, bg=COLORS["card"])
        self.shutdown_opts.pack(fill="x", pady=(4, 0))
        self.sd_row_seconds, self.sd_seconds = self._row(self.shutdown_opts, "秒数", self._mk_entry, width=10)
        self.sd_row_ip, self.sd_ip = self._row(self.shutdown_opts, "IP 地址", self._mk_entry, width=16)
        self.sd_row_ip.pack_forget()

        def toggle(*_):
            mode = self.shutdown_mode.get()
            if mode == "remote":
                self.sd_row_seconds.pack(fill="x", pady=4)
                self.sd_row_ip.pack(fill="x", pady=4)
            elif mode == "local":
                self.sd_row_seconds.pack(fill="x", pady=4)
                self.sd_row_ip.pack_forget()
            else:
                self.sd_row_seconds.pack_forget()
                self.sd_row_ip.pack_forget()
        self.shutdown_mode.trace_add("write", toggle)

        self._mk_btn(body, "执 行", self.shutdown_do, "primary").pack(anchor="w", pady=(10, 0))

    def shutdown_do(self):
        mode = self.shutdown_mode.get()
        if mode == "cancel":
            subprocess.run(["shutdown", "-a"], capture_output=True)
            messagebox.showinfo("成功", "已取消当前计算机上的关机计划。")
            return
        try:
            seconds = int(self.sd_seconds.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的秒数！")
            return
        if mode == "local":
            if seconds < 5:
                messagebox.showerror("错误", "秒数不能小于 5！")
                return
            if not messagebox.askyesno("确认", f"确认 {seconds} 秒后关闭当前计算机？"):
                return
            subprocess.run(["shutdown", "-s", "-t", str(seconds)], capture_output=True)
            messagebox.showinfo("成功", f"已设置 {seconds} 秒后关机，可随时回来取消。")
        elif mode == "remote":
            ip = self.sd_ip.get().strip()
            if not ip:
                messagebox.showerror("错误", "请输入 IP 地址！")
                return
            if not messagebox.askyesno("确认", f"确认 {seconds} 秒后远程关闭 {ip}？"):
                return
            subprocess.run(["shutdown", "-s", "-t", str(seconds), "-m", f"\\\\{ip}"],
                           capture_output=True)
            messagebox.showinfo("成功", "远程关机指令已发送。")

    # --------------------------------------------------------
    # 批量创建文件
    # --------------------------------------------------------
    def _build_batch_page(self, frame):
        self._header(frame, "批量创建文件", "按序列快速批量创建空文件")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "设置")
        card.pack(fill="x")

        self.batch_type = self._mk_entry(body, width=10)
        self.batch_quantity = self._mk_entry(body, width=10)
        self.batch_name = self._mk_entry(body, width=24)
        self._row(body, "文件类型", self.batch_type)
        self._row(body, "文件数量", self.batch_quantity)
        self._row(body, "文件前缀名", self.batch_name)

        path_row = tk.Frame(body, bg=COLORS["card"])
        path_row.pack(fill="x", pady=4)
        tk.Label(path_row, text="目标路径", font=(FONT, 10), bg=COLORS["card"],
                 fg=COLORS["text"], width=14, anchor="w").pack(side="left")
        self.batch_path = self._mk_entry(path_row, width=36)
        self.batch_path.pack(side="left")
        self._mk_btn(path_row, "浏览…", self.batch_browse, "ghost").pack(side="left", padx=(8, 0))

        self._mk_btn(body, "开始创建", self.batch_do, "primary").pack(anchor="w", pady=(10, 0))
        self.batch_result = tk.Label(body, text="", font=(FONT, 11),
                                     bg=COLORS["card"], fg=COLORS["success"])
        self.batch_result.pack(anchor="w", pady=(10, 0))

    def batch_browse(self):
        path = filedialog.askdirectory(title="选择创建位置")
        if path:
            self.batch_path.delete(0, "end")
            self.batch_path.insert(0, path)

    def batch_do(self):
        ftype = self.batch_type.get().strip()
        quantity = self.batch_quantity.get().strip()
        name = self.batch_name.get().strip()
        path = self.batch_path.get().strip()
        if not all((ftype, quantity, name, path)):
            messagebox.showerror("错误", "请填写完整的设置！")
            return
        if not os.path.isdir(path):
            messagebox.showerror("错误", "目标路径不存在！")
            return
        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("错误", "数量必须是整数！")
            return
        created = 0
        for num in range(1, quantity + 1):
            filename = os.path.join(path, f"{name}{num}.{ftype}")
            try:
                with open(filename, "w", encoding="utf-8"):
                    pass
                created += 1
            except OSError as e:
                messagebox.showerror("错误", f"创建 {filename} 失败：{e}")
                break
        self.batch_result.config(text=f"成功创建 {created} 个文件 → {path}")

    # --------------------------------------------------------
    # 激活 Windows
    # --------------------------------------------------------
    def _build_activate_page(self, frame):
        self._header(frame, "激活 Windows", "需要管理员权限")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "注意事项",
                                "按下按钮后几秒钟会弹出一个窗口：\n"
                                "1 - 永久激活当前版本Windows   2 - 把Windows激活到2038年\n"
                                "3 - 把Windows和Office激活到180天后")
        card.pack(fill="x")
        self._mk_btn(body, "打开 ActiveScript.bat", self.activate_do, "warning").pack(anchor="w")

    def activate_do(self):
        bat = os.path.join(BASE_DIR, "ActiveScript.bat")
        if not os.path.isfile(bat):
            messagebox.showerror("找不到文件", "未找到 ActiveScript.bat！")
            return
        subprocess.Popen(["cmd", "/c", "start", "", bat], cwd=BASE_DIR)
        messagebox.showinfo("已启动", "已在新窗口中打开激活脚本。")

    # --------------------------------------------------------
    # 让你的设备蓝屏（危险功能，双重确认）
    # --------------------------------------------------------
    def _build_bsod_page(self, frame):
        self._header(frame, "让你的设备蓝屏", "危险功能 · 仅限 Windows")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "警告",
                                "这可不是开玩笑，此功能真的会让 Windows 蓝屏！\n"
                                "Windows 11 加了保护措施，可能无法触发蓝屏。\n"
                                "使用前请务必保存所有工作！")
        card.pack(fill="x")
        self._mk_btn(body, "触发蓝屏（危险）", self.bsod_do, "danger").pack(anchor="w")

    def bsod_do(self):
        if sys.platform != "win32":
            messagebox.showerror("错误", "此功能仅支持 Windows！")
            return
        if not messagebox.askyesno("再次确认", "⚠️ 真的要继续吗？系统将蓝屏并可能需要重启！"):
            return
        token = simpledialog.askstring("验证", "如需继续，请输入 yes（输入其他内容取消）：")
        if token != "yes":
            return
        for count in (3, 2, 1):
            messagebox.showinfo("倒计时", f"{count} 秒后触发……")
        subprocess.Popen(["powershell.exe", "wininit"])
        messagebox.showinfo("已执行", "指令已执行。如果系统没有反应，说明此系统无法通过该方式触发蓝屏。")

    # --------------------------------------------------------
    # 恶搞（危险功能，双重确认）
    # --------------------------------------------------------
    def _build_prank_page(self, frame):
        self._header(frame, "恶搞", "危险功能 · 会关闭资源管理器并计划关机")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "警告",
                                "该功能会：\n"
                                "1. 强制结束 explorer.exe（桌面和任务栏会消失）\n"
                                "2. 计划 60 秒后关机\n"
                                "可通过本页的「恢复」按钮输入密码解除。\n"
                                "请务必先保存所有工作！")
        card.pack(fill="x")

        btns = tk.Frame(body, bg=COLORS["card"])
        btns.pack(anchor="w")
        self._mk_btn(btns, "触发恶搞（危险）", self.prank_do, "danger").pack(side="left")
        self._mk_btn(btns, "恢复（输入密码）", self.prank_restore, "success").pack(side="left", padx=(10, 0))

    def prank_do(self):
        if sys.platform != "win32":
            messagebox.showerror("错误", "此功能仅支持 Windows！")
            return
        if not messagebox.askyesno("再次确认", "⚠️ 真的要继续吗？桌面会消失且 60 秒后关机！"):
            return
        token = simpledialog.askstring("验证", "如需继续，请输入 yes：")
        if token != "yes":
            return
        subprocess.run(["taskkill", "-im", "explorer.exe", "-f"], capture_output=True)
        subprocess.run(["shutdown", "-s", "-t", "60",
                        "-c", "你的电脑将会在60秒后关机！"], capture_output=True)
        messagebox.showwarning("已触发", "恶搞已触发！请在本页点击「恢复」输入密码解除。")

    def prank_restore(self):
        pwd = simpledialog.askstring("Password", "快输密码！", show="•")
        if pwd == "Twb20020303!":
            subprocess.run(["shutdown", "-a"], capture_output=True)
            subprocess.Popen(["explorer.exe"])
            messagebox.showinfo("已恢复", "关机已取消，资源管理器已重新启动。")
        else:
            messagebox.showerror("错误", "密码错误！")

    # --------------------------------------------------------
    # 账户相关
    # --------------------------------------------------------
    def _build_account_page(self, frame):
        self._header(frame, "账户相关", "管理你的账户与数据")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        if not self.logged:
            card, body = self._card(wrap, "未登录",
                                    "你当前是游客身份，登录后可保存游戏记录与 BMI 日志。")
            card.pack(fill="x")
            self._mk_btn(body, "登录 / 注册", self.open_login, "primary").pack(anchor="w")
            return

        info, info_body = self._card(wrap, f"当前用户：{self.username}")
        info.pack(fill="x")
        tk.Label(info_body, text=f"数据目录：{self.userpath}", font=(FONT, 9),
                 bg=COLORS["card"], fg=COLORS["text_light"]).pack(anchor="w")

        actions, actions_body = self._card(wrap, "账户操作")
        actions.pack(fill="x", pady=(14, 0))

        def action_row(text, cmd, kind="ghost"):
            self._mk_btn(actions_body, text, cmd, kind).pack(anchor="w", pady=3, fill="x")

        action_row("修改密码", self.acc_change_password)
        action_row("更改用户名", self.acc_change_username)
        action_row("初始化账户（重置数据）", self.acc_init, "warning")
        action_row("注销账户（删除所有数据）", self.acc_delete, "danger")
        action_row("退出登录", self.logout)

    def _verify_password(self) -> bool:
        """要求输入当前密码进行验证，成功返回 True"""
        pwd = simpledialog.askstring("验证", "输入当前账户的密码：", show="•")
        if pwd is None:
            return False
        pwd_file = os.path.join(self.userpath, "password.txt")
        if os.path.isfile(pwd_file):
            with open(pwd_file, "r", encoding="utf-8") as f:
                if md5_hex(pwd) == f.read().strip():
                    return True
        messagebox.showerror("密码错误", "密码错误，请重试！")
        return False

    def acc_change_password(self):
        if not self._verify_password():
            return
        new_pwd = simpledialog.askstring("新密码", "输入新密码：", show="•")
        if not new_pwd:
            return
        with open(os.path.join(self.userpath, "password.txt"), "w", encoding="utf-8") as f:
            f.write(md5_hex(new_pwd))
        messagebox.showinfo("成功", "密码已更改，请重新登录！")
        self.logout()

    def acc_change_username(self):
        if not self._verify_password():
            return
        new_name = simpledialog.askstring("更改用户名", "输入你的新用户名：")
        if not new_name or not new_name.strip():
            return
        new_name = new_name.strip()
        new_path = os.path.join(USERFILES_DIR, new_name)
        if os.path.isdir(new_path):
            messagebox.showerror("错误", "该用户名已存在！")
            return
        try:
            os.rename(self.userpath, new_path)
        except OSError as e:
            messagebox.showerror("失败", f"重命名失败：{e}")
            return
        self.login_success(new_name)
        messagebox.showinfo("成功", f"用户名已更改为 {new_name}！")

    def acc_init(self):
        if not self._verify_password():
            return
        if not messagebox.askyesno("确认", "将重置你的用户数据（游戏记录、BMI 日志等）！继续？"):
            return
        ensure_user_dirs(self.username)
        messagebox.showinfo("成功", "你的用户数据已被重置。")

    def acc_delete(self):
        if not self._verify_password():
            return
        if not messagebox.askyesno("真的吗？", "注销后所有用户数据将被永久删除！"):
            return
        try:
            shutil.rmtree(self.userpath)
        except OSError as e:
            messagebox.showerror("失败", f"注销失败：{e}")
            return
        messagebox.showwarning("", "账户已经注销，请重新登录！")
        self.logged = False
        self.username = "游客"
        self.userpath = self.userpath_win = None
        self._update_statusbar()
        self._rebuild_account_page()
        self.open_login()

    # --------------------------------------------------------
    # 反馈问题
    # --------------------------------------------------------
    def _build_feedback_page(self, frame):
        self._header(frame, "反馈问题", "如果你有建议或问题，欢迎联系作者")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "联系方式")
        card.pack(fill="x")
        tk.Label(body, text="邮箱1：atwbmail@163.com\n邮箱2：superselfus@gmail.com\n"
                            f"GitHub：github.com/Hydrooxzgen/",
                 font=(FONT, 11), bg=COLORS["card"], fg=COLORS["text"],
                 justify="left").pack(anchor="w")
        tk.Label(body, text=f"感谢支持\n—— {APP_AUTHOR}, 2026/08/16",
                 font=(FONT, 9), bg=COLORS["card"], fg=COLORS["text_light"]).pack(anchor="w", pady=(10, 0))

    # --------------------------------------------------------
    # 更新日志
    # --------------------------------------------------------
    def _build_changelog_page(self, frame):
        self._header(frame, "更新日志", "查看历史更新记录")
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "Log")
        card.pack(fill="both", expand=True)
        self.changelog_log = self._mk_text(body, height=18)
        self.changelog_log.pack(fill="both", expand=True)

        log_path = os.path.join(BASE_DIR, "Update_Log.log")
        if os.path.isfile(log_path):
            try:
                with open(log_path, "r", encoding="utf-8") as f:
                    self._set_text(self.changelog_log, f.read())
            except OSError as e:
                self._set_text(self.changelog_log, f"读取失败：{e}")
        else:
            self._set_text(self.changelog_log,
                           "无法找到 Update_Log.log 文件。\n"
                           f"你可以访问 GitHub：github.com/Hydrooxzgen/Projects\n"
                           "下载 Update_Log.log 并放在 App.py 的目录下。")

    # --------------------------------------------------------
    # 关于
    # --------------------------------------------------------
    def _build_about_page(self, frame):
        self._header(frame, "关于", APP_TITLE)
        wrap = tk.Frame(frame, bg=COLORS["bg"])
        wrap.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        card, body = self._card(wrap, "版本信息")
        card.pack(fill="x")
        tk.Label(body, text=APP_TITLE, font=(FONT, 20, "bold"),
                 bg=COLORS["card"], fg=COLORS["primary"]).pack(anchor="w")
        tk.Label(body, text=f"VERSION {APP_VERSION}(New GUI)", font=(FONT, 11),
                 bg=COLORS["card"], fg=COLORS["text_light"]).pack(anchor="w", pady=(4, 0))
        tk.Label(body, text=f"当前用户：{self.username}\n"
                            f"Python：{sys.version.split()[0]}\n"
                            f"运行目录：{BASE_DIR}",
                 font=(FONT, 10), bg=COLORS["card"], fg=COLORS["text"],
                 justify="left").pack(anchor="w", pady=(12, 0))
        tk.Label(body, text=f"作者：{APP_AUTHOR}", font=(FONT, 9),
                 bg=COLORS["card"], fg=COLORS["text_light"]).pack(anchor="w", pady=(10, 0))


if __name__ == "__main__":
    if sys.version_info.major != 3:
        print("Not Support Python 2!")
        sys.exit(1)
    os.makedirs(USERFILES_DIR, exist_ok=True)
    app = App()
    app.mainloop()
# Author: Hydrooxygen
