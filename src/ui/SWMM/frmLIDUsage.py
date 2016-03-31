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
        # self.set_from(parent.parent.project)
        self.subcatchment_id = ''

    def set_add(self, project, subcatchment_id):
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

    def set_edit(self, project, row_id, lid_selected,
                 number_replicate_units, area_each_unit, top_width_overland_flow_surface,
                 percent_initially_saturated, percent_impervious_area_treated,
                 detailed_report_file, send_outflow_pervious_area):
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

        # number_replicate_units = self.parent.tblControls.item(row_id,5).text()
        self.lblPercent.setText('0.000')
        self.spxUnits.setValue(int(number_replicate_units))
        self.txtArea.setText(area_each_unit)
        self.txtWidth.setText(top_width_overland_flow_surface)
        self.txtSat.setText(percent_initially_saturated)
        self.txtTreated.setText(percent_impervious_area_treated)
        # self.txtDrain.setText('')
        self.txtFile.setText(detailed_report_file)
        # self.cbkReturn.setChecked(send_outflow_pervious_area)
        # self.cbxFull

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("CONTROLS")
        section.set_text(str(self.txtControls.toPlainText()))
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



