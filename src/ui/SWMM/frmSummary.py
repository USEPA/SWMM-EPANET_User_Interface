import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.SWMM.frmSummaryDesigner import Ui_frmSummary
from ui.help import HelpHandler


class frmSummary(QMainWindow, Ui_frmSummary):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/projectmenu.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

        if (main_form.program_settings.value("Geometry/" + "frmSummary_geometry")
                and main_form.program_settings.value("Geometry/" + "frmSummary_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmSummary_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmSummary_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, project):
        self.txtTitle.setText(str(project.title.title))
        self.txtNotes.setPlainText(str(project.title.comment))
        txtstr = "Number of Raingages " + "\t" + "\t" + str(len(project.raingages.value)) + "\r" + \
                 "Number of Subcatchments " + "\t" + "\t" + str(len(project.subcatchments.value)) + "\r" + \
                 "Number of Aquifers " + "\t" + "\t" + str(len(project.aquifers.value)) + "\r" + \
                 "Number of Snowpacks " + "\t" + "\t" + str(len(project.snowpacks.value)) + "\r" + \
                 "Number of RDII Hydrographs " + "\t" + str(len(project.hydrographs.value)) + "\r" + \
                 "Infiltration Model " + "\t" + "\t" + project.options.infiltration + "\r" + \
                 "Junction Nodes " + "\t" + "\t" +str(len(project.junctions.value)) + "\r" + \
                 "Outfall Nodes " + "\t" + "\t" + str(len(project.outfalls.value)) + "\r" + \
                 "Divider Nodes " + "\t" + "\t" + str(len(project.dividers.value)) + "\r" + \
                 "Storage Nodes " + "\t" + "\t" + str(len(project.storage.value)) + "\r" + \
                 "Conduit Links " + "\t" + "\t" + "\t" + str(len(project.conduits.value)) + "\r" + \
                 "Pump Links " + "\t" + "\t" + "\t" + str(len(project.pumps.value)) + "\r" + \
                 "Orifice Links " + "\t" + "\t" + "\t" + str(len(project.orifices.value)) + "\r" + \
                 "Weir Links " + "\t" + "\t" + "\t" + str(len(project.weirs.value)) + "\r" + \
                 "Outlet Links " + "\t" + "\t" + "\t" + str(len(project.outlets.value)) + "\r" + \
                 "Flow Units " + "\t" + "\t" + "\t" + project.options.flow_units.name + "\r" + \
                 "Flow Routing " + "\t" + "\t" + "\t" + project.options.flow_routing.name + "\r" + \
                 "Control Rules " + "\t" + "\t" + str(len(project.controls.value)) + "\r" + \
                 "Pollutants " + "\t" + "\t" + "\t" + str(len(project.pollutants.value)) + "\r" + \
                 "Land Uses " + "\t" + "\t" + "\t" + str(len(project.landuses.value)) + "\r" + \
                 "Time Series Inflows " + "\t" + "\t" + str(len(project.inflows.value)) + "\r" + \
                 "Dry Weather Inflows " + "\t" + "\t" + str(len(project.dwf.value)) + "\r" + \
                 "Groundwater Inflows " + "\t" + "\t" + str(len(project.aquifers.value)) + "\r" + \
                 "RDII Inflows " + "\t" + "\t" + "\t" + str(len(project.rdii.value)) + "\r" + \
                 "LID Controls " + "\t" + "\t" + "\t" + str(len(project.lid_controls.value)) + "\r" + \
                 "Treatment Units " + "\t" + "\t" + str(len(project.lid_usage.value))
        self.txtStats.setPlainText(txtstr)

    def cmdOK_Clicked(self):
        section = self._main_form.project.title
        if section.title != self.txtTitle.text() or \
            section.comment != self.txtNotes.toPlainText():
            self._main_form.mark_project_as_unsaved()

        section.title = self.txtTitle.text()
        section.comment = self.txtNotes.toPlainText()

        self._main_form.program_settings.setValue("Geometry/" + "frmSummary_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmSummary_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
