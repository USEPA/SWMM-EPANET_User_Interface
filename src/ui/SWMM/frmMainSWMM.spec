# -*- mode: python -*-

block_cipher = None


a = Analysis(['frmMainSWMM.py'],
             pathex=['C:\\Users\\Mark\\Anaconda2\\Lib\\site-packages\\PyQt4', 'C:\\devNotMW\\GitHub\\SWMM-EPANET_User_Interface_dev_ui\\src\\ui\\SWMM'],
             binaries=None,
             datas=None,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

def add_plugin(plugin_name):
    import os
    plugin_lst = []
    for file in os.listdir('../../plugins/' + plugin_name):
        if file == "__init__.py":
            plugin_lst.append(('plugins/' + plugin_name + '/' + file, '../../plugins/' + plugin_name + '/' + file, 'DATA'))
    return plugin_lst

a.datas += add_plugin('Summary')

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='frmMainSWMM',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries + [('swmm5.exe', '../../Externals/swmm/model/swmm5.exe', 'BINARY')]
                          + [('vcomp100.dll', '../../Externals/swmm/model/vcomp100.dll', 'BINARY')]
                          + [('SMOutputapi-64.dll', '../../Externals/swmm/outputapi/SMOutputapi-64.dll', 'BINARY')],
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='frmMainSWMM')
