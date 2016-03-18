import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmLIDUsageDesigner import Ui_frmLIDUsage


class frmLIDUsage(QtGui.QMainWindow, Ui_frmLIDUsage):


    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.epanet.project.Control()
        section = project.find_section("CONTROLS")
        # self.txtControls.setPlainText(str(section.get_text()))

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("CONTROLS")
        section.set_text(str(self.txtControls.toPlainText()))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def cboLIDControl_currentIndexChanged(self, newIndex):
        if newIndex == 0: # "Bio-Retention Cell"
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/1237LID.png"))
        elif newIndex == 1: # "Rain Garden"
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/1237LID.png"))
        elif newIndex == 2: # "Green Roof"
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/1237LID.png"))
        elif newIndex == 3: # "Infiltration Trench"
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/4LID.png"))
        elif newIndex == 4: # "Permeable Pavement"
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/5LID.png"))
        elif newIndex == 5: # "Rain Barrel"
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/6LID.png"))
        elif newIndex == 6: # "Rooftop Disconnection"
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/1237LID.png"))
        elif newIndex == 7: # "Vegetative Swale"
            self.lblImage.setPixmap(QtGui.QPixmap("../swmmimages/8LID.png"))


