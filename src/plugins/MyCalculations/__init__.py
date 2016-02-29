from PyQt4.QtGui import QMessageBox

plugin_name = 'MyCalculations'
plugin_create_menu = False
__all__ = {}


def run(session=None, choice=None):
    ltopTitle = 'Plugin:MyCalculations'
    QMessageBox.information(None, ltopTitle, "Custom user calculation is done.", QMessageBox.Ok)
