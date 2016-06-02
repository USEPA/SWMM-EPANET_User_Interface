import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.report
from core.epanet.options.report import StatusWrite
from enum import Enum
from ui.EPANET.frmReportOptionsDesigner import Ui_frmReportOptions


class frmReportOptions(QtGui.QMainWindow, Ui_frmReportOptions):
    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        # TODO: function that populates combo box from Enum
        self.cboStatus.addItems(("YES", "NO", "FULL"))
        self.cboEnergy.addItems(("YES", "NO"))
        self.cboSummary.addItems(("YES", "NO"))
        self.cboLink1.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboLink2.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboLink3.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboLink4.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboLink5.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboLink6.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboLink7.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboLink8.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboLink9.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboNode1.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboNode2.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboNode3.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboNode4.addItems(("<none>", "BELOW", "ABOVE"))
        self.cboNode5.addItems(("<none>", "BELOW", "ABOVE"))
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    @staticmethod
    def set_combo(combo_box, value):
        try:
            if isinstance(value, Enum):
                value = value.name
            elif isinstance(value, bool):
                if value:
                    value = "YES"
                else:
                    value = "NO"
            index = combo_box.findText(value, QtCore.Qt.MatchFixedString)
            if index >= 0:
                combo_box.setCurrentIndex(index)
        except Exception as e:
            print(str(e))

    def set_from(self, project):
        # section = core.epanet.options.report.ReportOptions()
        section = project.find_section("REPORT")
        self.txtPageSize.setText(str(section.pagesize))
        self.txtReportFileName.setText(str(section.file))
        frmReportOptions.set_combo(self.cboStatus, section.status)
        frmReportOptions.set_combo(self.cboSummary, section.summary)
        frmReportOptions.set_combo(self.cboEnergy, section.energy)

        # if parameter = "Elevation"
        # self.cbxNode1
        # self.cboNode1 = section.parameters
        # self.txtNode1
        # self.txtNode6

        # if parameter = "Demand"
        # self.cbxNode2
        # self.cboNode2 = section.parameters
        # self.txtNode2
        # self.txtNode7

        # if parameter = "Head"
        # self.cbxNode3
        # self.cboNode3 = section.parameters
        # self.txtNode3
        # self.txtNode8

        # if parameter = "Pressure"
        # self.cbxNode4
        # self.cboNode4 = section.parameters
        # self.txtNode4
        # self.txtNode9

        # if parameter = "Quality"
        # self.cbxNode5
        # self.cboNode5 = section.parameters
        # self.txtNode5
        # self.txtNode10

        # if parameter = "Length"
        # self.cbxLink1
        # self.cboLink1 = section.parameters
        # self.txtLink1
        # self.txtLink10

        # if parameter = "Diameter"
        # self.cbxLink2
        # self.cboLink2 = section.parameters
        # self.txtLink2
        # self.txtLink11

        # if parameter = "Flow"
        # self.cbxLink3
        # self.cboLink3 = section.parameters
        # self.txtLink3
        # self.txtLink12

        # if parameter = "Velocity"
        # self.cbxLink4
        # self.cboLink4 = section.parameters
        # self.txtLink4
        # self.txtLink13

        # if parameter = "Headloss"
        # self.cbxLink5
        # self.cboLink5 = section.parameters
        # self.txtLink5
        # self.txtLink14

        # if parameter = "Position"
        # self.cbxLink6
        # self.cboLink6 = section.parameters
        # self.txtLink6
        # self.txtLink15

        # if parameter = "Setting"
        # self.cbxLink7
        # self.cboLink7 = section.parameters
        # self.txtLink7
        # self.txtLink16

        # if parameter = "Reaction"
        # self.cbxLink8
        # self.cboLink8 = section.parameters
        # self.txtLink8
        # self.txtLink17

        # if parameter = "F-Factor"
        # self.cbxLink9
        # self.cboLink9 = section.parameters
        # self.txtLink9
        # self.txtLink18

    def cmdOK_Clicked(self):
        section = self._main_form.project.report
        section.pagesize = self.txtPageSize.text()
        section.file = self.txtReportFileName.text()
        section.status = core.epanet.options.report.StatusWrite[self.cboStatus.currentText()]
        section.summary = self.cboSummary.currentText() == "YES"
        section.energy = self.cboEnergy.currentText() == "YES"
        # parameters still to do
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
