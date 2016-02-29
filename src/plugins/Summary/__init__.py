import plugins.Summary.summarizeConduits
import plugins.Summary.summarizeNodes
import plugins.Summary.summarizePressureHeads
import plugins.Summary.summarizeSubbasins
from PyQt4.QtGui import QMessageBox

plugin_name = "Summary"
plugin_create_menu = True
__all__ = {'Conduits':1, 'Nodes':2, 'PressureHeads':3, 'Subbasins':4}


def run(session=None, choice=None):
    ltopTitle = 'Plugin:Summary'
    if choice is None:
        choice = 99
    if choice == 1:
        if session and session.project:
            summary = session.project.title.title
        else:
            summary = "Project not open"
        QMessageBox.information(None, ltopTitle, summary, QMessageBox.Ok)
        # pymsgbox.alert(plugins.Summary.summarizeConduits.run(), ltopTitle)
        pass
    elif choice == 2:
        # pymsgbox.alert(plugins.Summary.summarizeNodes.run(), ltopTitle)
        pass
    elif choice == 3:
        # pymsgbox.alert(plugins.Summary.summarizePressureHeads.run(), ltopTitle)
        pass
    elif choice == 4:
        # pymsgbox.alert(plugins.Summary.summarizeSubbasins.run(), ltopTitle)
        pass
    elif choice == 99:
        pass
    else:
        # pymsgbox.alert("Top level summary is done.", ltopTitle)
        pass
