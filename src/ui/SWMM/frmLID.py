import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from core.swmm.hydrology.lidcontrol import LIDType
from ui.SWMM.frmLIDDesigner import Ui_frmLID


class frmLID(QtGui.QMainWindow, Ui_frmLID):
    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/lidcontroleditor.htm"
        self.setupUi(self)
        self.cboLIDType.clear()
        self.cboLIDType.addItems(("Bio-Retention Cell","Rain Garden","Green Roof","Infiltration Trench","Permeable Pavement", "Rain Barrel", "Rooftop Disconnection", "Vegetative Swale"))
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboLIDType.currentIndexChanged.connect(self.cboLIDType_currentIndexChanged)
        self.lid_name = ''
        # set for first lid control for now
        self.set_from(main_form.project, 'rg')

    def set_from(self, project, lid_name):
        self.project = project
        self.cboLIDType_currentIndexChanged(0)
        # section = core.swmm.project.LIDControl
        section = project.lid_controls
        lid_list = section.value[0:]
        # assume we want to edit the first one
        self.lid_name = lid_name
        for lid in lid_list:
            if lid.name == lid_name:
                # this is the lid control we want to edit
                self.txtName.setText(lid.name)
                if lid.lid_type == LIDType.BC:
                    self.cboLIDType.setCurrentIndex(0)
                elif lid.lid_type == LIDType.RG:
                    self.cboLIDType.setCurrentIndex(1)
                elif lid.lid_type == LIDType.GR:
                    self.cboLIDType.setCurrentIndex(2)
                elif lid.lid_type == LIDType.IT:
                    self.cboLIDType.setCurrentIndex(3)
                elif lid.lid_type == LIDType.PP:
                    self.cboLIDType.setCurrentIndex(4)
                elif lid.lid_type == LIDType.RB:
                    self.cboLIDType.setCurrentIndex(5)
                elif lid.lid_type == LIDType.RD:
                    self.cboLIDType.setCurrentIndex(6)
                elif lid.lid_type == LIDType.VS:
                    self.cboLIDType.setCurrentIndex(7)

                # if lid.has_surface_layer:
                self.txtSurface1.setText(lid.surface_layer_storage_depth)
                self.txtSurface2.setText(lid.surface_layer_vegetative_cover_fraction)
                self.txtSurface3.setText(lid.surface_layer_surface_roughness)
                self.txtSurface4.setText(lid.surface_layer_surface_slope)
                self.txtSurface5.setText(lid.surface_layer_swale_side_slope)
                # if lid.has_pavement_layer:
                self.txtPavement1.setText(lid.pavement_layer_thickness)
                self.txtPavement2.setText(lid.pavement_layer_void_ratio)
                self.txtPavement3.setText(lid.pavement_layer_impervious_surface_fraction)
                self.txtPavement4.setText(lid.pavement_layer_permeability)
                self.txtPavement5.setText(lid.pavement_layer_clogging_factor)
                # if lid.has_soil_layer:
                self.txtSoil1.setText(lid.soil_layer_thickness)
                self.txtSoil2.setText(lid.soil_layer_porosity)
                self.txtSoil3.setText(lid.soil_layer_field_capacity)
                self.txtSoil4.setText(lid.soil_layer_wilting_point)
                self.txtSoil5.setText(lid.soil_layer_conductivity)
                self.txtSoil6.setText(lid.soil_layer_conductivity_slope)
                self.txtSoil7.setText(lid.soil_layer_suction_head)
                # if lid.has_storage_layer:
                self.txtStorage1.setText(lid.storage_layer_height)
                self.txtStorage2.setText(lid.storage_layer_void_ratio)
                self.txtStorage3.setText(lid.storage_layer_filtration_rate)
                self.txtStorage4.setText(lid.storage_layer_clogging_factor)
                # if lid.has_underdrain_system:
                self.txtDrain1.setText(lid.drain_coefficient)
                self.txtDrain2.setText(lid.drain_exponent)
                self.txtDrain3.setText(lid.drain_offset_height)
                self.txtDrain4.setText(lid.drain_delay)
                # if lid.has_drainmat_system:
                self.txtDrain1.setText(lid.drainmat_thickness)
                self.txtDrain2.setText(lid.drainmat_void_fraction)
                self.txtDrain3.setText(lid.drainmat_roughness)

    def cmdOK_Clicked(self):
        section = self.project.lid_controls
        lid_list = section.value[0:]
        for lid in lid_list:
            if lid.name == self.lid_name:
                # this is the lid
                lid.name = self.txtName.text()
                if self.cboLIDType.currentIndex() == 0:
                    lid.lid_type = LIDType.BC
                    lid.has_surface_layer = True
                    lid.has_pavement_layer = False
                    lid.has_soil_layer = True
                    lid.has_storage_layer = True
                    lid.has_underdrain_system = True
                    lid.has_drainmat_system = False
                elif self.cboLIDType.currentIndex() == 1:
                    lid.lid_type = LIDType.RG
                    lid.has_surface_layer = True
                    lid.has_pavement_layer = False
                    lid.has_soil_layer = True
                    lid.has_storage_layer = False
                    lid.has_underdrain_system = False
                    lid.has_drainmat_system = False
                elif self.cboLIDType.currentIndex() == 2:
                    lid.lid_type = LIDType.GR
                    lid.has_surface_layer = True
                    lid.has_pavement_layer = False
                    lid.has_soil_layer = True
                    lid.has_storage_layer = False
                    lid.has_underdrain_system = False
                    lid.has_drainmat_system = True
                elif self.cboLIDType.currentIndex() == 3:
                    lid.lid_type = LIDType.IT
                    lid.has_surface_layer = True
                    lid.has_pavement_layer = False
                    lid.has_soil_layer = True
                    lid.has_storage_layer = False
                    lid.has_underdrain_system = True
                    lid.has_drainmat_system = False
                elif self.cboLIDType.currentIndex() == 4:
                    lid.lid_type = LIDType.PP
                    lid.has_surface_layer = True
                    lid.has_pavement_layer = True
                    lid.has_soil_layer = True
                    lid.has_storage_layer = True
                    lid.has_underdrain_system = True
                    lid.has_drainmat_system = False
                elif self.cboLIDType.currentIndex() == 5:
                    lid.lid_type = LIDType.RB
                    lid.has_surface_layer = False
                    lid.has_pavement_layer = False
                    lid.has_soil_layer = False
                    lid.has_storage_layer = True
                    lid.has_underdrain_system = True
                    lid.has_drainmat_system = False
                elif self.cboLIDType.currentIndex() == 6:
                    lid.lid_type = LIDType.RD
                    lid.has_surface_layer = True
                    lid.has_pavement_layer = False
                    lid.has_soil_layer = False
                    lid.has_storage_layer = False
                    lid.has_underdrain_system = True
                    lid.has_drainmat_system = False
                elif self.cboLIDType.currentIndex() == 7:
                    lid.lid_type = LIDType.VS
                    lid.has_surface_layer = True
                    lid.has_pavement_layer = False
                    lid.has_soil_layer = False
                    lid.has_storage_layer = False
                    lid.has_underdrain_system = False
                    lid.has_drainmat_system = False

                # if lid.has_surface_layer:
                lid.surface_layer_storage_depth = self.txtSurface1.text()
                lid.surface_layer_vegetative_cover_fraction = self.txtSurface2.text()
                lid.surface_layer_surface_roughness = self.txtSurface3.text()
                lid.surface_layer_surface_slope = self.txtSurface4.text()
                lid.surface_layer_swale_side_slope = self.txtSurface5.text()
                # if lid.has_pavement_layer:
                lid.pavement_layer_thickness = self.txtPavement1.text()
                lid.pavement_layer_void_ratio = self.txtPavement2.text()
                lid.pavement_layer_impervious_surface_fraction = self.txtPavement3.text()
                lid.pavement_layer_permeability = self.txtPavement4.text()
                lid.pavement_layer_clogging_factor = self.txtPavement5.text()
                # if lid.has_soil_layer:
                lid.soil_layer_thickness = self.txtSoil1.text()
                lid.soil_layer_porosity = self.txtSoil2.text()
                lid.soil_layer_field_capacity = self.txtSoil3.text()
                lid.soil_layer_wilting_point = self.txtSoil4.text()
                lid.soil_layer_conductivity = self.txtSoil5.text()
                lid.soil_layer_conductivity_slope = self.txtSoil6.text()
                lid.soil_layer_suction_head = self.txtSoil7.text()
                # if lid.has_storage_layer:
                lid.storage_layer_height = self.txtStorage1.text()
                lid.storage_layer_void_ratio = self.txtStorage2.text()
                lid.storage_layer_filtration_rate = self.txtStorage3.text()
                lid.storage_layer_clogging_factor = self.txtStorage4.text()
                # if lid.has_underdrain_system:
                lid.drain_coefficient = self.txtDrain1.text()
                lid.drain_exponent = self.txtDrain2.text()
                lid.drain_offset_height = self.txtDrain3.text()
                lid.drain_delay = self.txtDrain4.text()
                # if lid.has_drainmat_system:
                lid.drainmat_thickness = self.txtDrain1.text()
                lid.drainmat_void_fraction = self.txtDrain2.text()
                lid.drainmat_roughness = self.txtDrain3.text()
        self._main_form.list_objects()
        self.close()

    def cmdCancel_Clicked(self):
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

        if newIndex == 0: # "Bio-Retention Cell"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/1bio.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,True)
            self.tabLID.setTabEnabled(3,True)
            self.tabLID.setTabEnabled(4,True)
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
            self.tabLID.setTabText(4,"Drainage Mat")

            self.lblSurface5.setVisible(False)
            self.txtSurface5.setVisible(False)

            self.lblDrain1.setText("Thickness (in. or mm)")
            self.lblDrain2.setText("Void Fraction")
            self.lblDrain3.setText("Roughness (Mannings n)")
            self.lblText.setText("")
            self.lblDrain4.setVisible(False)
            self.txtDrain4.setVisible(False)

        elif newIndex == 3: # "Infiltration Trench"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/4infilt.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,False)
            self.tabLID.setTabEnabled(3,True)
            self.tabLID.setTabEnabled(4,True)
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

        elif newIndex == 7: # "Vegetative Swale"
            self.lblImage.setPixmap(QtGui.QPixmap("./swmmimages/8veg.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,False)
            self.tabLID.setTabEnabled(3,False)
            self.tabLID.setTabEnabled(4,False)
            self.tabLID.setTabText(4,"Drain")

