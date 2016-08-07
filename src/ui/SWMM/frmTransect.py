import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmTransectDesigner import Ui_frmTransect


class frmTransect(QtGui.QMainWindow, Ui_frmTransect):
    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self._main_form = main_form
        self.transect_name = ''
        # set for first transect for now
        self.set_from(main_form.project, 'xx')

    def set_from(self, project, transect_name):
        # section = core.swmm.project.Transects
        section = project.find_section("TRANSECTS")
        transect_list = section.value[0:]
        # assume we want to edit the first one
        self.transect_name = transect_name
        for transect in transect_list:
            if transect.name == transect_name:
                # this is the transect we want to edit
                self.txtName.setText(transect.name)
                self.txtDescription.setText(transect.comment)
                self.txtLeftBank.setText(transect.n_left)
                self.txtRightBank.setText(transect.n_right)
                self.txtChannel.setText(transect.n_channel)
                self.txtLeftSta.setText(transect.overbank_left)
                self.txtRightSta.setText(transect.overbank_right)
                self.txtStations.setText(transect.stations_modifier)
                self.txtElevations.setText(transect.elevations_modifier)
                self.txtMeander.setText(transect.meander_modifier)
                point_count = -1
                for value in transect.stations:
                    point_count += 1
                    led = QtGui.QLineEdit(str(value[1]))
                    self.tblTransect.setItem(point_count,0,QtGui.QTableWidgetItem(led.text()))
                    led = QtGui.QLineEdit(str(value[0]))
                    self.tblTransect.setItem(point_count,1,QtGui.QTableWidgetItem(led.text()))

    def cmdOK_Clicked(self):
        section = self._main_form.project.find_section("TRANSECTS")
        transect_list = section.value[0:]
        for transect in transect_list:
            if transect.name == self.transect_name:
                # this is the transect
                transect.name = self.txtName.text()
                transect.comment = self.txtDescription.text()
                transect.n_left = self.txtLeftBank.text()
                transect.n_right = self.txtRightBank.text()
                transect.n_channel = self.txtChannel.text()
                transect.elevations_modifier = self.txtElevations.text()
                transect.meander_modifier = self.txtMeander.text()
                transect.stations_modifier = self.txtStations.text()
                transect.overbank_left = self.txtLeftSta.text()
                transect.overbank_right = self.txtRightSta.text()
                transect.stations = []
                for row in range(self.tblTransect.rowCount()):
                    if self.tblTransect.item(row,1):
                        x = self.tblTransect.item(row,1).text()
                        if len(x) > 0:
                            if self.tblTransect.item(row,0):
                                y = self.tblTransect.item(row,0).text()
                                if len(y) > 0:
                                    transect.stations.append((x,y))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
