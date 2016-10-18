import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from core.swmm.hydrology.unithydrograph import UnitHydrographEntry
from ui.SWMM.frmUnitHydrographDesigner import Ui_frmUnitHydrograph
from core.swmm.hydrology.unithydrograph import UnitHydrograph


class frmUnitHydrograph(QtGui.QMainWindow, Ui_frmUnitHydrograph):
    month = ['All Months', 'January', 'February', 'March', 'April', 'May', 'June',
             'July', 'August', 'September', 'October', 'November', 'December']
    month3 = ['All', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def __init__(self, main_form, edit_these, new_item):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/unithydrographeditordialog.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboHydrograph.currentIndexChanged.connect(self.cboHydrograph_currentIndexChanged)
        self._main_form = main_form
        self.project = main_form.project
        self.section = self.project.hydrographs
        self.new_item = new_item
        if new_item:
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):  # edit first hydrograph if given a list
                self.set_from(edit_these[0])
            else:
                self.set_from(edit_these)

    def set_from(self, hydrograph):
        if not isinstance(hydrograph, UnitHydrograph):
            hydrograph = self.section.value[hydrograph]
        if isinstance(hydrograph, UnitHydrograph):
            self.editing_item = hydrograph

        self.txtGroup.setText(hydrograph.name)

        self.cboHydrograph.setCurrentIndex(0)
        self.tblPack.setItem(0, 0, QtGui.QTableWidgetItem(''))
        self.tblPack.setItem(0, 1, QtGui.QTableWidgetItem(''))
        self.tblPack.setItem(0, 2, QtGui.QTableWidgetItem(''))
        self.tblAbstraction.setItem(0, 0, QtGui.QTableWidgetItem(''))
        self.tblAbstraction.setItem(0, 1, QtGui.QTableWidgetItem(''))
        self.tblAbstraction.setItem(0, 2, QtGui.QTableWidgetItem(''))
        self.tblPack.setItem(1, 0, QtGui.QTableWidgetItem(''))
        self.tblPack.setItem(1, 1, QtGui.QTableWidgetItem(''))
        self.tblPack.setItem(1, 2, QtGui.QTableWidgetItem(''))
        self.tblAbstraction.setItem(1, 0, QtGui.QTableWidgetItem(''))
        self.tblAbstraction.setItem(1, 1, QtGui.QTableWidgetItem(''))
        self.tblAbstraction.setItem(1, 2, QtGui.QTableWidgetItem(''))
        self.tblPack.setItem(2, 0, QtGui.QTableWidgetItem(''))
        self.tblPack.setItem(2, 1, QtGui.QTableWidgetItem(''))
        self.tblPack.setItem(2, 2, QtGui.QTableWidgetItem(''))
        self.tblAbstraction.setItem(2, 0, QtGui.QTableWidgetItem(''))
        self.tblAbstraction.setItem(2, 1, QtGui.QTableWidgetItem(''))
        self.tblAbstraction.setItem(2, 2, QtGui.QTableWidgetItem(''))
        for value in hydrograph.value:
            month_index = self.month3.index(value.hydrograph_month)
            self.cboHydrograph.setItemText(month_index, self.month[month_index] + " (*)")
            if value.hydrograph_month == 'All':
                # this is one we want to load
                row = 2
                if value.term == 'Short':
                    row = 0
                elif value.term == 'Medium':
                    row = 1
                led = QtGui.QLineEdit(str(value.response_ratio))
                self.tblPack.setItem(row, 0, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.time_to_peak))
                self.tblPack.setItem(row, 1, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.recession_limb_ratio))
                self.tblPack.setItem(row, 2, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.initial_abstraction_depth))
                self.tblAbstraction.setItem(row, 0, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.initial_abstraction_rate))
                self.tblAbstraction.setItem(row, 1, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.initial_abstraction_amount))
                self.tblAbstraction.setItem(row, 2, QtGui.QTableWidgetItem(led.text()))

        # code to set rain gage combo, to be implemented with rain gages
        rain_section = self.project.raingages
        rain_list = rain_section.value[0:]
        self.cboRain.clear()
        selected_index = 0
        for value in rain_list:
            self.cboRain.addItem(value.name)
            if value.name == hydrograph.rain_gage_name:
                selected_index = int(self.cboRain.count())-1
                self.cboRain.setCurrentIndex(selected_index)

    def cmdOK_Clicked(self):
        self.editing_item.name = self.txtGroup.text()
        self.editing_item.rain_gage_name = self.cboRain.currentText()
        month = self.month3[self.cboHydrograph.currentIndex()]
        month_found = False
        for value in self.editing_item.value:
            if value.hydrograph_month == month:
                # this is one we want to save
                month_found = True
                row = 2
                if value.term == 'Short':
                    row = 0
                elif value.term == 'Medium':
                    row = 1
                value.response_ratio = self.tblPack.item(row, 0).text()
                value.time_to_peak = self.tblPack.item(row, 1).text()
                value.recession_limb_ratio = self.tblPack.item(row, 2).text()
                value.initial_abstraction_depth = self.tblAbstraction.item(row, 0).text()
                value.initial_abstraction_rate = self.tblAbstraction.item(row, 1).text()
                value.initial_abstraction_amount = self.tblAbstraction.item(row, 2).text()
        if not month_found:
            # add new records for this month
            value1 = UnitHydrographEntry()
            value1.hydrograph_month = month
            value1.term = 'Short'
            value1.response_ratio = self.tblPack.item(0, 0).text()
            value1.time_to_peak = self.tblPack.item(0, 1).text()
            value1.recession_limb_ratio = self.tblPack.item(0, 2).text()
            value1.initial_abstraction_depth = self.tblAbstraction.item(0, 0).text()
            value1.initial_abstraction_rate = self.tblAbstraction.item(0, 1).text()
            value1.initial_abstraction_amount = self.tblAbstraction.item(0, 2).text()
            self.editing_item.value.append(value1)
            value2 = UnitHydrographEntry()
            value2.hydrograph_month = month
            value2.term = 'Medium'
            value2.response_ratio = self.tblPack.item(1, 0).text()
            value2.time_to_peak = self.tblPack.item(1, 1).text()
            value2.recession_limb_ratio = self.tblPack.item(1, 2).text()
            value2.initial_abstraction_depth = self.tblAbstraction.item(1, 0).text()
            value2.initial_abstraction_rate = self.tblAbstraction.item(1, 1).text()
            value2.initial_abstraction_amount = self.tblAbstraction.item(1, 2).text()
            self.editing_item.value.append(value2)
            value3 = UnitHydrographEntry()
            value3.hydrograph_month = month
            value3.term = 'Long'
            value3.response_ratio = self.tblPack.item(2, 0).text()
            value3.time_to_peak = self.tblPack.item(2, 1).text()
            value3.recession_limb_ratio = self.tblPack.item(2, 2).text()
            value3.initial_abstraction_depth = self.tblAbstraction.item(2, 0).text()
            value3.initial_abstraction_rate = self.tblAbstraction.item(2, 1).text()
            value3.initial_abstraction_amount = self.tblAbstraction.item(2, 2).text()
            self.editing_item.value.append(value3)
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
        else:
            pass
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboHydrograph_currentIndexChanged(self, newIndex):
        led = QtGui.QLineEdit('')
        self.tblPack.setItem(0, 0, QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(0, 1, QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(0, 2, QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(0, 0, QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(0, 1, QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(0, 2, QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(1, 0, QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(1, 1, QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(1, 2, QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(1, 0, QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(1, 1, QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(1, 2, QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(2, 0, QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(2, 1, QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(2, 2, QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(2, 0, QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(2, 1, QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(2, 2, QtGui.QTableWidgetItem(led.text()))

        for value in self.editing_item.value:
            if value.hydrograph_month == self.month3[newIndex]:
                if value.term == 'Short':
                    row = 0
                elif value.term == 'Medium':
                    row = 1
                else:
                    row = 2
                led = QtGui.QLineEdit(str(value.response_ratio))
                self.tblPack.setItem(row, 0, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.time_to_peak))
                self.tblPack.setItem(row, 1, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.recession_limb_ratio))
                self.tblPack.setItem(row, 2, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.initial_abstraction_depth))
                self.tblAbstraction.setItem(row, 0, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.initial_abstraction_rate))
                self.tblAbstraction.setItem(row, 1, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(value.initial_abstraction_amount))
                self.tblAbstraction.setItem(row, 2, QtGui.QTableWidgetItem(led.text()))

