# -*- mode: python ; coding: utf-8 -*-

import sys
import importlib
from os.path import dirname, join

base_path = dirname(dirname(sys.executable))
typelib_path = join(base_path, 'lib/girepository-1.0')
block_cipher = None

module_datas = [('currency_converter', ['eurofxref.csv', 'eurofxref-hist.zip'])]
__module_datas = []

for module, datas in module_datas:
  root = dirname(importlib.import_module(module).__file__)
  __module_datas.extend((join(root, data), module) for data in datas)

a = Analysis([join(base_path, 'bin/stringbuddydemo')],
             binaries=[(join(typelib_path, tl), 'gi_typelibs') for tl in os.listdir(typelib_path)],
             datas=[*__module_datas,
                    (join(base_path, 'etc/gtk-3.0'), 'etc/gtk-3.0'),
                    (join(base_path, 'share/stringbuddydemo'), 'share/stringbuddydemo')],
             hiddenimports=[
                'gi.repository.Gtk',
                'currency_converter',
                'dateutil.parser',
                'webbrowser',
                'requests',
                'platform'
                ],
             hookspath=[],
             hooksconfig={
                'gi': {
                    'icons': ['Fluent'],
                    'themes': ['Fluent'],
                    'languages': ['en_US'],
                    'module-versions': {
                       'Gtk': '3.0'
                     }
                }
             },
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
          [],
          exclude_binaries=True,
          name='stringbuddydemo',
          icon='../build/logo.ico',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=False,
               name='stringbuddydemo')
