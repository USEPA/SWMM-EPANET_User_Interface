import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from core.swmm.hydrology.subcatchment import Coverages
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor


class frmLandUseAssignment(frmGenericPropertyEditor):

    SECTION_NAME = "[COVERAGES]"

    def __init__(self, parent, subcatchment_name):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.subcatchment_name = subcatchment_name
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.setWindowTitle('SWMM Land Use Assignment for Subcatchment ' + subcatchment_name)
        self.lblNotes.setText('')
        self.tblGeneric.setColumnCount(1)
        local_column_list = []
        local_column_list.append('% of Area')
        self.tblGeneric.setHorizontalHeaderLabels(local_column_list)
        self.tblGeneric.setColumnWidth(0,200)
        self.local_land_use_list = []
        land_use_section = parent.project.find_section("LANDUSES")
        row_count = 0
        for value in land_use_section.value:
            row_count += 1
            self.local_land_use_list.append(value.land_use_name)
        self.tblGeneric.setRowCount(row_count)
        self.tblGeneric.setVerticalHeaderLabels(self.local_land_use_list)
        self.resize(300,300)
        section = parent.project.find_section("COVERAGES")
        coverage_list = section.value[0:]
        land_use_count = -1
        for land_use in self.local_land_use_list:
            land_use_count += 1
            for coverage in coverage_list:
                if coverage.subcatchment_name == subcatchment_name and coverage.land_use_name == land_use:
                    led = QtGui.QLineEdit(str(coverage.percent_subcatchment_area))
                    self.tblGeneric.setItem(land_use_count,0,QtGui.QTableWidgetItem(led.text()))
        self._parent = parent

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("COVERAGES")
        coverage_list = section.value[0:]
        land_use_count = -1
        for land_use in self.local_land_use_list:
            land_use_count += 1
            coverage_found = False
            for coverage in coverage_list:
                if coverage.subcatchment_name == self.subcatchment_name and coverage.land_use_name == land_use:
                    # put this back in place
                    coverage_found = True
                    if self.tblGeneric.item(land_use_count,0) and len(self.tblGeneric.item(land_use_count,0).text()) > 0:
                        coverage.percent_subcatchment_area = self.tblGeneric.item(land_use_count,0).text()
                    else:
                        section.value.remove(coverage)
            if not coverage_found:
                # add new record
                if self.tblGeneric.item(land_use_count,0):
                    value1 = Coverages()
                    value1.subcatchment_name = self.subcatchment_name
                    value1.land_use_name = land_use
                    value1.percent_subcatchment_area = str(self.tblGeneric.item(land_use_count,0).text())
                    if section.value == '':
                        section.value = []
                    section.value.append(value1)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
