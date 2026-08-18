# -*- mode: python ; coding: utf-8 -*-
# PyInstaller 打包配置：CanApp
# 用法: py -m PyInstaller CanApp.spec
# 输出: dist/CanApp/CanApp.exe  (onedir)

a = Analysis(
    ['CanApp.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('lang', 'lang'),
        ('UserFiles/template', 'UserFiles/template'),
        ('ActiveScript.bat', '.'),
    ],
    hiddenimports=['requests', 'pythonping'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter.test', 'pydoc', 'test', 'unittest'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CanApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CanApp',
)
