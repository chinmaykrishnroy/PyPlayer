# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/aarav/OneDrive/Documents/Code/PyPlayer/PyPlayer/New folder (2)/main.py'],
    pathex=['C:/Users/aarav/AppData/Local/Programs/Python/Python311/Lib/site-packages/PyQt5/Qt5/bin'],
    binaries=[],
    datas=[('C:/Users/aarav/OneDrive/Documents/Code/PyPlayer/PyPlayer/New folder (2)/res_rc.py', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='PyPlayer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\aarav\\OneDrive\\Documents\\Code\\PyPlayer\\PyPlayer\\New folder (2)\\player.ico'],
    hide_console='hide-early',
)
