# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=['magic_filter', 'moviepy', 'imageio_ffmpeg.binaries'],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='Render360.exe',
            debug=False,
            strip=None,
            upx=True,
            console=False,
            icon='s_icon.ico')