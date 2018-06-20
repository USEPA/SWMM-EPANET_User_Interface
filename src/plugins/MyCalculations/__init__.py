from PyQt5.QtGui import QMessageBox

plugin_name = 'MyCalculations'
plugin_create_menu = False
__all__ = {}


def run(session=None, choice=None):
    ltopTitle = 'Plugin:MyCalculations'
    QMessageBox.information(None, ltopTitle, "This is a sample plug-in illustrating how a single menu could contain a custom user calculation.", QMessageBox.Ok)
