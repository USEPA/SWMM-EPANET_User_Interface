import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmLIDControlsDesigner import Ui_frmLIDControls
from ui.SWMM.frmLIDUsage import frmLIDUsage
from core.swmm.hydrology.lidcontrol import LIDType


class frmLIDControls(QtGui.QMainWindow, Ui_frmLIDControls):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.btnAdd, QtCore.SIGNAL("clicked()"), self.btnAdd_Clicked)
        QtCore.QObject.connect(self.btnEdit, QtCore.SIGNAL("clicked()"), self.btnEdit_Clicked)
        QtCore.QObject.connect(self.btnDelete, QtCore.SIGNAL("clicked()"), self.btnDelete_Clicked)
        self._parent = parent
        # set for first subcatchment for now
        self.subcatchment_id = ''
        self.set_subcatchment(parent.project,'1')

    def set_subcatchment(self, project, subcatchment_id):
        # section = core.swmm.project.LIDUsage()
        section = project.find_section("LID_USAGE")
        lid_list = section.value[0:]
        # assume we want to edit the first one
        self.subcatchment_id = subcatchment_id
        self.setWindowTitle("LID Controls for Subcatchment " + subcatchment_id)
        self.tblControls.setColumnCount(self.tblControls.columnCount()+5)  # add for hidden columns
        lid_count = -1
        for value in lid_list:
            if value.subcatchment_name == subcatchment_id:
                # this is the subcatchment we want to edit
                lid_count += 1
                self.tblControls.setRowCount(lid_count+1)
                led = QtGui.QLineEdit(value.control_name)
                self.tblControls.setItem(lid_count,0,QtGui.QTableWidgetItem(str(led.text())))

                lid_name = value.control_name
                lid_control_section = self._parent.project.find_section("LID_CONTROLS")
                lid_control_list = lid_control_section.value[0:]
                for lid in lid_control_list:
                    if lid.control_name == value.control_name:
                        # this is the lid
                        if lid.lid_type == LIDType.BC:
                            lid_name = 'Bio-Retention'
                        elif lid.lid_type == LIDType.RG:
                            lid_name = 'Rain Garden'
                        elif lid.lid_type == LIDType.GR:
                            lid_name = 'Green Roof'
                        elif lid.lid_type == LIDType.IT:
                            lid_name = 'Infiltration Trench'
                        elif lid.lid_type == LIDType.PP:
                            lid_name = 'Permeable Pavement'
                        elif lid.lid_type == LIDType.RB:
                            lid_name = 'Rain Barrel'
                        elif lid.lid_type == LIDType.RD:
                            lid_name = 'Rooftop Disconnection'
                        elif lid.lid_type == LIDType.VS:
                            lid_name = 'Vegetative Swale'
                led = QtGui.QLineEdit(lid_name)
                self.tblControls.setItem(lid_count,1,QtGui.QTableWidgetItem(str(led.text())))

                area = float(value.number_replicate_units) * float(value.area_each_unit)
                units = 1
                if units == 1:
                    conversion_factor = 43560.0
                else:
                    conversion_factor = 10000.0

                subcatchment_area = core.swmm.project.Subcatchment(subcatchment_id).area
                if len(subcatchment_area) < 1:
                    subcatchment_area = 10.0
                elif subcatchment_area <= 0:
                    subcatchment_area = 10.0

                subcatchment_area = float(subcatchment_area) * conversion_factor

                led = QtGui.QLineEdit('{:5.3f}'.format(100.0 * area/subcatchment_area))
                self.tblControls.setItem(lid_count,2,QtGui.QTableWidgetItem(str(led.text())))

                led = QtGui.QLineEdit(str(value.percent_impervious_area_treated))
                self.tblControls.setItem(lid_count,3,QtGui.QTableWidgetItem(str(led.text())))

                led = QtGui.QLineEdit(str(value.detailed_report_file))
                self.tblControls.setItem(lid_count,4,QtGui.QTableWidgetItem(str(led.text())))

                # store the other param values in hidden columns
                led = QtGui.QLineEdit(str(value.number_replicate_units))
                self.tblControls.setItem(lid_count,5,QtGui.QTableWidgetItem(str(led.text())))
                led = QtGui.QLineEdit(str(value.area_each_unit))
                self.tblControls.setItem(lid_count,6,QtGui.QTableWidgetItem(str(led.text())))
                led = QtGui.QLineEdit(str(value.top_width_overland_flow_surface))
                self.tblControls.setItem(lid_count,7,QtGui.QTableWidgetItem(str(led.text())))
                led = QtGui.QLineEdit(str(value.percent_initially_saturated))
                self.tblControls.setItem(lid_count,8,QtGui.QTableWidgetItem(str(led.text())))
                led = QtGui.QLineEdit(str(value.send_outflow_pervious_area))
                self.tblControls.setItem(lid_count,9,QtGui.QTableWidgetItem(str(led.text())))

        self.tblControls.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tblControls.setColumnHidden(5,True)
        self.tblControls.setColumnHidden(6,True)
        self.tblControls.setColumnHidden(7,True)
        self.tblControls.setColumnHidden(8,True)
        self.tblControls.setColumnHidden(9,True)

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("LID_USAGE")
        lid_list = section.value[0:]
        lid_count = -1
        for value in lid_list:
            if value.subcatchment_name == self.subcatchment_id:
                lid_count += 1
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def btnAdd_Clicked(self):
        self._frmLIDUsage = frmLIDUsage(self._parent)
        # add to this subcatchment
        self._frmLIDUsage.set_add(self._parent.project,self.subcatchment_id)
        self._frmLIDUsage.show()

    def btnEdit_Clicked(self):
        self._frmLIDUsage = frmLIDUsage(self._parent)
        row = self.tblControls.currentRow()
        lid_selected = str(self.tblControls.item(row,0).text())
        # edit the lid for this subcatchment and this lid name
        self._frmLIDUsage.set_edit(self._parent.project, self, row, lid_selected)
        self._frmLIDUsage.show()

    def btnDelete_Clicked(self):
        row = self.tblControls.currentRow()
        self.tblControls.removeRow(row)
