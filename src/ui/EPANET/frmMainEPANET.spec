# -*- mode: python -*-

block_cipher = None

qgis_dev = 'C:\\OSGeo4W64\\apps\\qgis-dev\\'
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

qgis_plugins = qgis_dev + 'plugins\\'
lst = []
for file in os.listdir(qgis_plugins):
    lst.append(('plugins/' + file, qgis_plugins + file, 'DATA'))
a.datas += lst

resourcesdir = qgis_dev + 'resources\\'
lst = []
for file in os.listdir(zoneinfodir):
    lst.append(('resources/' + file, resourcesdir + file, 'DATA'))
a.datas += lst

zoneinfodir = site_packages + 'dateutil\\zoneinfo\\'
lst = []
for file in os.listdir(zoneinfodir):
    lst.append(('dateutil/zoneinfo/' + file, zoneinfodir + file, 'DATA'))
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
