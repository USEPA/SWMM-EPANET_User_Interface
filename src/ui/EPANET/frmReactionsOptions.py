import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
import core.epanet.options.reactions
from ui.EPANET.frmReactionsOptionsDesigner import Ui_frmReactionsOptions


class frmReactionsOptions(QtGui.QMainWindow, Ui_frmReactionsOptions):
    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Anal0042.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        # section = core.epanet.options.reactions.Reactions()
        section = project.find_section("REACTIONS")
        self.txtBulkOrder.setText(str(section.order_bulk))
        self.txtWallOrder.setText(str(section.order_wall))
        self.txtTankOrder.setText(str(section.order_tank))
        self.txtGlobalBulk.setText(str(section.global_bulk))
        self.txtGlobalWall.setText(str(section.global_wall))
        self.txtLimiting.setText(str(section.limiting_potential))
        self.txtCorrelation.setText(str(section.roughness_correlation))

    def cmdOK_Clicked(self):
        section = self._main_form.project.find_section("REACTIONS")
        section.order_bulk = self.txtBulkOrder.text()
        section.order_wall = self.txtWallOrder.text()
        section.order_tank = self.txtTankOrder.text()
        section.global_bulk = self.txtGlobalBulk.text()
        section.global_wall = self.txtGlobalWall.text()
        section.limiting_potential = self.txtLimiting.text()
        section.roughness_correlation = self.txtCorrelation.text()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
