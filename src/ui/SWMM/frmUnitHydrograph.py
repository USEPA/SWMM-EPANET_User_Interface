import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmUnitHydrographDesigner import Ui_frmUnitHydrograph


class frmUnitHydrograph(QtGui.QMainWindow, Ui_frmUnitHydrograph):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboHydrograph.currentIndexChanged.connect(self.cboHydrograph_currentIndexChanged)
        self._parent = parent
        self.hydrograph_id = ''
        # set for first unit hydrograph group for now
        self.set_from(parent.project,'uh')

    def set_from(self, project, hydrograph_id):
        # section = core.swmm.project.UnitHydrograph
        section = project.find_section("HYDROGRAPHS")
        hydrograph_list = section.value[0:]
        # assume we want to edit the first one
        self.hydrograph_id = hydrograph_id
        for hydrograph in hydrograph_list:
            if hydrograph.group_name: # == hydrograph_id
                # this is the unit hydrograph group we want to edit
                self.txtGroup.setText(hydrograph.group_name)

                self.cboHydrograph.setCurrentIndex(0)
                for value in hydrograph.value:
                    if value.hydrograph_month == 'All':
                        # this is one we want to load
                        self.cboHydrograph.setItemText(0,"All Months (*)")
                        row = 2
                        if value.term == 'Short':
                            row = 0
                        elif value.term == 'Medium':
                            row = 1
                        led = QtGui.QLineEdit(str(value.response_ratio))
                        self.tblPack.setItem(row,0,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.time_to_peak))
                        self.tblPack.setItem(row,1,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.recession_limb_ratio))
                        self.tblPack.setItem(row,2,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.initial_abstraction_depth))
                        self.tblAbstraction.setItem(row,0,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.initial_abstraction_rate))
                        self.tblAbstraction.setItem(row,1,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.initial_abstraction_amount))
                        self.tblAbstraction.setItem(row,2,QtGui.QTableWidgetItem(led.text()))
                    elif value.hydrograph_month == 'Jan':
                        self.cboHydrograph.setItemText(1,"January (*)")
                    elif value.hydrograph_month == 'Feb':
                        self.cboHydrograph.setItemText(2,"February (*)")
                    elif value.hydrograph_month == 'Mar':
                        self.cboHydrograph.setItemText(3,"March (*)")
                    elif value.hydrograph_month == 'Apr':
                        self.cboHydrograph.setItemText(4,"April (*)")
                    elif value.hydrograph_month == 'May':
                        self.cboHydrograph.setItemText(5,"May (*)")
                    elif value.hydrograph_month == 'Jun':
                        self.cboHydrograph.setItemText(6,"June (*)")
                    elif value.hydrograph_month == 'Jul':
                        self.cboHydrograph.setItemText(7,"July (*)")
                    elif value.hydrograph_month == 'Aug':
                        self.cboHydrograph.setItemText(8,"August (*)")
                    elif value.hydrograph_month == 'Sep':
                        self.cboHydrograph.setItemText(9,"September (*)")
                    elif value.hydrograph_month == 'Oct':
                        self.cboHydrograph.setItemText(10,"October (*)")
                    elif value.hydrograph_month == 'Nov':
                        self.cboHydrograph.setItemText(11,"November (*)")
                    elif value.hydrograph_month == 'Dec':
                        self.cboHydrograph.setItemText(12,"December (*)")

                # code to set rain gage combo, to be implemented with rain gages
                rain_section = project.find_section("RAINGAGES")
                rain_list = rain_section.value[0:]
                self.cboRain.clear()
                selected_index = 0
                # for value in rain_list:
                    # self.cboRain.addItem(value.name)
                    # if value.name == hydrograph.rain_gage_id:
                    #     selected_index = int(self.cboRain.count())-1
                    #     self.cboRain.setCurrentIndex(selected_index)

    def cmdOK_Clicked(self):
        section = self._parent.project.title
        section.title = self.txtTitle.toPlainText()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboHydrograph_currentIndexChanged(self, newIndex):
        led = QtGui.QLineEdit('')
        self.tblPack.setItem(0,0,QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(0,1,QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(0,2,QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(0,0,QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(0,1,QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(0,2,QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(1,0,QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(1,1,QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(1,2,QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(1,0,QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(1,1,QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(1,2,QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(2,0,QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(2,1,QtGui.QTableWidgetItem(led.text()))
        self.tblPack.setItem(2,2,QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(2,0,QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(2,1,QtGui.QTableWidgetItem(led.text()))
        self.tblAbstraction.setItem(2,2,QtGui.QTableWidgetItem(led.text()))
        section = self._parent.project.find_section("HYDROGRAPHS")
        hydrograph_list = section.value[0:]
        for hydrograph in hydrograph_list:
            if hydrograph.group_name == self.hydrograph_id:
                # this is the unit hydrograph group we want to edit
                for value in hydrograph.value:
                    if (value.hydrograph_month == 'All' and newIndex == 0) or \
                            (value.hydrograph_month == 'Jan' and newIndex == 1) or \
                            (value.hydrograph_month == 'Feb' and newIndex == 2) or \
                            (value.hydrograph_month == 'Mar' and newIndex == 3) or \
                            (value.hydrograph_month == 'Apr' and newIndex == 4) or \
                            (value.hydrograph_month == 'May' and newIndex == 5) or \
                            (value.hydrograph_month == 'Jun' and newIndex == 6) or \
                            (value.hydrograph_month == 'Jul' and newIndex == 7) or \
                            (value.hydrograph_month == 'Aug' and newIndex == 8) or \
                            (value.hydrograph_month == 'Sep' and newIndex == 9) or \
                            (value.hydrograph_month == 'Oct' and newIndex == 10) or \
                            (value.hydrograph_month == 'Nov' and newIndex == 11) or \
                            (value.hydrograph_month == 'Dec' and newIndex == 12):
                        row = 2
                        if value.term == 'Short':
                            row = 0
                        elif value.term == 'Medium':
                            row = 1
                        led = QtGui.QLineEdit(str(value.response_ratio))
                        self.tblPack.setItem(row,0,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.time_to_peak))
                        self.tblPack.setItem(row,1,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.recession_limb_ratio))
                        self.tblPack.setItem(row,2,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.initial_abstraction_depth))
                        self.tblAbstraction.setItem(row,0,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.initial_abstraction_rate))
                        self.tblAbstraction.setItem(row,1,QtGui.QTableWidgetItem(led.text()))
                        led = QtGui.QLineEdit(str(value.initial_abstraction_amount))
                        self.tblAbstraction.setItem(row,2,QtGui.QTableWidgetItem(led.text()))

