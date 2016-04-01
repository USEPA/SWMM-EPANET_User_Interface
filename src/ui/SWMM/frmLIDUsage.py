import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from core.swmm.hydrology.lidcontrol import LIDType
from ui.SWMM.frmLIDUsageDesigner import Ui_frmLIDUsage


class frmLIDUsage(QtGui.QMainWindow, Ui_frmLIDUsage):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self._parent = parent
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboLIDControl.currentIndexChanged.connect(self.cboLIDControl_currentIndexChanged)
        self.spxUnits.valueChanged.connect(self.spxUnits_valueChanged)
        self.txtArea.textChanged.connect(self.txtArea_textChanged)
        self.cbxFull.stateChanged.connect(self.cbxFull_stateChanged)
        self.btnFile.clicked.connect(self.btnFile_clicked)
        self.btnClear.clicked.connect(self.btnClear_clicked)
        # self.set_from(parent.parent.project)
        self.subcatchment_id = ''
        self.row_id = -1

    def set_add(self, project, parent_form, subcatchment_id):
        self.parent_form = parent_form
        section = project.find_section("LID_CONTROLS")
        lid_list = section.value[0:]
        self.cboLIDControl.clear()
        for lid in lid_list:
            self.cboLIDControl.addItem(lid.control_name)
        self.subcatchment_id = subcatchment_id
        self.lblPercent.setText('0.000')
        self.spxUnits.setValue(1)
        self.txtArea.setText('0')
        self.txtWidth.setText('0')
        self.txtSat.setText('0')
        self.txtTreated.setText('0')
        self.txtDrain.setText('')
        self.txtFile.setText('')

    def set_edit(self, project, parent_form, row_id, lid_selected, subcatchment_id):
        self.row_id = row_id
        self.parent_form = parent_form
        section = project.find_section("LID_CONTROLS")
        lid_list = section.value[0:]
        self.cboLIDControl.clear()
        selected_index = 0
        item_count = -1
        for lid in lid_list:
            self.cboLIDControl.addItem(lid.control_name)
            item_count += 1
            if lid_selected == lid.control_name:
                selected_index = item_count
        self.cboLIDControl.setCurrentIndex(selected_index)
        self.subcatchment_id = subcatchment_id

        number_replicate_units = parent_form.tblControls.item(row_id,5).text()
        area_each_unit = parent_form.tblControls.item(row_id,6).text()
        top_width_overland_flow_surface = parent_form.tblControls.item(row_id,7).text()
        percent_initially_saturated = parent_form.tblControls.item(row_id,8).text()
        percent_impervious_area_treated = parent_form.tblControls.item(row_id,3).text()
        detailed_report_file = parent_form.tblControls.item(row_id,4).text()
        send_outflow_pervious_area = parent_form.tblControls.item(row_id,9).text()
        subcatchment_drains_to = parent_form.tblControls.item(row_id,10).text()

        self.lblPercent.setText('0.000')
        self.spxUnits.setValue(int(number_replicate_units))
        self.txtArea.setText(area_each_unit)
        self.txtWidth.setText(top_width_overland_flow_surface)
        self.txtSat.setText(percent_initially_saturated)
        self.txtTreated.setText(percent_impervious_area_treated)
        self.txtDrain.setText(subcatchment_drains_to)
        self.txtFile.setText(detailed_report_file)
        if int(send_outflow_pervious_area) > 0:
          self.cbkReturn.setChecked(True)
        else:
          self.cbkReturn.setChecked(False)
        # self.cbxFull
        self.calculate_area()

    def cmdOK_Clicked(self):
        lid_control = self.cboLIDControl.currentText()
        percent_impervious_area_treated =  self.txtTreated.text()
        detailed_report_file = self.txtFile.text()
        number_replicate_units = self.spxUnits.value()
        area_each_unit = self.txtArea.text()
        top_width_overland_flow_surface = self.txtWidth.text()
        percent_initially_saturated = self.txtSat.text()
        subcatchment_drains_to = self.txtDrain.text()
        if self.cbkReturn.isChecked():
            send_outflow_pervious_area = 1
        else:
            send_outflow_pervious_area = 0

        if self.row_id < 0:
            # this is a new lid usage, put after all others
            self.row_id = self.parent_form.tblControls.rowCount()
            self.parent_form.tblControls.setRowCount(self.parent_form.tblControls.rowCount()+1)

        if self.row_id >= 0:
            # editing an existing lid usage, put back
            led = QtGui.QLineEdit(lid_control)
            self.parent_form.tblControls.setItem(self.row_id,0,QtGui.QTableWidgetItem(str(led.text())))
            led = QtGui.QLineEdit(percent_impervious_area_treated)
            self.parent_form.tblControls.setItem(self.row_id,3,QtGui.QTableWidgetItem(str(led.text())))
            led = QtGui.QLineEdit(detailed_report_file)
            self.parent_form.tblControls.setItem(self.row_id,4,QtGui.QTableWidgetItem(str(led.text())))
            led = QtGui.QLineEdit(str(number_replicate_units))
            self.parent_form.tblControls.setItem(self.row_id,5,QtGui.QTableWidgetItem(str(led.text())))
            led = QtGui.QLineEdit(area_each_unit)
            self.parent_form.tblControls.setItem(self.row_id,6,QtGui.QTableWidgetItem(str(led.text())))
            led = QtGui.QLineEdit(top_width_overland_flow_surface)
            self.parent_form.tblControls.setItem(self.row_id,7,QtGui.QTableWidgetItem(str(led.text())))
            led = QtGui.QLineEdit(percent_initially_saturated)
            self.parent_form.tblControls.setItem(self.row_id,8,QtGui.QTableWidgetItem(str(led.text())))
            led = QtGui.QLineEdit(str(send_outflow_pervious_area))
            self.parent_form.tblControls.setItem(self.row_id,9,QtGui.QTableWidgetItem(str(led.text())))
            led = QtGui.QLineEdit(subcatchment_drains_to)
            self.parent_form.tblControls.setItem(self.row_id,10,QtGui.QTableWidgetItem(str(led.text())))

            # recalculate area and lid name
            self.parent_form.SetLongLIDName(lid_control,self.row_id)
            self.parent_form.SetAreaTerm(self.subcatchment_id, self.row_id, number_replicate_units, area_each_unit)

        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboLIDControl_currentIndexChanged(self, newIndex):
        selected_text = self.cboLIDControl.currentText()
        section = self._parent.project.find_section("LID_CONTROLS")
        lid_list = section.value[0:]
        for lid in lid_list:
            if lid.control_name == selected_text:
                # this is the lid control, get its type
                if lid.lid_type == LIDType.BC:
                    self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/1237LID.png"))
                elif lid.lid_type == LIDType.RG:
                    self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/1237LID.png"))
                elif lid.lid_type == LIDType.GR:
                    self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/1237LID.png"))
                elif lid.lid_type == LIDType.IT:
                    self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/4LID.png"))
                elif lid.lid_type == LIDType.PP:
                    self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/5LID.png"))
                elif lid.lid_type == LIDType.RB:
                    self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/6LID.png"))
                elif lid.lid_type == LIDType.RD:
                    self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/1237LID.png"))
                elif lid.lid_type == LIDType.VS:
                    self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/8LID.png"))

    def calculate_area(self):
        units = 1
        if units == 1:
            conversion_factor = 43560.0
        else:
            conversion_factor = 10000.0

        subcatchment_area = core.swmm.project.Subcatchment(self.subcatchment_id).area
        if len(subcatchment_area) < 1:
            subcatchment_area = 10.0
        elif subcatchment_area <= 0:
            subcatchment_area = 10.0

        subcatchment_area = float(subcatchment_area) * conversion_factor

        if self.cbxFull.isChecked():
            area_each_unit = subcatchment_area / float(self.spxUnits.value())
            self.txtArea.setText('{:5.2f}'.format(area_each_unit))
            self.lblPercent.setText('100.0')
        else:
            number_replicate_units = self.spxUnits.value()
            area_each_unit = self.txtArea.text()
            if len(area_each_unit) > 0:
                area = float(number_replicate_units) * float(area_each_unit)
                self.lblPercent.setText('{:5.3f}'.format(100.0 * area/subcatchment_area))

    def spxUnits_valueChanged(self):
        self.calculate_area()

    def txtArea_textChanged(self):
        self.calculate_area()

    def cbxFull_stateChanged(self):
        self.calculate_area()

    def btnFile_clicked(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, "LID Report File", '',
                                                      "LID Report Files (*.txt);;All files (*.*)")
        if file_name:
            self.txtFile.setText(file_name)

    def btnClear_clicked(self):
        self.txtFile.setText('')


