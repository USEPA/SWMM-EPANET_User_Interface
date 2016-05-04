import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydraulics.node import Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmTreatment(frmGenericPropertyEditor):

    SECTION_NAME = "[TREATMENT]"

    def __init__(self, parent, node_name):
        # purposely not calling frmGenericPropertyEditor.__init__
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.node_name = node_name
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.setWindowTitle('SWMM Treatment Editor for Node ' + node_name)
        self.lblNotes.setText(Treatment.hint)
        self.tblGeneric.setColumnCount(1)
        local_column_list = ['Treatment Expression']
        self.tblGeneric.setHorizontalHeaderLabels(local_column_list)
        self.tblGeneric.setColumnWidth(0,400)
        self.local_pollutant_list = []
        pollutants_section = parent.project.find_section("POLLUTANTS")
        row_count = 0
        for value in pollutants_section.value:
            row_count += 1
            self.local_pollutant_list.append(value.name)
        self.tblGeneric.setRowCount(row_count)
        self.tblGeneric.setVerticalHeaderLabels(self.local_pollutant_list)
        self.resize(480,600)
        # self.fraTop.resize(400,200)
        # self.fraTop.setMaximumHeight(200)
        self.fraNotes.height = 400
        section = parent.project.find_section("TREATMENT")
        treatment_list = section.value[0:]
        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            for treatment in treatment_list:
                if treatment.node == node_name and treatment.pollutant == pollutant:
                    led = QtGui.QLineEdit(str(treatment.function))
                    self.tblGeneric.setItem(pollutant_count,0,QtGui.QTableWidgetItem(led.text()))
        self._parent = parent

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("TREATMENT")
        treatment_list = section.value[0:]
        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            treatment_found = False
            for treatment in treatment_list:
                if treatment.node == self.node_name and treatment.pollutant == pollutant:
                    # put this back in place
                    treatment_found = True
                    if self.tblGeneric.item(pollutant_count,0) and len(self.tblGeneric.item(pollutant_count,0).text()) > 0:
                        treatment.function = self.tblGeneric.item(pollutant_count,0).text()
                    else:
                        section.value.remove(treatment)
            if not treatment_found:
                # add new record
                if self.tblGeneric.item(pollutant_count,0):
                    value1 = Treatment()
                    value1.node = self.node_name
                    value1.pollutant = pollutant
                    value1.function = str(self.tblGeneric.item(pollutant_count,0).text())
                    if section.value == '':
                        section.value = []
                    section.value.append(value1)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
