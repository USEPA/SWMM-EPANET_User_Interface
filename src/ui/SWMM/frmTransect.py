import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QTableWidgetItem
from ui.SWMM.frmTransectDesigner import Ui_frmTransect
from ui.help import HelpHandler
from core.swmm.hydraulics.link import Transect
import pandas as pd
from ui.frmPlotViewer import frmPlotViewer


class frmTransect(QMainWindow, Ui_frmTransect):
    SECTION_TYPE = Transect

    def __init__(self, main_form, edit_these, new_item):
        QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/transecteditordialog.htm"
        self.helper = HelpHandler(self)
        self.setupUi(self)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.btnView.clicked.connect(self.btnView_Clicked)
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
            self.txtLeftBank.setText(str(transect.n_left))
            self.txtRightBank.setText(str(transect.n_right))
            self.txtChannel.setText(str(transect.n_channel))
            self.txtLeftSta.setText(str(transect.overbank_left))
            self.txtRightSta.setText(str(transect.overbank_right))
            self.txtStations.setText(str(transect.stations_modifier))
            self.txtElevations.setText(str(transect.elevations_modifier))
            self.txtMeander.setText(str(transect.meander_modifier))
            point_count = -1
            for value in transect.stations:
                point_count += 1
                led = QLineEdit(str(value[1]))
                self.tblTransect.setItem(point_count,0,QTableWidgetItem(led.text()))
                led = QLineEdit(str(value[0]))
                self.tblTransect.setItem(point_count,1,QTableWidgetItem(led.text()))
        if self.project.metric:
            self.tblTransect.horizontalHeaderItem(0).setText('Station (m)')
            self.tblTransect.horizontalHeaderItem(1).setText('Elevation (m)')

    def cmdOK_Clicked(self):
        orig_name = self.editing_item.name
        orig_comment = self.editing_item.comment
        orig_n_left = self.editing_item.n_left
        orig_n_right = self.editing_item.n_right
        orig_n_channel = self.editing_item.n_channel
        orig_eleations_modifier = self.editing_item.elevations_modifier
        orig_meander_modifier = self.editing_item.meander_modifier
        orig_stations_modifier = self.editing_item.stations_modifier
        orig_overbank_left = self.editing_item.overbank_left
        orig_overbank_right = self.editing_item.overbank_right
        orig_stations = self.editing_item.stations

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
        for row in range(self.tblTransect.rowCount()):
            if self.tblTransect.item(row,1):
                x = self.tblTransect.item(row,1).text()
                if len(x) > 0:
                    if self.tblTransect.item(row,0):
                        y = self.tblTransect.item(row,0).text()
                        if len(y) > 0:
                            self.editing_item.stations.append((x,y))

        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
            self._main_form.mark_project_as_unsaved()
        else:
            if orig_name != self.editing_item.name or \
                orig_comment != self.editing_item.comment or \
                orig_n_left != self.editing_item.n_left or \
                orig_n_right != self.editing_item.n_right or \
                orig_n_channel != self.editing_item.n_channel or \
                orig_eleations_modifier != self.editing_item.elevations_modifier or \
                orig_meander_modifier != self.editing_item.meander_modifier or \
                orig_stations_modifier != self.editing_item.stations_modifier or \
                orig_overbank_left != self.editing_item.overbank_left or \
                orig_overbank_right != self.editing_item.overbank_right or \
                orig_stations != self.editing_item.stations:
                self._main_form.mark_project_as_unsaved()
            pass

        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    def btnView_Clicked(self):
        """
        Display the grid data with pandas dataframe plot function
        Returns: None
        """
        self.Y = []
        self.X = []
        for row in range(self.tblTransect.rowCount()):
            if self.tblTransect.item(row,0):
                x = self.tblTransect.item(row,0).text()
                if len(x) > 0:
                    if self.tblTransect.item(row,1):
                        y = self.tblTransect.item(row,1).text()
                        if len(y) > 0:
                            self.X.append(x)
                            self.Y.append(y)

        ts = pd.Series(self.Y, index=self.X)
        df = pd.DataFrame({'':ts})
        frm_plt = frmPlotViewer(df,'xy', 'Transect ' + self.editing_item.name, self.windowIcon(),
                                self.tblTransect.horizontalHeaderItem(0).text(), self.tblTransect.horizontalHeaderItem(1).text())
        frm_plt.setWindowTitle("Transect Viewer")
        frm_plt.show()