import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydrology.subcatchment import InitialLoading
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmInitialBuildup(frmGenericPropertyEditor):

    SECTION_NAME = "[LOADINGS]"

    def __init__(self, parent, subcatchment_name):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.subcatchment_name = subcatchment_name
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.setWindowTitle('SWMM Initial Buildup Editor for Subcatchment ' + subcatchment_name)
        self.lblNotes.setText("Enter initial buildup of pollutants on Subcatchment " + subcatchment_name)
        self.tblGeneric.setColumnCount(1)
        local_column_list = []
        units = 1
        if units == 1:
            local_column_list.append('Initial Buildup (lbs/ac)')
        else:
            local_column_list.append('Initial Buildup (kg/ha)')
        self.tblGeneric.setHorizontalHeaderLabels(local_column_list)
        self.tblGeneric.setColumnWidth(0,200)
        self.local_pollutant_list = []
        pollutants_section = parent.project.find_section("POLLUTANTS")
        row_count = 0
        for value in pollutants_section.value:
            row_count += 1
            self.local_pollutant_list.append(value.name)
        self.tblGeneric.setRowCount(row_count)
        self.tblGeneric.setVerticalHeaderLabels(self.local_pollutant_list)
        self.resize(300,300)
        section = parent.project.find_section("LOADINGS")
        loadings_list = section.value[0:]
        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            for loading in loadings_list:
                if loading.subcatchment_name == subcatchment_name and loading.pollutant_name == pollutant:
                    led = QtGui.QLineEdit(str(loading.initial_buildup))
                    self.tblGeneric.setItem(pollutant_count,0,QtGui.QTableWidgetItem(led.text()))
        self._parent = parent

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("LOADINGS")
        loadings_list = section.value[0:]
        pollutant_count = -1
        for pollutant in self.local_pollutant_list:
            pollutant_count += 1
            loading_found = False
            for loading in loadings_list:
                if loading.subcatchment_name == self.subcatchment_name and loading.pollutant_name == pollutant:
                    # put this back in place
                    loading_found = True
                    if self.tblGeneric.item(pollutant_count,0) and len(self.tblGeneric.item(pollutant_count,0).text()) > 0:
                        loading.initial_buildup = self.tblGeneric.item(pollutant_count,0).text()
                    else:
                        section.value.remove(loading)
            if not loading_found:
                # add new record
                if self.tblGeneric.item(pollutant_count,0):
                    value1 = InitialLoading()
                    value1.subcatchment_name = self.subcatchment_name
                    value1.pollutant_name = pollutant
                    value1.initial_buildup = str(self.tblGeneric.item(pollutant_count,0).text())
                    if section.value == '':
                        section.value = []
                    section.value.append(value1)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
