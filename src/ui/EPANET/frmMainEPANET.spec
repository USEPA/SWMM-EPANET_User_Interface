# -*- mode: python -*-

block_cipher = None


a = Analysis(['frmMainEPANET.py'],
             pathex=['C:\\devNotMW\\GitHub\\SWMM-EPANET_User_Interface_dev_ui\\src\\ui\\EPANET'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='frmMainEPANET',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries + [('epanet2d.exe', '../../Externals/epanet2d.exe', 'BINARY')],
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='frmMainEPANET')
