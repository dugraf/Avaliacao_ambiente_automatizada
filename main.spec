# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['asyncio', 'uuid', 'cryptography', 'cryptography.hazmat.backends', 'cryptography.hazmat.backends.openssl', 'cryptography.hazmat.bindings._rust']
hiddenimports += collect_submodules('cryptography')


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('D:\\Program Files\\OpenSSL-Win64\\bin\\libssl-3-x64.dll', '.'), ('D:\\Program Files\\OpenSSL-Win64\\bin\\libcrypto-3-x64.dll', '.')],
    datas=[('assets', 'assets'), ('logs', 'logs'), ('controllers\\scripts', 'controllers\\scripts')],
    hiddenimports=hiddenimports,
    hookspath=['hooks'],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
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
    name='main',
)
