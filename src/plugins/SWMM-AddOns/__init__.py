from PyQt5 import QtCore

plugin_name = "SWMM-AddOns"
plugin_create_menu = True
__all__ = {"SWMM-CAT":1,
           "SSOAP":2}

def run(session=None, choice=None):

    if choice == 1:
        swmmcat_executable_full_path = "C:\Program Files (x86)\SWMM-CAT\SWMM-CAT.exe"

        swmmcat_process = QtCore.QProcess()
        swmmcat_process.startDetached(swmmcat_executable_full_path, [])

    if choice == 2:
        ssoap_executable_full_path = "C:\Program Files (x86)\EPA SSOAP Toolbox\SSOAPToolbox.exe"

        ssoap_process = QtCore.QProcess()
        ssoap_process.startDetached(ssoap_executable_full_path, [])