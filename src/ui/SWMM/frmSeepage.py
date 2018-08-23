from PyQt4 import QtGui
from ui.help import HelpHandler
from core.swmm.hydraulics.node import Treatment
from ui.frmGenericPropertyEditor import frmGenericPropertyEditor
from core.swmm.hydraulics.node import StorageUnit


class frmSeepage(frmGenericPropertyEditor):

    SECTION_NAME = "[STORAGE]"

    def __init__(self, main_form, node_name):
        # purposely not calling frmGenericPropertyEditor.__init__
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/green_amptinfiltrationparame.htm"
        self.setupUi(self)
        self.node_name = node_name
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.setWindowTitle('Storage Seepage Editor for Node ' + node_name)

        self.section = main_form.project.find_section("STORAGE")
        self.storage_nodes_list = self.section.value[0:]

        self.tblGeneric.horizontalHeader().hide()
        self.tblGeneric.setRowCount(3)
        self.tblGeneric.setColumnCount(1)
        props = []
        props.append('Suction Head')
        props.append('Conductivity')
        props.append('Initial Deficit')
        self.tblGeneric.setVerticalHeaderLabels(props)

        found = False
        for storage_node in self.storage_nodes_list:
            if storage_node.name == node_name:
                found = True
                led = QtGui.QLineEdit(str(storage_node.seepage_suction_head))
                self.tblGeneric.setItem(-1, 1, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(storage_node.seepage_hydraulic_conductivity))
                self.tblGeneric.setItem(0, 1, QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(storage_node.seepage_initial_moisture_deficit))
                self.tblGeneric.setItem(1, 1, QtGui.QTableWidgetItem(led.text()))
        if not found:
            led = QtGui.QLineEdit(str(0))
            self.tblGeneric.setItem(-1, 1, QtGui.QTableWidgetItem(led.text()))
            led = QtGui.QLineEdit(str(1))
            self.tblGeneric.setItem(0, 1, QtGui.QTableWidgetItem(led.text()))
            led = QtGui.QLineEdit(str(2))
            self.tblGeneric.setItem(1, 1, QtGui.QTableWidgetItem(led.text()))

        if self.lblNotes:
            self.tblGeneric.currentCellChanged.connect(self.table_currentCellChanged)

        # ## Soil capillary suction head (in or mm)
        # self.seepage_suction_head = '0'
        #
        # ## Soil saturated hydraulic conductivity (in/hr or mm/hr)
        # self.seepage_hydraulic_conductivity = '0'
        #
        # ## Initial soil moisture deficit (volume of voids / total volume)
        # self.seepage_initial_moisture_deficit = '0'

        self.resize(280,300)
        self._main_form = main_form

    def cmdOK_Clicked(self):
        node_found = False
        for storage_node in self.storage_nodes_list:
            if storage_node.name == self.node_name:
                # put this back in place
                node_found = True
                storage_node.seepage_suction_head = self.tblGeneric.item(0,0).text()
                storage_node.seepage_hydraulic_conductivity = self.tblGeneric.item(1,0).text()
                storage_node.seepage_initial_moisture_deficit = self.tblGeneric.item(2,0).text()
        if not node_found:
            # add new one
            value1 = StorageUnit()
            value1.node = self.node_name
            value1.seepage_suction_head = self.tblGeneric.item(0, 0).text()
            value1.seepage_hydraulic_conductivity = self.tblGeneric.item(1, 0).text()
            value1.seepage_initial_moisture_deficit = self.tblGeneric.item(2, 0).text()
            self.section.value.append(value1)
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def table_currentCellChanged(self):
        row = self.tblGeneric.currentRow()
        if self.lblNotes:
            if row == 0:
                self.lblNotes.setText('Soil capillary suction head (in or mm)')
            elif row == 1:
                self.lblNotes.setText('Soil saturated hydraulic conductivity (in/hr or mm/hr)')
            elif row == 2:
                self.lblNotes.setText('Initial soil moisture deficit (volume of voids / total volume)')


