# -*- coding: utf-8 -*-
"""【重建管线 · 第 1 步】一键重建 App.py（多语言切换版）。

用途：从单语言版 AppGUI_CHS.py 生成多语言版 App.py。
步骤：
  1. 复制 AppGUI_CHS.py 干净源码
  2. 注入 i18n 基础设施（import json + 语言加载 + tr()）
  3. NAV_GROUPS 类属性 -> _nav_groups() 方法（支持运行时切换语言）
  4. 用 tokenize 安全替换中文字符串为 tr('...')（含隐式拼接合并）
  5. 修复 batch 页 _row bug、APP_VERSION 去 tr()、注入语言切换 UI

用法：python dev/_rebuild.py
输入：AppGUI_CHS.py       输出：App.py
依赖：需先运行本脚本，再运行 _fstring_convert.py
"""
import ast
import io
import os
import token
import tokenize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "AppGUI_CHS.py")
DST = os.path.join(ROOT, "App.py")

I18N_BLOCK = '''
# ==================== 多语言支持（i18n） ====================
LANG_DIR = os.path.join(BASE_DIR, "lang")
_CURRENT_LANG = "zh_CN"          # 当前语言（zh_CN / en_US ...）
_LANG_DICT = {}                  # 当前语言的翻译字典 {中文原文: 翻译}

# 支持的语言（文件位于 lang/{code}.json）
# 注意：放在 tr() 定义之后，因为显示名也参与翻译

def _load_lang(lang):
    """加载 lang/{lang}.json 到 _LANG_DICT；失败时回退为空字典（保持原文）。"""
    global _CURRENT_LANG, _LANG_DICT
    _CURRENT_LANG = lang
    _LANG_DICT = {}
    path = os.path.join(LANG_DIR, lang + ".json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            _LANG_DICT = data
    except Exception:
        _LANG_DICT = {}
    return _LANG_DICT


def tr(key, *args, **kwargs):
    """翻译：查 _LANG_DICT[key]；找不到则返回原文。
    支持格式占位符：tr('欢迎 {name}！', name='Tom') 或 tr('共 {} 项', 5)
    """
    text = _LANG_DICT.get(key, key)
    if args or kwargs:
        try:
            return text.format(*args, **kwargs)
        except (IndexError, KeyError, ValueError):
            return text
    return text


LANGUAGES = {
    "zh_CN": tr("中文"),
    "zh_TW": "繁體中文",
    "en_US": "English",
}


# 首次加载默认语言
_load_lang(_CURRENT_LANG)
'''

OLD_NAV = '''    # --------------------------------------------------------
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
    ]'''

NEW_NAV = '''    # --------------------------------------------------------
    # 页面注册&切换逻辑
    # --------------------------------------------------------
    # 导航树（多语言：切换语言后重建）
    def _nav_groups(self):
        return [
            (tr("首页"), [("home", tr("  首页"))]),
            (tr("游戏娱乐"), [("guess", tr("  猜数字")), ("fist", tr("  石头剪刀布")), ("mind", tr("  读心术"))]),
            (tr("数学工具"), [("base", tr("  进制转换")), ("accuracy", tr("  计算正确率")),
                        ("average", tr("  计算平均数")), ("rabbit", tr("  鸡兔同笼")),
                        ("collatz", tr("  Collatz数列")), ("table", tr("  九九乘法表")),
                        ("bmi", tr("  BMI检测")), ("money", tr("  凑钱数")),
                        ("sort", tr("  按升/降排序数列"))]),
            (tr("网络工具"), [("translate", tr("  中英互译机")), ("ping", tr("  Ping"))]),
            (tr("文本工具"), [("morse", tr("  摩斯密码转换器")), ("talk", tr("  Talk out"))]),
            (tr("系统工具"), [("shutdown", tr("  定时关机")), ("batch", tr("  批量创建文件")),
                        ("activate", tr("  激活Windows")), ("bsod", tr("  让你的设备蓝屏")),
                        ("prank", tr("  恶搞"))]),
            (tr("账户"), [("account", tr("  账户相关"))]),
            (tr("其他"), [("feedback", tr("  反馈问题")), ("changelog", tr("  更新日志")),
                    ("about", tr("  关于"))]),
        ]'''


def has_real_cn_raw(raw):
    """raw 为去掉引号的源码文本；跳过 \\uXXXX/\\xXX 转义，判断是否有真实中文字符"""
    i = 0
    n = len(raw)
    while i < n:
        ch = raw[i]
        if ch == "\\":
            if i + 1 < n and raw[i + 1] in "uxU":
                i += 6 if raw[i + 1] in "uU" else 4
            else:
                i += 2
            continue
        if "\u4e00" <= ch <= "\u9fff":
            return True
        i += 1
    return False


def str_value(s):
    """字符串字面量 -> 值（失败返回 None）"""
    try:
        return ast.literal_eval(s)
    except Exception:
        return None


def group_consecutive_strings(tokens):
    """找出隐式拼接组：连续的 STRING token（允许中间 NL/COMMENT）"""
    groups = []
    i = 0
    n = len(tokens)
    while i < n:
        typ = tokens[i][0]
        if typ == token.STRING and not tokens[i][1].startswith(('"""', "'''")):
            group = [i]
            j = i + 1
            while j < n:
                t2 = tokens[j][0]
                s2 = tokens[j][1]
                if t2 == token.STRING and not s2.startswith(('"""', "'''")):
                    group.append(j)
                    j += 1
                elif t2 in (token.NL, token.COMMENT):
                    j += 1
                else:
                    break
            groups.append(group)
            i = group[-1] + 1
        else:
            i += 1
    return groups


def main():
    src = io.open(SRC, encoding="utf-8").read()

    # ---- 1. 注入 import json ----
    assert 'import hashlib\nimport os\n' in src, 'import block not found'
    src = src.replace('import hashlib\nimport os\n',
                      'import hashlib\nimport json\nimport os\n', 1)

    # ---- 2. 注入 i18n 基础设施（BASE_DIR 定义之后）----
    anchor = 'TEMPLATE_DIR = os.path.join(USERFILES_DIR, "template")'
    assert anchor in src, 'TEMPLATE_DIR not found'
    src = src.replace(anchor, anchor + I18N_BLOCK, 1)

    # ---- 3. NAV_GROUPS -> _nav_groups() ----
    assert OLD_NAV in src, 'NAV_GROUPS block not found'
    src = src.replace(OLD_NAV, NEW_NAV, 1)
    src = src.replace('for group, items in self.NAV_GROUPS:',
                      'for group, items in self._nav_groups():', 1)
    src = src.replace('sum(len(items) for _, items in self.NAV_GROUPS)',
                      'sum(len(items) for _, items in self._nav_groups())', 1)

    # ---- 3.5 混合拼接补丁（普通字符串 + f-string 拼接，脚本无法自动处理）----
    patches = [
        # 反馈页联系方式
        ('text="邮箱1：atwbmail@163.com\\n邮箱2：superselfus@gmail.com\\n"\n'
         '                            f"GitHub：github.com/Hydrooxzgen/",',
         'text=tr("邮箱1：atwbmail@163.com\\n邮箱2：superselfus@gmail.com\\nGitHub：github.com/Hydrooxzgen/"),'),
        # 更新日志页
        ('self._set_text(self.changelog_log,\n'
         '                           "无法找到 Update_Log.log 文件。\\n"\n'
         '                           f"你可以访问 GitHub：github.com/Hydrooxzgen/Projects\\n"\n'
         '                           "下载 Update_Log.log 并放在 App.py 的目录下。")',
         'self._set_text(self.changelog_log,\n'
         '                           tr("无法找到 Update_Log.log 文件。\\n你可以访问 GitHub：github.com/Hydrooxzgen/Projects\\n下载 Update_Log.log 并放在 App.py 的目录下。"))'),
        # batch 页 _row 传实例 bug（AppGUI_CHS.py 保留原始 bug，重建时修复）
        ('        self.batch_type = self._mk_entry(body, width=10)\n'
         '        self.batch_quantity = self._mk_entry(body, width=10)\n'
         '        self.batch_name = self._mk_entry(body, width=24)\n'
         '        self._row(body, "文件类型", self.batch_type)\n'
         '        self._row(body, "文件数量", self.batch_quantity)\n'
         '        self._row(body, "文件前缀名", self.batch_name)',
         '        _, self.batch_type = self._row(body, "文件类型", self._mk_entry, width=10)\n'
         '        _, self.batch_quantity = self._row(body, "文件数量", self._mk_entry, width=10)\n'
         '        _, self.batch_name = self._row(body, "文件前缀名", self._mk_entry, width=24)'),
    ]
    for old, new in patches:
        assert old in src, 'patch not found: ' + old[:50]
        src = src.replace(old, new, 1)

    # ---- 4. tokenize 替换中文字符串 ----
    tokens = list(tokenize.generate_tokens(io.StringIO(src).readline))

    # 隐式拼接组合并：组内任一含中文 -> 整个组合并为一个 tr(...)
    groups = group_consecutive_strings(tokens)
    merge_idx = set()
    replacements = {}  # index -> new token string
    for group in groups:
        if len(group) <= 1:
            continue
        parts = []
        has_cn = False
        ok = True
        for idx in group:
            s = tokens[idx][1]
            v = str_value(s)
            if v is None:
                ok = False
                break
            if has_real_cn_raw(s[1:-1]):
                has_cn = True
            parts.append(v)
        if not ok:
            continue
        if has_cn:
            merged = ''.join(parts)
            new_lit = repr(merged) if '"' not in merged else "'" + merged + "'"
            replacements[group[0]] = 'tr(' + new_lit + ')'
            merge_idx.update(group[1:])

    def prev_meaningful(idx):
        """找 idx 之前第一个非 NL/COMMENT 的 token 索引"""
        k = idx - 1
        while k >= 0 and tokens[k][0] in (token.NL, token.COMMENT, token.INDENT):
            k -= 1
        return k

    # 单个字符串替换（跳过已合并的拼接组，含组首；跳过 tr( 内部字符串）
    for i, tok in enumerate(tokens):
        typ, string = tok[0], tok[1]
        if i in merge_idx or i in replacements:
            continue
        if typ == token.STRING and not string.startswith(('"""', "'''")):
            if len(string) > 1 and string[0] in "rfbuRFBU":
                continue
            # tr( 内部：前一个有效 token 是 '(' 且再前一个是 NAME 'tr'
            p1 = prev_meaningful(i)
            if p1 >= 0 and tokens[p1][0] == token.OP and tokens[p1][1] == '(':
                p2 = prev_meaningful(p1)
                if p2 >= 0 and tokens[p2][0] == token.NAME and tokens[p2][1] == 'tr':
                    continue
            if has_real_cn_raw(string[1:-1]):
                replacements[i] = 'tr(' + string + ')'

    new_tokens = []
    for i, (typ, string, start, end, line) in enumerate(tokens):
        if i in merge_idx:
            continue  # 已合并进组首，不再单独输出
        if i in replacements:
            new_tokens.append(tokenize.TokenInfo(
                token.STRING, replacements[i], start, end, line))
        else:
            new_tokens.append(tokenize.TokenInfo(typ, string, start, end, line))

    new_src = tokenize.untokenize(new_tokens)

    # ---- 4.5 版本号不参与翻译（位于 tr 定义之前，调用会 NameError）----
    new_src = new_src.replace('APP_VERSION = tr("1.0.0 单语言简体中文版")',
                              'APP_VERSION = "1.0.0 单语言简体中文版"', 1)

    # ---- 4.6 注入多语言切换 UI（不写入 App.py，仅 App_new.py 拥有）----
    # a. show_page 记录当前页
    assert new_src.count('    def show_page(self, pid):\n        if pid not in self.page_frames:') == 1
    new_src = new_src.replace(
        '    def show_page(self, pid):\n        if pid not in self.page_frames:',
        '    def show_page(self, pid):\n        self._current_pid = pid\n        if pid not in self.page_frames:', 1)
    # b. 状态栏语言切换按钮
    assert new_src.count('self.btn_switch = tk.Button(bar, text=tr("登录 / 切换账户"), command=self.open_login,') == 1
    new_src = new_src.replace(
        '        self.status_user.pack(side="left", padx=14)\n\n'
        '        self.btn_switch = tk.Button(bar, text=tr("登录 / 切换账户"), command=self.open_login,',
        '        self.status_user.pack(side="left", padx=14)\n\n'
        '        self.btn_lang = tk.Button(bar, text=tr("中文"), command=self._switch_lang,\n'
        '                                  bg=COLORS["statusbar"], fg="#86EFAC",\n'
        '                                  activebackground=COLORS["statusbar"],\n'
        '                                  activeforeground="white", bd=0, relief="flat",\n'
        '                                  cursor="hand2", font=(FONT, 9))\n'
        '        self.btn_lang.pack(side="right", padx=(0, 4))\n\n'
        '        self.btn_switch = tk.Button(bar, text=tr("登录 / 切换账户"), command=self.open_login,', 1)
    # c. _switch_lang 方法（注入在 _update_statusbar 之前）
    assert new_src.count('    def _update_statusbar(self):') == 1
    switch_lang_code = '''    # --------------------------------------------------------
    # 多语言切换
    # --------------------------------------------------------
    def _switch_lang(self):
        """在支持的语言间循环切换，并重建整个界面"""
        codes = list(LANGUAGES.keys())
        idx = codes.index(_CURRENT_LANG)
        next_lang = codes[(idx + 1) % len(codes)]
        _load_lang(next_lang)

        # 重建导航树
        self.nav.delete(*self.nav.get_children())
        self._register_pages()

        # 销毁所有已构建页面（重新以当前语言构建）
        for pid in list(self.page_frames):
            try:
                self.page_frames[pid].destroy()
            except Exception:
                pass
        self.page_frames = {}

        # 更新状态栏文本
        self.status_user.config(
            text=tr('👤 当前用户：{0}', self.username) +
            (tr("（已登录）") if self.logged else tr("（游客）")))
        self.btn_lang.config(text=tr("中文"))
        self.btn_switch.config(text=tr("登录 / 切换账户"))
        self.btn_logout.config(text=tr("退出登录"))

        # 重建当前页面
        self.show_page(getattr(self, "_current_pid", "home"))

    def _update_statusbar(self):'''
    new_src = new_src.replace('    def _update_statusbar(self):', switch_lang_code, 1)

    with io.open(DST, "w", encoding="utf-8", newline="") as f:
        f.write(new_src)

    print("重建完成:", DST)
    single = sum(1 for k in replacements if k not in merge_idx)
    merged_cnt = sum(1 for g in groups if len(g) > 1 and g[0] in replacements)
    print("单字符串替换:", single, "处")
    print("拼接组合并翻译:", merged_cnt, "组")


if __name__ == "__main__":
    main()
