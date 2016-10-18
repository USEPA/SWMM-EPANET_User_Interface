import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmTransectDesigner import Ui_frmTransect
from core.swmm.hydraulics.link import Transect


class frmTransect(QtGui.QMainWindow, Ui_frmTransect):
    SECTION_TYPE = Transect

    def __init__(self, main_form, edit_these, new_item):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self._main_form = main_form
        self.project = main_form.project
        self.section = self.project.transects
        self.new_item = new_item
        if new_item:
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):  # edit first transect if given a list
                self.set_from(edit_these[0])
            else:
                self.set_from(edit_these)

    def set_from(self, transect):
        if not isinstance(transect, Transect):
            transect = self.section.value[transect]
        if isinstance(transect, Transect):
            self.editing_item = transect
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
        self.editing_item.name = self.txtName.text()
        self.editing_item.comment = self.txtDescription.text()
        self.editing_item.n_left = self.txtLeftBank.text()
        self.editing_item.n_right = self.txtRightBank.text()
        self.editing_item.n_channel = self.txtChannel.text()
        self.editing_item.elevations_modifier = self.txtElevations.text()
        self.editing_item.meander_modifier = self.txtMeander.text()
        self.editing_item.stations_modifier = self.txtStations.text()
        self.editing_item.overbank_left = self.txtLeftSta.text()
        self.editing_item.overbank_right = self.txtRightSta.text()
        self.editing_item.stations = []
        for row in range(self.tblself.editing_item.rowCount()):
            if self.tblTransect.item(row,1):
                x = self.tblTransect.item(row,1).text()
                if len(x) > 0:
                    if self.tblTransect.item(row,0):
                        y = self.tblTransect.item(row,0).text()
                        if len(y) > 0:
                            self.editing_item.stations.append((x,y))
        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self.main_form.add_item(self.new_item)
        else:
            pass
            # TODO: self._main_form.edited_?

        self.close()

    def cmdCancel_Clicked(self):
        self.close()
