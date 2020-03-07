import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTableWidgetItem
from core.swmm.hydrology.lidcontrol import LIDType
from ui.SWMM.frmLIDDesigner import Ui_frmLID
from core.swmm.hydrology.lidcontrol import LIDControl
from core.swmm.curves import CurveType


class frmLID(QMainWindow, Ui_frmLID):
    def __init__(self, main_form, edit_these, new_item):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/lidcontroleditor.htm"
        self.setupUi(self)
        self.cboLIDType.clear()
        self.cboLIDType.addItems(("Bio-Retention Cell","Rain Garden","Green Roof","Infiltration Trench","Permeable Pavement", "Rain Barrel", "Rooftop Disconnection", "Vegetative Swale"))
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.cboLIDType.currentIndexChanged.connect(self.cboLIDType_currentIndexChanged)
        self._main_form = main_form
        self.project = main_form.project
        self.section = self.project.lid_controls
        self.new_item = new_item

        self.tblPollutant.setColumnCount(1)
        self.tblPollutant.setHorizontalHeaderLabels(["% Removal"])
        pollutant_count = -1
        self.pollutant_list = self.project.pollutants.value[0:]
        pollutant_names = []
        for pollutant in self.pollutant_list:
            pollutant_names.append(pollutant.name)
        self.tblPollutant.setRowCount(len(pollutant_names))
        self.tblPollutant.setVerticalHeaderLabels(pollutant_names)
        for pollutant in self.pollutant_list:
            pollutant_count += 1
            self.tblPollutant.setItem(pollutant_count, 0, QTableWidgetItem(''))

        # # for curves, show available curves
        # curves_section = self.project.find_section("CURVES")
        # curves_list = curves_section.value[0:]
        # for curve in curves_list:
        #     if curve.curve_type == CurveType.CONTROL:
        #         self.cboCurve.addItem(curve.name)

        if new_item:
            self.lid = new_item
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):  # edit first lid control if given a list
                if not isinstance(edit_these[0], LIDControl):
                    self.lid = self.section.value[edit_these[0]]
                else:
                    self.lid = edit_these[0]
                self.set_from(edit_these[0])
            else:
                self.lid = edit_these
                self.set_from(edit_these)

        if (main_form.program_settings.value("Geometry/" + "frmLID_geometry") and
                main_form.program_settings.value("Geometry/" + "frmLID_state")):
            self.restoreGeometry(main_form.program_settings.value("Geometry/" + "frmLID_geometry",
                                                                  self.geometry(), type=QtCore.QByteArray))
            self.restoreState(main_form.program_settings.value("Geometry/" + "frmLID_state",
                                                               self.windowState(), type=QtCore.QByteArray))

    def set_from(self, lid):
        if not isinstance(lid, LIDControl):
            lid = self.section.value[lid]
        if isinstance(lid, LIDControl):
            self.editing_item = lid

            self.cboLIDType_currentIndexChanged(0)

            self.txtName.setText(lid.name)
            if lid.lid_type == LIDType.BC:
                self.cboLIDType.setCurrentIndex(0)
                lid.has_surface_layer = True
                lid.has_pavement_layer = False
                lid.has_soil_layer = True
                lid.has_storage_layer = True
                lid.has_underdrain_system = True
                lid.has_drainmat_system = False
                lid.has_pollutant_removals = True
            elif lid.lid_type == LIDType.RG:
                self.cboLIDType.setCurrentIndex(1)
                lid.has_surface_layer = True
                lid.has_pavement_layer = False
                lid.has_soil_layer = True
                lid.has_storage_layer = False
                lid.has_underdrain_system = False
                lid.has_drainmat_system = False
                lid.has_pollutant_removals = False
            elif lid.lid_type == LIDType.GR:
                self.cboLIDType.setCurrentIndex(2)
                lid.has_surface_layer = True
                lid.has_pavement_layer = False
                lid.has_soil_layer = True
                lid.has_storage_layer = False
                lid.has_underdrain_system = False
                lid.has_drainmat_system = True
                lid.has_pollutant_removals = False
            elif lid.lid_type == LIDType.IT:
                self.cboLIDType.setCurrentIndex(3)
                lid.has_surface_layer = True
                lid.has_pavement_layer = False
                lid.has_soil_layer = False
                lid.has_storage_layer = True
                lid.has_underdrain_system = True
                lid.has_drainmat_system = False
                lid.has_pollutant_removals = True
            elif lid.lid_type == LIDType.PP:
                self.cboLIDType.setCurrentIndex(4)
                lid.has_surface_layer = True
                lid.has_pavement_layer = True
                lid.has_soil_layer = True
                lid.has_storage_layer = True
                lid.has_underdrain_system = True
                lid.has_drainmat_system = False
                lid.has_pollutant_removals = True
            elif lid.lid_type == LIDType.RB:
                self.cboLIDType.setCurrentIndex(5)
                lid.has_surface_layer = False
                lid.has_pavement_layer = False
                lid.has_soil_layer = False
                lid.has_storage_layer = True
                lid.has_underdrain_system = True
                lid.has_drainmat_system = False
                lid.has_pollutant_removals = True
            elif lid.lid_type == LIDType.RD:
                self.cboLIDType.setCurrentIndex(6)
                lid.has_surface_layer = True
                lid.has_pavement_layer = False
                lid.has_soil_layer = False
                lid.has_storage_layer = False
                lid.has_underdrain_system = True
                lid.has_drainmat_system = False
                lid.has_pollutant_removals = False
            elif lid.lid_type == LIDType.VS:
                self.cboLIDType.setCurrentIndex(7)
                lid.has_surface_layer = True
                lid.has_pavement_layer = False
                lid.has_soil_layer = False
                lid.has_storage_layer = False
                lid.has_underdrain_system = False
                lid.has_drainmat_system = False
                lid.has_pollutant_removals = False

            if lid.has_surface_layer:
                self.txtSurface1.setText(lid.surface_layer_storage_depth)
                self.txtSurface2.setText(lid.surface_layer_vegetative_cover_fraction)
                self.txtSurface3.setText(lid.surface_layer_surface_roughness)
                self.txtSurface4.setText(lid.surface_layer_surface_slope)
                self.txtSurface5.setText(lid.surface_layer_swale_side_slope)
            if lid.has_pavement_layer:
                self.txtPavement1.setText(lid.pavement_layer_thickness)
                self.txtPavement2.setText(lid.pavement_layer_void_ratio)
                self.txtPavement3.setText(lid.pavement_layer_impervious_surface_fraction)
                self.txtPavement4.setText(lid.pavement_layer_permeability)
                self.txtPavement5.setText(lid.pavement_layer_clogging_factor)
                self.txtRegeneration.setText(lid.pavement_layer_regeneration_interval)
                self.txtFraction.setText(lid.pavement_layer_regeneration_fraction)
            if lid.has_soil_layer:
                self.txtSoil1.setText(lid.soil_layer_thickness)
                self.txtSoil2.setText(lid.soil_layer_porosity)
                self.txtSoil3.setText(lid.soil_layer_field_capacity)
                self.txtSoil4.setText(lid.soil_layer_wilting_point)
                self.txtSoil5.setText(lid.soil_layer_conductivity)
                self.txtSoil6.setText(lid.soil_layer_conductivity_slope)
                self.txtSoil7.setText(lid.soil_layer_suction_head)
            if lid.has_storage_layer:
                self.txtStorage1.setText(lid.storage_layer_height)
                self.txtStorage2.setText(lid.storage_layer_void_ratio)
                self.txtStorage3.setText(lid.storage_layer_filtration_rate)
                self.txtStorage4.setText(lid.storage_layer_clogging_factor)
            if lid.has_underdrain_system:
                self.txtDrain1.setText(lid.drain_coefficient)
                self.txtDrain2.setText(lid.drain_exponent)
                self.txtDrain3.setText(lid.drain_offset_height)
                self.txtDrain4.setText(lid.drain_delay)
                self.txtOpen.setText(lid.drain_open_level)
                self.txtClosed.setText(lid.drain_closed_level)

                # for curves, show available curves
                self.cboCurve.addItem('')
                curves_section = self.project.find_section("CURVES")
                curves_list = curves_section.value[0:]
                selected_index = 0
                for curve in curves_list:
                    if curve.curve_type == CurveType.CONTROL:
                        self.cboCurve.addItem(curve.name)
                        if lid.drain_control_curve == curve.name:
                            selected_index = int(self.cboCurve.count()) - 1
                self.cboCurve.setCurrentIndex(selected_index)

            if lid.has_drainmat_system:
                self.txtDrain1.setText(lid.drainmat_thickness)
                self.txtDrain2.setText(lid.drainmat_void_fraction)
                self.txtDrain3.setText(lid.drainmat_roughness)
            if lid.has_pollutant_removals:
                if len(self.pollutant_list) > 0:
                    self.tblPollutant.setItem(-1, 1, QTableWidgetItem(lid.removal_removal1))
                if len(self.pollutant_list) > 1:
                    self.tblPollutant.setItem(0, 1, QTableWidgetItem(lid.removal_removal2))
                if len(self.pollutant_list) > 2:
                    self.tblPollutant.setItem(1, 1, QTableWidgetItem(lid.removal_removal3))
                if len(self.pollutant_list) > 3:
                    self.tblPollutant.setItem(2, 1, QTableWidgetItem(lid.removal_removal4))
                if len(self.pollutant_list) > 4:
                    self.tblPollutant.setItem(3, 1, QTableWidgetItem(lid.removal_removal5))


    def cmdOK_Clicked(self):
        oldname = self.editing_item.name
        self.editing_item.name = self.txtName.text()

        orig_lid_type = self.editing_item.lid_type
        orig_surface_layer_storage_depth = self.editing_item.surface_layer_storage_depth
        orig_surface_layer_vegetative_cover_fraction = self.editing_item.surface_layer_vegetative_cover_fraction
        orig_surface_layer_surface_roughness = self.editing_item.surface_layer_surface_roughness
        orig_surface_layer_surface_slope = self.editing_item.surface_layer_surface_slope
        orig_surface_layer_swale_side_slope = self.editing_item.surface_layer_swale_side_slope
        orig_pavement_layer_thickness = self.editing_item.pavement_layer_thickness
        orig_pavement_layer_void_ratio = self.editing_item.pavement_layer_void_ratio
        orig_pavement_layer_impervious_surface_fraction = self.editing_item.pavement_layer_impervious_surface_fraction
        orig_pavement_layer_permeability = self.editing_item.pavement_layer_permeability
        orig_pavement_layer_clogging_factor = self.editing_item.pavement_layer_clogging_factor
        orig_pavement_layer_regeneration_interval = self.editing_item.pavement_layer_regeneration_interval
        orig_pavement_layer_regeneration_fraction = self.editing_item.pavement_layer_regeneration_fraction
        orig_soil_layer_thickness = self.editing_item.soil_layer_thickness
        orig_soil_layer_porosity = self.editing_item.soil_layer_porosity
        orig_soil_layer_field_capacity = self.editing_item.soil_layer_field_capacity
        orig_soil_layer_wilting_point = self.editing_item.soil_layer_wilting_point
        orig_soil_layer_conductivity = self.editing_item.soil_layer_conductivity
        orig_soil_layer_conductivity_slope = self.editing_item.soil_layer_conductivity_slope
        orig_soil_layer_suction_head = self.editing_item.soil_layer_suction_head
        orig_storage_layer_height = self.editing_item.storage_layer_height
        orig_storage_layer_void_ratio = self.editing_item.storage_layer_void_ratio
        orig_storage_layer_filtration_rate = self.editing_item.storage_layer_filtration_rate
        orig_storage_layer_clogging_factor = self.editing_item.storage_layer_clogging_factor
        orig_drain_coefficient = self.editing_item.drain_coefficient
        orig_drain_exponent = self.editing_item.drain_exponent
        orig_drain_offset_height = self.editing_item.drain_offset_height
        orig_drain_delay = self.editing_item.drain_delay
        orig_drain_open_level = self.editing_item.drain_open_level
        orig_drain_closed_level = self.editing_item.drain_closed_level
        orig_drain_control_curve = self.editing_item.drain_control_curve
        orig_drainmat_thickness = self.editing_item.drainmat_thickness
        orig_drainmat_void_fraction = self.editing_item.drainmat_void_fraction
        orig_drainmat_roughness = self.editing_item.drainmat_roughness
        orig_removal_removal1 = self.editing_item.removal_removal1
        orig_removal_removal2 = self.editing_item.removal_removal2
        orig_removal_removal3 = self.editing_item.removal_removal3
        orig_removal_removal4 = self.editing_item.removal_removal4
        orig_removal_removal5 = self.editing_item.removal_removal5

        if self.cboLIDType.currentIndex() == 0:
            self.editing_item.lid_type = LIDType.BC
            self.editing_item.has_surface_layer = True
            self.editing_item.has_pavement_layer = False
            self.editing_item.has_soil_layer = True
            self.editing_item.has_storage_layer = True
            self.editing_item.has_underdrain_system = True
            self.editing_item.has_drainmat_system = False
            self.editing_item.has_pollutant_removals = True
        elif self.cboLIDType.currentIndex() == 1:
            self.editing_item.lid_type = LIDType.RG
            self.editing_item.has_surface_layer = True
            self.editing_item.has_pavement_layer = False
            self.editing_item.has_soil_layer = True
            self.editing_item.has_storage_layer = False
            self.editing_item.has_underdrain_system = False
            self.editing_item.has_drainmat_system = False
            self.editing_item.has_pollutant_removals = False
        elif self.cboLIDType.currentIndex() == 2:
            self.editing_item.lid_type = LIDType.GR
            self.editing_item.has_surface_layer = True
            self.editing_item.has_pavement_layer = False
            self.editing_item.has_soil_layer = True
            self.editing_item.has_storage_layer = False
            self.editing_item.has_underdrain_system = False
            self.editing_item.has_drainmat_system = True
            self.editing_item.has_pollutant_removals = False
        elif self.cboLIDType.currentIndex() == 3:
            self.editing_item.lid_type = LIDType.IT
            self.editing_item.has_surface_layer = True
            self.editing_item.has_pavement_layer = False
            self.editing_item.has_soil_layer = False
            self.editing_item.has_storage_layer = True
            self.editing_item.has_underdrain_system = True
            self.editing_item.has_drainmat_system = False
            self.editing_item.has_pollutant_removals = True
        elif self.cboLIDType.currentIndex() == 4:
            self.editing_item.lid_type = LIDType.PP
            self.editing_item.has_surface_layer = True
            self.editing_item.has_pavement_layer = True
            self.editing_item.has_soil_layer = True
            self.editing_item.has_storage_layer = True
            self.editing_item.has_underdrain_system = True
            self.editing_item.has_drainmat_system = False
            self.editing_item.has_pollutant_removals = True
        elif self.cboLIDType.currentIndex() == 5:
            self.editing_item.lid_type = LIDType.RB
            self.editing_item.has_surface_layer = False
            self.editing_item.has_pavement_layer = False
            self.editing_item.has_soil_layer = False
            self.editing_item.has_storage_layer = True
            self.editing_item.has_underdrain_system = True
            self.editing_item.has_drainmat_system = False
            self.editing_item.has_pollutant_removals = True
        elif self.cboLIDType.currentIndex() == 6:
            self.editing_item.lid_type = LIDType.RD
            self.editing_item.has_surface_layer = True
            self.editing_item.has_pavement_layer = False
            self.editing_item.has_soil_layer = False
            self.editing_item.has_storage_layer = False
            self.editing_item.has_underdrain_system = True
            self.editing_item.has_drainmat_system = False
            self.editing_item.has_pollutant_removals = False
        elif self.cboLIDType.currentIndex() == 7:
            self.editing_item.lid_type = LIDType.VS
            self.editing_item.has_surface_layer = True
            self.editing_item.has_pavement_layer = False
            self.editing_item.has_soil_layer = False
            self.editing_item.has_storage_layer = False
            self.editing_item.has_underdrain_system = False
            self.editing_item.has_drainmat_system = False
            self.editing_item.has_pollutant_removals = False

        if self.editing_item.has_surface_layer:
            if self.cboLIDType.currentIndex() == 6:
                self.editing_item.surface_layer_storage_depth = self.txtSurface1.text()
                self.editing_item.surface_layer_surface_roughness = self.txtSurface2.text()
                self.editing_item.surface_layer_surface_slope = self.txtSurface3.text()
            else:
                self.editing_item.surface_layer_storage_depth = self.txtSurface1.text()
                self.editing_item.surface_layer_vegetative_cover_fraction = self.txtSurface2.text()
                self.editing_item.surface_layer_surface_roughness = self.txtSurface3.text()
                self.editing_item.surface_layer_surface_slope = self.txtSurface4.text()
                self.editing_item.surface_layer_swale_side_slope = self.txtSurface5.text()
        if self.editing_item.has_pavement_layer:
            self.editing_item.pavement_layer_thickness = self.txtPavement1.text()
            self.editing_item.pavement_layer_void_ratio = self.txtPavement2.text()
            self.editing_item.pavement_layer_impervious_surface_fraction = self.txtPavement3.text()
            self.editing_item.pavement_layer_permeability = self.txtPavement4.text()
            self.editing_item.pavement_layer_clogging_factor = self.txtPavement5.text()
            self.editing_item.pavement_layer_regeneration_interval = self.txtRegeneration.text()
            self.editing_item.pavement_layer_regeneration_fraction = self.txtFraction.text()
        if self.editing_item.has_soil_layer:
            self.editing_item.soil_layer_thickness = self.txtSoil1.text()
            self.editing_item.soil_layer_porosity = self.txtSoil2.text()
            self.editing_item.soil_layer_field_capacity = self.txtSoil3.text()
            self.editing_item.soil_layer_wilting_point = self.txtSoil4.text()
            self.editing_item.soil_layer_conductivity = self.txtSoil5.text()
            self.editing_item.soil_layer_conductivity_slope = self.txtSoil6.text()
            self.editing_item.soil_layer_suction_head = self.txtSoil7.text()
        if self.editing_item.has_storage_layer:
            self.editing_item.storage_layer_height = self.txtStorage1.text()
            self.editing_item.storage_layer_void_ratio = self.txtStorage2.text()
            self.editing_item.storage_layer_filtration_rate = self.txtStorage3.text()
            self.editing_item.storage_layer_clogging_factor = self.txtStorage4.text()
        if self.editing_item.has_underdrain_system:
            self.editing_item.drain_coefficient = self.txtDrain1.text()
            self.editing_item.drain_exponent = self.txtDrain2.text()
            self.editing_item.drain_offset_height = self.txtDrain3.text()
            self.editing_item.drain_delay = self.txtDrain4.text()
            self.editing_item.drain_open_level = self.txtOpen.text()
            self.editing_item.drain_closed_level = self.txtClosed.text()
            self.editing_item.drain_control_curve = self.cboCurve.currentText()
        if self.editing_item.has_drainmat_system:
            self.editing_item.drainmat_thickness = self.txtDrain1.text()
            self.editing_item.drainmat_void_fraction = self.txtDrain2.text()
            self.editing_item.drainmat_roughness = self.txtDrain3.text()
        if self.editing_item.has_pollutant_removals:
            if len(self.pollutant_list) > 0:
                self.editing_item.removal_pollutant1 = self.pollutant_list[0].name
                self.editing_item.removal_removal1 = self.tblPollutant.item(0, 0).text()
            if len(self.pollutant_list) > 1:
                self.editing_item.removal_pollutant2 = self.pollutant_list[1].name
                self.editing_item.removal_removal2 = self.tblPollutant.item(1, 0).text()
            if len(self.pollutant_list) > 2:
                self.editing_item.removal_pollutant3 = self.pollutant_list[2].name
                self.editing_item.removal_removal3 = self.tblPollutant.item(2, 0).text()
            if len(self.pollutant_list) > 3:
                self.editing_item.removal_pollutant4 = self.pollutant_list[3].name
                self.editing_item.removal_removal4 = self.tblPollutant.item(3, 0).text()
            if len(self.pollutant_list) > 4:
                self.editing_item.removal_pollutant5 = self.pollutant_list[4].name
                self.editing_item.removal_removal5 = self.tblPollutant.item(4, 0).text()
        # self.main_form.list_objects()

        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
            self._main_form.mark_project_as_unsaved()
        else:
            if oldname != self.editing_item.name:
                edited_names = []
                edited_names.append((oldname, self.editing_item))
                self._main_form.edited_name(edited_names)
            pass

        if orig_lid_type != self.editing_item.lid_type or \
            orig_surface_layer_storage_depth != self.editing_item.surface_layer_storage_depth or \
            orig_surface_layer_vegetative_cover_fraction != self.editing_item.surface_layer_vegetative_cover_fraction or \
            orig_surface_layer_surface_roughness != self.editing_item.surface_layer_surface_roughness or \
            orig_surface_layer_surface_slope != self.editing_item.surface_layer_surface_slope or \
            orig_surface_layer_swale_side_slope != self.editing_item.surface_layer_swale_side_slope or \
            orig_pavement_layer_thickness != self.editing_item.pavement_layer_thickness or \
            orig_pavement_layer_void_ratio != self.editing_item.pavement_layer_void_ratio or \
            orig_pavement_layer_impervious_surface_fraction != self.editing_item.pavement_layer_impervious_surface_fraction or \
            orig_pavement_layer_permeability != self.editing_item.pavement_layer_permeability or \
            orig_pavement_layer_clogging_factor != self.editing_item.pavement_layer_clogging_factor or \
            orig_pavement_layer_regeneration_interval != self.editing_item.pavement_layer_regeneration_interval or \
            orig_pavement_layer_regeneration_fraction != self.editing_item.pavement_layer_regeneration_fraction or \
            orig_soil_layer_thickness != self.editing_item.soil_layer_thickness or \
            orig_soil_layer_porosity != self.editing_item.soil_layer_porosity or \
            orig_soil_layer_field_capacity != self.editing_item.soil_layer_field_capacity or \
            orig_soil_layer_wilting_point != self.editing_item.soil_layer_wilting_point or \
            orig_soil_layer_conductivity != self.editing_item.soil_layer_conductivity or \
            orig_soil_layer_conductivity_slope != self.editing_item.soil_layer_conductivity_slope or \
            orig_soil_layer_suction_head != self.editing_item.soil_layer_suction_head or \
            orig_storage_layer_height != self.editing_item.storage_layer_height or \
            orig_storage_layer_void_ratio != self.editing_item.storage_layer_void_ratio or \
            orig_storage_layer_filtration_rate != self.editing_item.storage_layer_filtration_rate or \
            orig_storage_layer_clogging_factor != self.editing_item.storage_layer_clogging_factor or \
            orig_drain_coefficient != self.editing_item.drain_coefficient or \
            orig_drain_exponent != self.editing_item.drain_exponent or \
            orig_drain_offset_height != self.editing_item.drain_offset_height or \
            orig_drain_delay != self.editing_item.drain_delay or \
            orig_drain_open_level != self.editing_item.drain_open_level or \
            orig_drain_closed_level != self.editing_item.drain_closed_level or \
            orig_drain_control_curve != self.editing_item.drain_control_curve or \
            orig_drainmat_thickness != self.editing_item.drainmat_thickness or \
            orig_drainmat_void_fraction != self.editing_item.drainmat_void_fraction or \
            orig_drainmat_roughness != self.editing_item.drainmat_roughness or \
            orig_removal_removal1 != self.editing_item.removal_removal1 or \
            orig_removal_removal2 != self.editing_item.removal_removal2 or \
            orig_removal_removal3 != self.editing_item.removal_removal3 or \
            orig_removal_removal4 != self.editing_item.removal_removal4 or \
            orig_removal_removal5 != self.editing_item.removal_removal5:
            self._main_form.mark_project_as_unsaved()

        self._main_form.program_settings.setValue("Geometry/" + "frmLID_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmLID_state", self.saveState())
        self.close()

    def cmdCancel_Clicked(self):
        self._main_form.program_settings.setValue("Geometry/" + "frmLID_geometry", self.saveGeometry())
        self._main_form.program_settings.setValue("Geometry/" + "frmLID_state", self.saveState())
        self.close()

    def cboLIDType_currentIndexChanged(self, newIndex):

        self.lblSurface1.setText("Berm Height (in. or mm)")
        self.lblSurface2.setText("Vegetation Volume Fraction")
        self.lblSurface3.setText("Surface Roughness (Mannings n)")
        self.lblSurface4.setText("Surface Slope (percent)")
        self.lblSurface5.setText("Swale Side Slope (run / rise)")
        self.lblSurface2.setVisible(True)
        self.txtSurface2.setVisible(True)
        self.lblSurface3.setVisible(True)
        self.txtSurface3.setVisible(True)
        self.lblSurface4.setVisible(True)
        self.txtSurface4.setVisible(True)
        self.lblSurface5.setVisible(True)
        self.txtSurface5.setVisible(True)

        self.lblSoil1.setText("Thickness (in. or mm)")
        self.lblSoil2.setText("Porosity (volume fraction)")
        self.lblSoil3.setText("Field Capacity (volume fraction)")
        self.lblSoil4.setText("Wilting Point (volume fraction)")
        self.lblSoil5.setText("Conductivity (in/hr or mm/hr)")
        self.lblSoil6.setText("Conductivity Slope")
        self.lblSoil7.setText("Suction Head (in. or mm)")

        self.lblStorage1.setText("Thickness (in. or mm)")
        self.lblStorage2.setText("Void Ratio (Voids / Solids)")
        self.lblStorage3.setText("Seepage Rate (in/hr or mm/hr)")
        self.lblStorage4.setText("Clogging Factor")
        self.lblStorage2.setVisible(True)
        self.txtStorage2.setVisible(True)
        self.lblStorage3.setVisible(True)
        self.txtStorage3.setVisible(True)
        self.lblStorage4.setVisible(True)
        self.txtStorage4.setVisible(True)

        self.lblPavement1.setText("Thickness (in. or mm)")
        self.lblPavement2.setText("Void Ratio (Voids / Solids)")
        self.lblPavement3.setText("Impervious Surface Fraction")
        self.lblPavement4.setText("Permeability (in/hr or mm/hr)")
        self.lblPavement5.setText("Clogging Factor")

        self.lblDrain1.setText("Flow Coefficient*")
        self.lblDrain2.setText("Flow Exponent")
        self.lblDrain3.setText("Offset Height (in. or mm)")
        self.lblText.setText("*Units are for flow in either in/hr or mm/hr; use 0 if there is no drain.")
        self.lblDrain2.setVisible(True)
        self.txtDrain2.setVisible(True)
        self.lblDrain3.setVisible(True)
        self.txtDrain3.setVisible(True)
        self.lblDrain4.setVisible(True)
        self.txtDrain4.setVisible(True)
        self.lblOpen.setVisible(True)
        self.lblClosed.setVisible(True)
        self.lblControl.setVisible(True)
        self.txtOpen.setVisible(True)
        self.txtClosed.setVisible(True)
        self.cboCurve.setVisible(True)

        if newIndex == 0: # "Bio-Retention Cell"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/1bio.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,True)
            self.tabLID.setTabEnabled(3,True)
            self.tabLID.setTabEnabled(4,True)
            if self.pollutant_list:
                self.tabLID.setTabEnabled(5, True)
            else:
                self.tabLID.setTabEnabled(5, False)
            self.tabLID.setTabText(4,"Drain")

            self.lblSurface5.setVisible(False)
            self.txtSurface5.setVisible(False)

            self.lblDrain4.setVisible(False)
            self.txtDrain4.setVisible(False)

        elif newIndex == 1: # "Rain Garden"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/2rain.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,True)
            self.tabLID.setTabEnabled(3,False)
            self.tabLID.setTabEnabled(4,False)
            self.tabLID.setTabEnabled(5, False)
            self.tabLID.setTabText(4,"Drain")

            self.lblSurface5.setVisible(False)
            self.txtSurface5.setVisible(False)

        elif newIndex == 2: # "Green Roof"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/3greenl.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,True)
            self.tabLID.setTabEnabled(3,False)
            self.tabLID.setTabEnabled(4,True)
            self.tabLID.setTabEnabled(5, False)
            self.tabLID.setTabText(4,"Drainage Mat")

            self.lblSurface5.setVisible(False)
            self.txtSurface5.setVisible(False)

            self.lblDrain1.setText("Thickness (in. or mm)")
            self.lblDrain2.setText("Void Fraction")
            self.lblDrain3.setText("Roughness (Mannings n)")
            self.lblText.setText("")
            self.lblDrain4.setVisible(False)
            self.txtDrain4.setVisible(False)

            self.lblOpen.setVisible(False)
            self.lblClosed.setVisible(False)
            self.lblControl.setVisible(False)
            self.txtOpen.setVisible(False)
            self.txtClosed.setVisible(False)
            self.cboCurve.setVisible(False)

        elif newIndex == 3: # "Infiltration Trench"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/4infilt.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,False)
            self.tabLID.setTabEnabled(3,True)
            self.tabLID.setTabEnabled(4,True)
            if self.pollutant_list:
                self.tabLID.setTabEnabled(5, True)
            else:
                self.tabLID.setTabEnabled(5, False)
            self.tabLID.setTabText(4,"Drain")

            self.lblSurface5.setVisible(False)
            self.txtSurface5.setVisible(False)

            self.lblDrain1.setText("Flow Coefficient*")
            self.lblDrain2.setText("Flow Exponent")
            self.lblDrain3.setText("Offset Height (in. or mm)")
            self.lblText.setText("*Units are for flow in either in/hr or mm/hr; use 0 if there is no drain.")
            self.lblDrain4.setVisible(False)
            self.txtDrain4.setVisible(False)

        elif newIndex == 4: # "Permeable Pavement"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/5perm.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,True)
            self.tabLID.setTabEnabled(2,True)
            self.tabLID.setTabEnabled(3,True)
            self.tabLID.setTabEnabled(4,True)
            if self.pollutant_list:
                self.tabLID.setTabEnabled(5, True)
            else:
                self.tabLID.setTabEnabled(5, False)
            self.tabLID.setTabText(4,"Drain")

            self.lblSurface5.setVisible(False)
            self.txtSurface5.setVisible(False)

            self.lblDrain1.setText("Flow Coefficient*")
            self.lblDrain2.setText("Flow Exponent")
            self.lblDrain3.setText("Offset Height (in. or mm)")
            self.lblText.setText("*Units are for flow in either in/hr or mm/hr; use 0 if there is no drain.")
            self.lblDrain4.setVisible(False)
            self.txtDrain4.setVisible(False)

        elif newIndex == 5: # "Rain Barrel"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/6barrel.png"))
            self.tabLID.setTabEnabled(0,False)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,False)
            self.tabLID.setTabEnabled(3,True)
            self.tabLID.setTabEnabled(4,True)
            if self.pollutant_list:
                self.tabLID.setTabEnabled(5, True)
            else:
                self.tabLID.setTabEnabled(5, False)
            self.tabLID.setTabText(4,"Drain")

            self.lblStorage1.setText("Barrel Height (in. or mm)")
            self.lblStorage2.setVisible(False)
            self.txtStorage2.setVisible(False)
            self.lblStorage3.setVisible(False)
            self.txtStorage3.setVisible(False)
            self.lblStorage4.setVisible(False)
            self.txtStorage4.setVisible(False)

            self.lblDrain1.setText("Flow Coefficient*")
            self.lblDrain2.setText("Flow Exponent")
            self.lblDrain3.setText("Offset Height (in. or mm)")
            self.lblDrain4.setText("Drain Delay (hours)")
            self.lblText.setText("*Units are for flow in either in/hr or mm/hr; use 0 if there is no drain.")

        elif newIndex == 6: # "Rooftop Disconnection"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/7rooftop.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,False)
            self.tabLID.setTabEnabled(3,False)
            self.tabLID.setTabEnabled(4,True)
            self.tabLID.setTabEnabled(5, False)
            self.tabLID.setTabText(4,"Roof Drain")

            self.lblSurface1.setText("Storage Depth (in. or mm)")
            self.lblSurface2.setText("Surface Roughness (Mannings n)")
            self.lblSurface3.setText("Surface Slope (percent)")
            self.lblSurface4.setVisible(False)
            self.txtSurface4.setVisible(False)
            self.lblSurface5.setVisible(False)
            self.txtSurface5.setVisible(False)

            self.lblDrain1.setText("Flow Capacity (in/hr or mm/hr)")
            self.lblDrain2.setVisible(False)
            self.txtDrain2.setVisible(False)
            self.lblDrain3.setVisible(False)
            self.txtDrain3.setVisible(False)
            self.lblDrain4.setVisible(False)
            self.txtDrain4.setVisible(False)
            self.lblText.setText("Enter the maximum flow rate that the roof's drain system (gutters, downspouts, and leaders) can handle before overflowing. Use 0 if not applicable.")

            self.lblOpen.setVisible(False)
            self.lblClosed.setVisible(False)
            self.lblControl.setVisible(False)
            self.txtOpen.setVisible(False)
            self.txtClosed.setVisible(False)
            self.cboCurve.setVisible(False)

        elif newIndex == 7: # "Vegetative Swale"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/8veg.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,False)
            self.tabLID.setTabEnabled(3,False)
            self.tabLID.setTabEnabled(4,False)
            self.tabLID.setTabEnabled(5, False)
            self.tabLID.setTabText(4,"Drain")

        if newIndex == 0:
            self.lid.has_surface_layer = True
            self.lid.has_pavement_layer = False
            self.lid.has_soil_layer = True
            self.lid.has_storage_layer = True
            self.lid.has_underdrain_system = True
            self.lid.has_drainmat_system = False
            self.lid.has_pollutant_removals = True
        elif newIndex == 1:
            self.lid.has_surface_layer = True
            self.lid.has_pavement_layer = False
            self.lid.has_soil_layer = True
            self.lid.has_storage_layer = False
            self.lid.has_underdrain_system = False
            self.lid.has_drainmat_system = False
            self.lid.has_pollutant_removals = False
        elif newIndex == 2:
            self.lid.has_surface_layer = True
            self.lid.has_pavement_layer = False
            self.lid.has_soil_layer = True
            self.lid.has_storage_layer = False
            self.lid.has_underdrain_system = False
            self.lid.has_drainmat_system = True
            self.lid.has_pollutant_removals = False
        elif newIndex == 3:
            self.lid.has_surface_layer = True
            self.lid.has_pavement_layer = False
            self.lid.has_soil_layer = True
            self.lid.has_storage_layer = False
            self.lid.has_underdrain_system = True
            self.lid.has_drainmat_system = False
            self.lid.has_pollutant_removals = True
        elif newIndex == 4:
            self.lid.has_surface_layer = True
            self.lid.has_pavement_layer = True
            self.lid.has_soil_layer = True
            self.lid.has_storage_layer = True
            self.lid.has_underdrain_system = True
            self.lid.has_drainmat_system = False
            self.lid.has_pollutant_removals = True
        elif newIndex == 5:
            self.lid.has_surface_layer = False
            self.lid.has_pavement_layer = False
            self.lid.has_soil_layer = False
            self.lid.has_storage_layer = True
            self.lid.has_underdrain_system = True
            self.lid.has_drainmat_system = False
            self.lid.has_pollutant_removals = True
        elif newIndex == 6:
            self.lid.has_surface_layer = True
            self.lid.has_pavement_layer = False
            self.lid.has_soil_layer = False
            self.lid.has_storage_layer = False
            self.lid.has_underdrain_system = True
            self.lid.has_drainmat_system = False
            self.lid.has_pollutant_removals = False
        elif newIndex == 7:
            self.lid.has_surface_layer = True
            self.lid.has_pavement_layer = False
            self.lid.has_soil_layer = False
            self.lid.has_storage_layer = False
            self.lid.has_underdrain_system = False
            self.lid.has_drainmat_system = False
            self.lid.has_pollutant_removals = False

        if self.lid.has_surface_layer:
            if newIndex == 6:
                self.txtSurface1.setText(self.lid.surface_layer_storage_depth)
                self.txtSurface2.setText(self.lid.surface_layer_surface_roughness)
                self.txtSurface3.setText(self.lid.surface_layer_surface_slope)
            else:
                self.txtSurface1.setText(self.lid.surface_layer_storage_depth)
                self.txtSurface2.setText(self.lid.surface_layer_vegetative_cover_fraction)
                self.txtSurface3.setText(self.lid.surface_layer_surface_roughness)
                self.txtSurface4.setText(self.lid.surface_layer_surface_slope)
                self.txtSurface5.setText(self.lid.surface_layer_swale_side_slope)
        if self.lid.has_pavement_layer:
            self.txtPavement1.setText(self.lid.pavement_layer_thickness)
            self.txtPavement2.setText(self.lid.pavement_layer_void_ratio)
            self.txtPavement3.setText(self.lid.pavement_layer_impervious_surface_fraction)
            self.txtPavement4.setText(self.lid.pavement_layer_permeability)
            self.txtPavement5.setText(self.lid.pavement_layer_clogging_factor)
        if self.lid.has_soil_layer:
            self.txtSoil1.setText(self.lid.soil_layer_thickness)
            self.txtSoil2.setText(self.lid.soil_layer_porosity)
            self.txtSoil3.setText(self.lid.soil_layer_field_capacity)
            self.txtSoil4.setText(self.lid.soil_layer_wilting_point)
            self.txtSoil5.setText(self.lid.soil_layer_conductivity)
            self.txtSoil6.setText(self.lid.soil_layer_conductivity_slope)
            self.txtSoil7.setText(self.lid.soil_layer_suction_head)
        if self.lid.has_storage_layer:
            self.txtStorage1.setText(self.lid.storage_layer_height)
            self.txtStorage2.setText(self.lid.storage_layer_void_ratio)
            self.txtStorage3.setText(self.lid.storage_layer_filtration_rate)
            self.txtStorage4.setText(self.lid.storage_layer_clogging_factor)
        if self.lid.has_underdrain_system:
            self.txtDrain1.setText(self.lid.drain_coefficient)
            self.txtDrain2.setText(self.lid.drain_exponent)
            self.txtDrain3.setText(self.lid.drain_offset_height)
            self.txtDrain4.setText(self.lid.drain_delay)
        if self.lid.has_drainmat_system:
            self.txtDrain1.setText(self.lid.drainmat_thickness)
            self.txtDrain2.setText(self.lid.drainmat_void_fraction)
            self.txtDrain3.setText(self.lid.drainmat_roughness)

