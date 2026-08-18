# CanApp

> 一个基于 Python + Tkinter 的多功能桌面工具箱，内置多语言支持与本地用户系统。

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)]()
[![License](https://img.shields.io/badge/License-Proprietary-orange)]()

**CanApp** 是一个开箱即用的 Windows 桌面应用合集（2年前搞的了，现在只是图形化了，垃圾项目）

## FEATURES

### 很多feature。。

## 多语言支持

内置三语切换，界面文字实时刷新：

| 语言代码 | 语言 | 说明 |
|----------|------|------|
| `zh_CN` | 简体中文 | 默认语言 |
| `zh_TW` | 繁體中文 | 繁体中文 |
| `en_US` | English | 英语 |

## 安装使用

### 方式一：安装包（推荐）

从 [GitHub Releases](https://github.com/Hydrooxzgen/CanApp/releases) 下载 `CanApp_Setup_x.x.x.exe`，双击安装即可。

- 仅支持Windows系统

### 方式二：从源码运行

需要 **Python 3.13+**（内置 Tkinter）：

```powershell
# 安装依赖
py -m pip install requests pythonping

# 运行
py CanApp.py
```

## 打包构建，发布release

### 1. 打包 exe (通过PyInstaller)

```powershell
py -m PyInstaller CanApp.spec --noconfirm --clean
```

EXE：`dist\CanApp\CanApp.exe`

### 2. 制作安装程序（Inno Setup）

```powershell
& "D:\InnoSetup\InstallPath\ISCC.exe" .\CanApp_installer.iss
```

产物：`dist\CanApp_Setup_{VERSION}.exe`

> 完整发布流程 [`how_to_releaseArelease.txt`](how_to_releaseArelease.txt)

## 项目文件结构

```
CanApp/
├── CanApp.py                  # 主程序（单文件应用）
├── CanApp.spec                # PyInstaller 打包配置
├── CanApp_installer.iss       # Inno Setup 安装脚本
├── lang/
│   ├── zh_CN.json             # 简中翻译(default)
│   ├── zh_TW.json             # 繁中翻译
│   └── en_US.json             # 英语翻译
├── UserFiles/
│   ├── template/              # 内置模板文件
│   └── users/                 # 用户数据（运行时生成）
├── dev/                       # debug工具：
│   ├── _test_all.py           # 完整测试套件(整合dev下其他py的功能)
│   ├── _smoke_test.py         # 冒烟测试
│   ├── _diff_lang.py          # 检查三语键同步
│   ├── _check_i18n.py         # i18n checker
│   ├── _rebuild.py            # 代码重建
│   └── ...
└── how_to_releaseArelease.txt # 发布流程
```

## 开放

```powershell
# 检查三语翻译键同步（期望：总计差异 0）
$env:PYTHONIOENCODING="utf-8"; py dev\_diff_lang.py

# 运行完整测试套件（期望：通过 14 / 14）
$env:PYTHONIOENCODING="utf-8"; py dev\_test_all.py
```

## 作者

- **Hydrooxygen** —— [GitHub](https://github.com/Hydrooxzgen)

## 许可

本项目为个人开源项目，保留所有权利。请勿用于商业用途。
垃圾项目 不喜勿喷
