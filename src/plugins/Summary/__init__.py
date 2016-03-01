import plugins.Summary.summarizeConduits
import plugins.Summary.summarizeNodes
import plugins.Summary.summarizePressureHeads
import plugins.Summary.summarizeSubbasins
from PyQt4.QtGui import QMessageBox

plugin_name = "Summary"
plugin_create_menu = True
__all__ = {'Title':1, 'Nodes':2, 'Links':3}


def run(session=None, choice=None):
    ltopTitle = 'Plugin:Summary'
    explain_text = "This is a sample plug-in illustrating how a single plug-in could add a menu with several sub-menus." + '\n' + '\n' + "Result: "
    if choice is None:
        choice = 99
    if choice == 1:
        if session and session.project:
            summary = session.project.title.title
        else:
            summary = "Project not open"
        QMessageBox.information(None, ltopTitle, explain_text + '\n' + summary, QMessageBox.Ok)
        # pymsgbox.alert(plugins.Summary.summarizeConduits.run(), ltopTitle)
        pass
    elif choice == 2:
        # pymsgbox.alert(plugins.Summary.summarizeNodes.run(), ltopTitle)
        QMessageBox.information(None, ltopTitle,  explain_text + plugins.Summary.summarizeNodes.run(), QMessageBox.Ok)
        pass
    elif choice == 3:
        # pymsgbox.alert(plugins.Summary.summarizeConduits.run(), ltopTitle)
        QMessageBox.information(None, ltopTitle,  explain_text + plugins.Summary.summarizeConduits.run(), QMessageBox.Ok)
        pass
    elif choice == 99:
        pass
    else:
        # pymsgbox.alert("Top level summary is done.", ltopTitle)
        pass
