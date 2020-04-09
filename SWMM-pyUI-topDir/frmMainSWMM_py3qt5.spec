# -*- mode: python -*-

block_cipher = None

apps_qgis = 'C:\\OSGeo4W64\\apps\\qgis\\'
apps_qgis_bin = 'C:\\OSGeo4W64\\apps\\qgis\\bin\\'
site_packages = 'C:\\OSGeo4W64\\apps\\Python37\\Lib\\site-packages\\'
proj_base = 'C:\\dev\\SWMM-EPANET_User_Interface\\src\\' 

a = Analysis(['frmMainSWMM.py'],
             pathex=[site_packages + 'PyQt5', apps_qgis, apps_qgis_bin, proj_base, proj_base + 'ui', proj_base + 'ui\\SWMM'],
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
        # if file == "__init__.py":
        plugin_lst.append(('plugins/' + plugin_name + '/' + file, '../../plugins/' + plugin_name + '/' + file, 'DATA'))
    return plugin_lst

a.datas += add_plugin('ImportExportGIS')
a.datas += add_plugin('Summary')

folder = apps_qgis + 'plugins\\'
lst = []
for file in os.listdir(folder):
    lst.append(('plugins/' + file, folder + file, 'DATA'))
a.datas += lst
a.datas += Tree(site_packages + '\\swmm\\output', prefix='swmm/output')

#folder = apps_qgis + 'resources\\'
#lst = []
#for file in os.listdir(folder):
#    lst.append(('resources/' + file, folder + file, 'DATA'))
#a.datas += lst

folder = site_packages + 'dateutil\\zoneinfo\\'
lst = []
for file in os.listdir(folder):
    lst.append(('dateutil/zoneinfo/' + file, folder + file, 'DATA'))
a.datas += lst

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='SWMM-UI',
          debug=False,
          strip=False,
          upx=True,
          console=True )

pybin = 'C:\\OSGeo4W64\\bin\\'
pyqtbin = 'C:\\OSGeo4W64\\apps\\Qt5\\bin\\'

coll = COLLECT(exe,
               a.binaries + [('swmm5.exe', '../../Externals/swmm/model/swmm5.exe', 'BINARY')]
                          + [('swmm5_x64.dll', '../../Externals/swmm/model/swmm5_x64.dll', 'BINARY')]
                          + [('SMOutputapi-64.dll', '../../Externals/swmm/outputapi/SMOutputapi-64.dll', 'BINARY')]
                          + [('swmm.qch', 'swmm.qch', 'BINARY')]
                          + [('swmm.qhc', 'swmm.qhc', 'BINARY')]
                          + [('assistant.exe',  pyqtbin + 'assistant.exe', 'BINARY')]
                          + [('Qt5Help.dll',    pyqtbin + 'Qt5Help.dll', 'BINARY')],
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='SWMM-UI')
