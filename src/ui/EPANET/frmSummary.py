import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow
from ui.EPANET.frmSummaryDesigner import Ui_frmSummary


class frmSummary(QMainWindow, Ui_frmSummary):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Pipes.htm"
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        # section = core.epanet.project.Title()
        self.txtTitle.setText(str(project.title.title))
        self.txtNotes.setPlainText(str(project.title.notes))
        txtstr = "Number of Junctions " + "\t" + str(len(project.junctions.value)) + "\r" + \
                 "Number of Reservoirs " + "\t" + str(len(project.reservoirs.value)) + "\r" + \
                 "Number of Tanks " + "\t" + str(len(project.tanks.value)) + "\r" + \
                 "Number of Pipes " + "\t" + str(len(project.pipes.value)) + "\r" + \
                 "Number of Pumps " + "\t" + str(len(project.pumps.value)) + "\r" + \
                 "Number of Valves " + "\t" + str(len(project.valves.value)) + "\r" + \
                 "Flow Units " + "\t" + "\t" + str(project.options.hydraulics.flow_units.name) + "\r" + \
                 "Headloss Formula " + "\t" + str(project.options.hydraulics.head_loss.name.replace('_', "-")) + "\r" + \
                 "Quality Parameter " + "\t" + str(project.options.quality.chemical_name)
        self.txtStats.setPlainText(txtstr)

    def cmdOK_Clicked(self):
        section = self._main_form.project.title
        section.title = self.txtTitle.text()
        section.notes = self.txtNotes.toPlainText()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
