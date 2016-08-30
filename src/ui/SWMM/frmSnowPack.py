import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmSnowPackDesigner import Ui_frmSnowPack


class frmSnowPack(QtGui.QMainWindow, Ui_frmSnowPack):
    def __init__(self, main_form=None, edit_these=[]):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/snowpackparameterseditor.htm"
        # TODO: include help topic for snow removal (on separate tab?)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self._main_form = main_form
        self.pack_name = ''
        if edit_these:
            if isinstance(edit_these, list):
                self.set_from(main_form.project, edit_these[0])
            else:
                self.set_from(main_form.project, edit_these)

    def set_from(self, project, pack_name):
        # section = core.swmm.project.SnowPack
        section = project.find_section("SNOWPACKS")
        snow_list = section.value[0:]
        # assume we want to edit the first one
        self.pack_name = pack_name
        for pack in snow_list:
            if pack.name == pack_name:
                # this is the snowpack we want to edit
                self.txtSnow.setText(pack.name)

                led = QtGui.QLineEdit(str(pack.plowable_minimum_melt_coefficient))
                self.tblPack.setItem(0,0,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.plowable_maximum_melt_coefficient))
                self.tblPack.setItem(1,0,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.plowable_base_temperature))
                self.tblPack.setItem(2,0,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.plowable_fraction_free_water_capacity))
                self.tblPack.setItem(3,0,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.plowable_initial_snow_depth))
                self.tblPack.setItem(4,0,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.plowable_initial_free_water))
                self.tblPack.setItem(5,0,QtGui.QTableWidgetItem(led.text()))

                led = QtGui.QLineEdit(str(pack.impervious_minimum_melt_coefficient))
                self.tblPack.setItem(0,1,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.impervious_maximum_melt_coefficient))
                self.tblPack.setItem(1,1,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.impervious_base_temperature))
                self.tblPack.setItem(2,1,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.impervious_fraction_free_water_capacity))
                self.tblPack.setItem(3,1,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.impervious_initial_snow_depth))
                self.tblPack.setItem(4,1,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.impervious_initial_free_water))
                self.tblPack.setItem(5,1,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.impervious_depth_100_cover))
                self.tblPack.setItem(6,1,QtGui.QTableWidgetItem(led.text()))

                led = QtGui.QLineEdit(str(pack.pervious_minimum_melt_coefficient))
                self.tblPack.setItem(0,2,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.pervious_maximum_melt_coefficient))
                self.tblPack.setItem(1,2,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.pervious_base_temperature))
                self.tblPack.setItem(2,2,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.pervious_fraction_free_water_capacity))
                self.tblPack.setItem(3,2,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.pervious_initial_snow_depth))
                self.tblPack.setItem(4,2,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.pervious_initial_free_water))
                self.tblPack.setItem(5,2,QtGui.QTableWidgetItem(led.text()))
                led = QtGui.QLineEdit(str(pack.pervious_depth_100_cover))
                self.tblPack.setItem(6,2,QtGui.QTableWidgetItem(led.text()))

                self.txtFraction.setText(pack.plowable_fraction_impervious_area)

                self.txtRemoval1.setText(pack.depth_snow_removal_begins)
                self.txtRemoval2.setText(pack.fraction_transferred_out_watershed)
                self.txtRemoval3.setText(pack.fraction_transferred_impervious_area)
                self.txtRemoval4.setText(pack.fraction_transferred_pervious_area)
                self.txtRemoval5.setText(pack.fraction_converted_immediate_melt)
                self.txtRemoval6.setText(pack.fraction_moved_another_subcatchment)
                self.txtRemoval7.setText(pack.subcatchment_transfer)

    def cmdOK_Clicked(self):
        section = self._main_form.project.find_section("SNOWPACKS")

        snow_list = section.value[0:]
        for pack in snow_list:
            if pack.name == self.pack_name:
                # this is the snowpack
                pack.name = self.txtSnow.text()

                pack.plowable_minimum_melt_coefficient = self.tblPack.item(0,0).text()
                pack.plowable_maximum_melt_coefficient = self.tblPack.item(1,0).text()
                pack.plowable_base_temperature = self.tblPack.item(2,0).text()
                pack.plowable_fraction_free_water_capacity  =self.tblPack.item(3,0).text()
                pack.plowable_initial_snow_depth = self.tblPack.item(4,0).text()
                pack.plowable_initial_free_water = self.tblPack.item(5,0).text()

                pack.impervious_minimum_melt_coefficient = self.tblPack.item(0,1).text()
                pack.impervious_maximum_melt_coefficient = self.tblPack.item(1,1).text()
                pack.impervious_base_temperature = self.tblPack.item(2,1).text()
                pack.impervious_fraction_free_water_capacity = self.tblPack.item(3,1).text()
                pack.impervious_initial_snow_depth = self.tblPack.item(4,1).text()
                pack.impervious_initial_free_water = self.tblPack.item(5,1).text()
                pack.impervious_depth_100_cover = self.tblPack.item(6,1).text()

                pack.pervious_minimum_melt_coefficient = self.tblPack.item(0,2).text()
                pack.pervious_maximum_melt_coefficient = self.tblPack.item(1,2).text()
                pack.pervious_base_temperature = self.tblPack.item(2,2).text()
                pack.pervious_fraction_free_water_capacity = self.tblPack.item(3,2).text()
                pack.pervious_initial_snow_depth = self.tblPack.item(4,2).text()
                pack.pervious_initial_free_water = self.tblPack.item(5,2).text()
                pack.pervious_depth_100_cover = self.tblPack.item(6,2).text()

                pack.plowable_fraction_impervious_area = self.txtFraction.text()

                pack.depth_snow_removal_begins = self.txtRemoval1.text()
                pack.fraction_transferred_out_watershed = self.txtRemoval2.text()
                pack.fraction_transferred_impervious_area = self.txtRemoval3.text()
                pack.fraction_transferred_pervious_area = self.txtRemoval4.text()
                pack.fraction_converted_immediate_melt = self.txtRemoval5.text()
                pack.fraction_moved_another_subcatchment = self.txtRemoval6.text()
                pack.subcatchment_transfer = self.txtRemoval7.text()

        self.close()

    def cmdCancel_Clicked(self):
        self.close()
