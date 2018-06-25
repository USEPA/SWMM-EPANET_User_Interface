# import plugins.Summary.summarizeConduits
# import plugins.Summary.summarizeNodes
# import plugins.Summary.summarizePressureHeads
# import plugins.Summary.summarizeSubbasins
from PyQt5.QtGui import QMessageBox

plugin_name = "Summary"
plugin_create_menu = True
__all__ = {"Title":1, "Nodes":2, "Links":3}


def run(session=None, choice=None):
    ltopTitle = 'Plugin:Summary'
    explain_text = "This is a sample plug-in illustrating how a single plug-in can add a menu with several functions." \
                   + "\n\nResult: "
    if choice is None:
        choice = 99
    if choice == 1:
        if session and session.project:
            summary = session.project.title.title
        else:
            summary = "Project is not open"
        QMessageBox.information(None, ltopTitle, explain_text + '\n' + summary, QMessageBox.Ok)
        pass
    elif choice == 2:
        QMessageBox.information(None, ltopTitle,  explain_text + '\n' + "summarizeNodes", QMessageBox.Ok)
        pass
    elif choice == 3:
        QMessageBox.information(None, ltopTitle,  explain_text + '\n' + "summarizeConduits", QMessageBox.Ok)
        pass
    elif choice == 99:
        pass
    else:
        QMessageBox.information(None, ltopTitle,  explain_text + '\n' + "Top level summary is done.", QMessageBox.Ok)
        pass
