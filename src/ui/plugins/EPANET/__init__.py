import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from ui.plugins.EPANET.frmHydraulicsOptions import Ui_frmHydraulicsOptions

plugin_name = "EPANET"
plugin_create_menu = False
__all__ = {}
_main_window = None
_frm_options = None


def load(main_window):
    global _main_window
    _main_window = main_window
    _main_window.setWindowTitle("EPANET")
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

    # Save EPANET project from File/Save As menu
    main_window.actionSaveEPANET = QtGui.QAction(main_window)
    main_window.actionSaveEPANET.setObjectName("actionSaveEPANET")
    main_window.menuFile.addAction(main_window.actionSaveEPANET)
    main_window.actionSaveEPANET.setText("Save EPANET Project As...")
    QtCore.QObject.connect(main_window.actionSaveEPANET, QtCore.SIGNAL('triggered()'), save_epanet)

def open_epanet():
    if not _main_window:
        QtGui.QMessageBox.critical(None, "Plugin not loaded", "_main_window not set in plugin", QtGui.QMessageBox.Ok)
        return

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


def save_epanet():
    if not _main_window:
        QtGui.QMessageBox.critical(None, "Plugin not loaded", "_main_window not set in plugin", QtGui.QMessageBox.Ok)
        return

    file_name = QtGui.QFileDialog.getSaveFileName(None, caption='EPANET Input file')
    inp_writer = open(file_name, 'w')
    inp_writer.write(_main_window.current_project.to_inp())
    inp_writer.close()


def open_options():
    global _main_window, _frm_options
    if not _main_window:
        QtGui.QMessageBox.critical(None, "Plugin not loaded", "_main_window not set in plugin", QtGui.QMessageBox.Ok)
    _frm_options = frmOptions()
    _frm_options.show()


class frmOptions(QtGui.QMainWindow, Ui_frmHydraulicsOptions):
    def __init__(self, parent=None):
        if not parent:
            parent = _main_window
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        # TODO: function that populates combo box from Enum
        self.cboFlowUnits.addItems(("CFS", "GPM", "MGD", "IMGD", "AFD", "LPS", "LPM", "MLD", "CMH", "CMD"))
        self.cboHeadloss.addItems(("H_W", "D_W", "C_M"))
        self.cboUnbalanced.addItems(("STOP", "CONTINUE"))
        self.set_from(_main_window.current_project)

    def set_from(self, project):
        section = project.find_section("OPTIONS")
        self.txtSpecificGravity.setText(section.specific_gravity)
        self.txtRelativeViscosity.setText(section.relative_viscosity)
        self.txtMaximumTrials.setText(section.maximum_trials)
        self.txtAccuracy.setText(section.accuracy)
        self.txtDefaultPattern.setText(section.default_pattern)
        self.txtDemandMultiplier.setText(section.demand_multiplier)
        self.txtEmitterExponent.setText(section.emitter_exponent)
        self.txtCheckFrequency.setText(section.check_frequency)
        self.txtMaxCheck.setText(section.max_check)
        self.txtDampLimit.setText(section.damp_limit)

