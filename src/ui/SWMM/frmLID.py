import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmLIDDesigner import Ui_frmLID


class frmLID(QtGui.QMainWindow, Ui_frmLID):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.cboLIDType.clear()
        self.cboLIDType.addItems(("Bio-Retention Cell","Rain Garden","Green Roof","Infiltration Trench","Permeable Pavement", "Rain Barrel", "Rooftop Disconnection", "Vegetative Swale"))
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.cboLIDType.currentIndexChanged.connect(self.cboLIDType_currentIndexChanged)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        section = project.title
        # self.txtTitle.setPlainText(project.title.title)
        self.cboLIDType_currentIndexChanged(0)

    def cmdOK_Clicked(self):
        section = self._parent.project.title
        section.title = self.txtTitle.toPlainText()
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
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/1bio.png"))
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
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/2rain.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,True)
            self.tabLID.setTabEnabled(3,False)
            self.tabLID.setTabEnabled(4,False)
            self.tabLID.setTabText(4,"Drain")

            self.lblSurface5.setVisible(False)
            self.txtSurface5.setVisible(False)

        elif newIndex == 2: # "Green Roof"
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/3greenl.png"))
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
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/4infilt.png"))
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
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/5perm.png"))
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
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/6barrel.png"))
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
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/7rooftop.png"))
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
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/8veg.png"))
            self.tabLID.setTabEnabled(0,True)
            self.tabLID.setTabEnabled(1,False)
            self.tabLID.setTabEnabled(2,False)
            self.tabLID.setTabEnabled(3,False)
            self.tabLID.setTabEnabled(4,False)
            self.tabLID.setTabText(4,"Drain")

