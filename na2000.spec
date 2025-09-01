# -*- mode: python ; coding: utf-8 -*-
def getLib():
    result = []
    for root, dirs, filenames in os.walk("lib"):
        if "__pycache__" in root:
            continue

        for file in filenames:
            if not file.endswith(".pyc") and not file.startswith("."):
                src = os.path.join(root, file)
                dest = os.path.relpath(root, "lib")
                if dest == ".":
                    dest = ""
                result.append((src, os.path.join("lib", dest)))
    return result


a = Analysis(
    ["na2000.py"],
    pathex=[],
    binaries=[],
    datas=getLib(),
    hiddenimports=[
	'lib.CrashHelper',
    'ctypes',
    '_ctypes',
    'ctypes.util',
    'multiprocessing',
    'multiprocessing.util',
    'multiprocessing.context',
    'multiprocessing.reduction',
	],
    hookspath=[],
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
    a.binaries,
    a.datas,
    [],
    name="na2000",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon='external/icon.ico'
)
