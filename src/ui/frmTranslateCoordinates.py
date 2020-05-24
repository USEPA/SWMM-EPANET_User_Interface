from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtWidgets import QMessageBox, QDialog
from ui.help import HelpHandler
from ui.frmTranslateCoordinatesDesigner import Ui_frmTranslateCoordinatesDesigner
from ui.model_utility import ParseData
from core.coordinate import Coordinate
from qgis.gui import QgsProjectionSelectionDialog
import os, sys


class frmTranslateCoordinates(QDialog):
    def __init__(self, main_form, *args):
        QDialog.__init__(self, main_form)
        #self.helper = HelpHandler(self)
        #self.help_topic = "epanet/src/src/Register.htm"
        self.ui = Ui_frmTranslateCoordinatesDesigner()
        self.ui.setupUi(self)
        self.setModal(0)
        # self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        # self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        # self.toolButton.clicked.connect(self.toolButton_Clicked)
        self.ui.btnTranslate.clicked.connect(self.translate)
        self.ui.btnCancel.clicked.connect(self.cancel)
        self.ui.btnSelectCRS.clicked.connect(self.set_dst_crs)
        self.msg = ""
        self.model_layers = []
        self.pt_src_ll = Coordinate()
        self.pt_src_ur = Coordinate()
        self.pt_dst_ll = None
        self.pt_dst_ur = None
        if not args or len(args) < 2:
            self.msg = "Not enough coordinate information."
        else:
            self.set_coords_source_ll(args[0])
            self.set_coords_source_ur(args[1])

        # need to load table with selected file names
        self.GISDataFiles = {}
        self.file_filter = "Shapefile (*.shp);;All files (*.*)"
        self.data_path = ""
        if args:
            self.file_filter = args[0]
            if len(args) > 1:
                self.GISDataFiles = args[1]
        self._main_form = main_form
        self.model_map_crs_name = ""
        self.model_map_crs_unit = ""
        self.destination_crs_name = ""
        self.destination_crs_unit = ""
        self.set_from()

    def set_from(self):
        self.model = self._main_form.model
        self.model_layers = self._main_form.model_layers.all_layers
        if self.model == "EPANET":
            self.ui.chkAutoUpdate.setText("Update length of all pipes")
            pass
        elif self.model == "SWMM":
            pass

        if self._main_form and self._main_form.project:
            self.model_map_crs_name = self._main_form.project.map.crs_name
            self.model_map_crs_unit = self._main_form.project.map.crs_unit

        if self.pt_src_ll:
            self.ui.txtLL_src_x.setText(str(self.pt_src_ll.x))
            self.ui.txtLL_src_y.setText(str(self.pt_src_ll.y))
        else:
            self.ui.txtLL_src_x.setText("")
            self.ui.txtLL_src_y.setText("")

        if self.pt_src_ur:
            self.ui.txtUR_src_x.setText(str(self.pt_src_ur.x))
            self.ui.txtUR_src_y.setText(str(self.pt_src_ur.y))
        else:
            self.ui.txtUR_src_x.setText("")
            self.ui.txtUR_src_y.setText("")

        # testing data for EPANET Net1 model
        # self.ui.txtLL_dst_x.setText(str(48116663.4021))
        # self.ui.txtLL_dst_y.setText(str(-10191358.2487))
        # self.ui.txtUR_dst_x.setText(str(48127203.2619))
        # self.ui.txtUR_dst_y.setText(str(-10180815.3556))
        # testing data for SWMM Example1 model
        # self.ui.txtLL_dst_x.setText(str(48122641.7524))
        # self.ui.txtLL_dst_y.setText(str(-10179458.5428))
        # self.ui.txtUR_dst_x.setText(str(48124275.7448))
        # self.ui.txtUR_dst_y.setText(str(-10177851.1660))

    def set_coords_source_ll(self, pt_ll):
        if not pt_ll:
            return
        if isinstance(pt_ll, Coordinate):
            self.pt_src_ll.x = pt_ll.x
            self.pt_src_ll.y = pt_ll.y
        else:
            try:
                self.pt_src_ll.x = pt_ll.x()
                self.pt_src_ll.y = pt_ll.y()
                pass
            except:
                pass
        self.ui.txtLL_src_x.setText(str(self.pt_src_ll.x))
        self.ui.txtLL_src_y.setText(str(self.pt_src_ll.y))

    def set_coords_source_ur(self, pt_ur):
        if not pt_ur:
            return
        if isinstance(pt_ur, Coordinate):
            self.pt_src_ur.x = pt_ur.x
            self.pt_src_ur.y = pt_ur.y
        else:
            try:
                self.pt_src_ur.x = pt_ur.x()
                self.pt_src_ur.y = pt_ur.y()
                pass
            except:
                pass
        self.ui.txtUR_src_x.setText(str(self.pt_src_ur.x))
        self.ui.txtUR_src_y.setText(str(self.pt_src_ur.y))

    def set_coords_destination_ll(self, pt_ll):
        if not pt_ll:
            return
        if isinstance(pt_ll, Coordinate):
            self.pt_dst_ll.x = pt_ll.x
            self.pt_dst_ll.y = pt_ll.y
        else:
            try:
                self.pt_dst_ll.x = pt_ll.x()
                self.pt_dst_ll.y = pt_ll.y()
                pass
            except:
                pass

    def set_coords_destination_ur(self, pt_ur):
        if not pt_ur:
            return
        if isinstance(pt_ur, Coordinate):
            self.pt_dst_ur.x = pt_ur.x
            self.pt_dst_ur.y = pt_ur.y
        else:
            try:
                self.pt_dst_ur.x = pt_ur.x()
                self.pt_dst_ur.y = pt_ur.y()
                pass
            except:
                pass

    def check_coords(self):
        # check source LL coordinates
        new_src_LL = Coordinate()
        val, val_is_good = ParseData.floatTryParse(self.ui.txtLL_src_x.text())
        if val_is_good:
            new_src_LL.x = val
        else:
            return False
        val, val_is_good = ParseData.floatTryParse(self.ui.txtLL_src_y.text())
        if val_is_good:
            new_src_LL.y = val
        else:
            return False

        # check source UR coordinates
        new_src_UR = Coordinate()
        val, val_is_good = ParseData.floatTryParse(self.ui.txtUR_src_x.text())
        if val_is_good:
            new_src_UR.x = val
        else:
            return False
        val, val_is_good = ParseData.floatTryParse(self.ui.txtUR_src_y.text())
        if val_is_good:
            new_src_UR.y = val
        else:
            return False

        # check destination LL coordinates
        new_dst_LL = Coordinate()
        val, val_is_good = ParseData.floatTryParse(self.ui.txtLL_dst_x.text())
        if val_is_good:
            new_dst_LL.x = val
        else:
            return False
        val, val_is_good = ParseData.floatTryParse(self.ui.txtLL_dst_y.text())
        if val_is_good:
            new_dst_LL.y = val
        else:
            return False

        # check destination UR coordinates
        new_dst_UR = Coordinate()
        val, val_is_good = ParseData.floatTryParse(self.ui.txtUR_dst_x.text())
        if val_is_good:
            new_dst_UR.x = val
        else:
            return False
        val, val_is_good = ParseData.floatTryParse(self.ui.txtUR_dst_y.text())
        if val_is_good:
            new_dst_UR.y = val
        else:
            return False

        self.pt_src_ll.x = new_src_LL.x
        self.pt_src_ll.y = new_src_LL.y
        self.pt_src_ur.x = new_src_UR.x
        self.pt_src_ur.y = new_src_UR.y

        if not self.pt_dst_ll:
            self.pt_dst_ll = type(self.pt_src_ll)()
        if not self.pt_dst_ur:
            self.pt_dst_ur = type(self.pt_src_ur)()
        self.pt_dst_ll.x = new_dst_LL.x
        self.pt_dst_ll.y = new_dst_LL.y
        self.pt_dst_ur.x = new_dst_UR.x
        self.pt_dst_ur.y = new_dst_UR.y

        return True

    def set_dst_crs(self):
        try:
            frmCRS = QgsProjectionSelectionDialog(self._main_form)
            if frmCRS.exec_():
                if frmCRS.crs() is not None and frmCRS.crs().authid():
                    self.destination_crs_name = frmCRS.crs().authid()
                    self._main_form.map_widget.update_project_map_crs_info(self.destination_crs_name)
                    self._main_form.txtCrs.setText(self.destination_crs_name)
        except:
            pass

    def translate(self):
        if not self.check_coords():
            QMessageBox.information(None, "Bad Coordinates", "Invalid coordinates.")
            return

        if self.ui.rdoUnitFeet.isChecked():
            self.destination_crs_unit = "feet"
        elif self.ui.rdoUnitFeet.isChecked():
            self.destination_crs_unit = "meters"

        try:

            self._main_form.map_widget.translate_layers_coordinates(self.pt_src_ll,
                                                                    self.pt_src_ur,
                                                                    self.pt_dst_ll,
                                                                    self.pt_dst_ur)
            if self.ui.chkAutoUpdate.isChecked():
                msgBox = QMessageBox()
                msgBox.icon = self._main_form.windowIcon()
                if self.model == "EPANET":
                    msgBox.setWindowTitle("Update links length")
                    msgBox.setText("Re-calculating all links' length will change model results!\n\n"
                                   "Do you want to proceed?")
                elif self.model == "SWMM":
                    msgBox.setWindowTitle("Update links length and subcatchments area")
                    msgBox.setText("Re-calculating links' length and subcatchments' area will change model results!\n\n"
                                   "Do you want to proceed?")
                msgBox.setInformativeText(self._main_form.project.file_name)
                msgBox.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
                msgBox.setDefaultButton(QMessageBox.Cancel)
                ret = msgBox.exec_()
                if ret == QMessageBox.Ok:
                    self._main_form.map_widget.update_links_length()
                    if self._main_form.model == "SWMM":
                        self._main_form.map_widget.update_subcatchments_area(self.destination_crs_unit)
                    pass

            self._main_form.save_project_as()

            self.accept()
        except Exception as e:
            QMessageBox.information(None, "Translate failed", str(e))
            return

    def cancel(self):
        if self._main_form and self._main_form.project:
            self._main_form.project.map.crs_name = self.model_map_crs_name
            self._main_form.project.map.crs_unit = self.model_map_crs_unit
        self.reject()
