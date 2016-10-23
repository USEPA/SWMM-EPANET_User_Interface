# -*- mode: python -*-

block_cipher = None

apps_qgis = 'C:\\OSGeo4W64\\apps\\qgis\\'
site_packages = 'C:\\OSGeo4W64\\apps\\Python27\\Lib\\site-packages\\'

a = Analysis(['frmMainEPANET.py'],
             pathex=[site_packages + 'PyQt4', 'C:\\devNotMW\\GitHub\\SWMM-EPANET_User_Interface_dev_ui\\src\\ui\\EPANET'],
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
          name='EPANET-UI',
          debug=False,
          strip=False,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries + [('epanet2_amd64.dll', '../../Externals/epanet/model/epanet2_amd64.dll', 'BINARY')]
                          + [('ENOutputAPI-64.dll', '../../Externals/epanet/outputapi/ENOutputAPI-64.dll', 'BINARY')],
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='EPANET-UI')
