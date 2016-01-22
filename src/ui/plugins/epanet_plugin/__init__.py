import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from ui.plugins.epanet_plugin.frmHydraulicsOptions import Ui_frmHydraulicsOptions

plugin_name = 'EPANET'
plugin_create_menu = False
__all__ = {}
_main_window = None
_frm_options = None

def load(main_window):
    global _main_window
    _main_window = main_window
    # Set the contents of the project tree control
    model = QtGui.QStandardItemModel()
    model.appendRow(QtGui.QStandardItem("Title/Notes"))
    model.appendRow(QtGui.QStandardItem("Options"))
    hydraulics = QtGui.QStandardItem("Hydraulics")
    hydraulics.appendRow(QtGui.QStandardItem("Controls"))
    hydraulics.appendRow(QtGui.QStandardItem("Links"))
    hydraulics.appendRow(QtGui.QStandardItem("Nodes"))
    model.appendRow(hydraulics)
    model.appendRow(QtGui.QStandardItem("Curves"))
    model.appendRow(QtGui.QStandardItem("Labels"))
    model.appendRow(QtGui.QStandardItem("Patterns"))
    main_window.treeProject.setModel(model)

    # Open EPANET project from File/Open menu
    main_window.actionOpenEPANET = QtGui.QAction(main_window)
    main_window.actionOpenEPANET.setObjectName("actionOpenEPANET")
    main_window.menuFile.addAction(main_window.actionOpenEPANET)
    main_window.actionOpenEPANET.setText("Open EPANET Project")
    QtCore.QObject.connect(main_window.actionOpenEPANET, QtCore.SIGNAL('triggered()'), open_epanet)


def open_epanet():
    if not _main_window:
        QtGui.QMessageBox.critical(None, "Plugin not loaded", "_main_window not set in plugin", QtGui.QMessageBox.Ok)

    file_name = QtGui.QFileDialog.getOpenFileName(None, caption='EPANET Input file')

    opened_project = core.epanet.project.Project()
    opened_project.read_file(file_name)
    _main_window.current_project = opened_project
    model = QtGui.QStandardItemModel()
    for section in opened_project.sections:
        if hasattr(section, "SECTION_NAME"):
            if section.SECTION_NAME == '[OPTIONS]':
                # # Open options form to edit this section
                # action_options = QtGui.QAction(_main_window)
                # action_options.setObjectName("actionOptions")
                # model.appendRow(action_options)
                # action_options.setText("Options")
                # action_options = QtGui.QStandardItem("Options")
                # QtCore.QObject.connect(action_options, QtCore.SIGNAL('triggered()'), open_options)
                model.appendRow(QtGui.QStandardItem("Options"))
            else:
                model.appendRow(QtGui.QStandardItem(section.SECTION_NAME))
        else:
            model.appendRow(QtGui.QStandardItem(section.name))
    _main_window.treeProject.setModel(model)
    open_options()

#    except Exception as ex:
#        QtGui.QMessageBox.critical(None, "Error loading file", file_name + '\n\n' + ex.__str__(), QtGui.QMessageBox.Ok)


def open_options():
    global _main_window, _frm_options
    if not _main_window:
        QtGui.QMessageBox.critical(None, "Plugin not loaded", "_main_window not set in plugin", QtGui.QMessageBox.Ok)
    _frm_options = frmOptions()
    _frm_options.show()

class frmOptions(QtGui.QMainWindow, Ui_frmHydraulicsOptions):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
