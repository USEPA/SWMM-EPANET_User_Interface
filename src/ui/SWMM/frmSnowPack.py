import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmSnowPackDesigner import Ui_frmSnowPack
from core.swmm.hydrology.snowpack import SnowPack


class frmSnowPack(QtGui.QMainWindow, Ui_frmSnowPack):
    def __init__(self, main_form, edit_these, new_item):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "swmm/src/src/snowpackparameterseditor.htm"
        # TODO: include help topic for snow removal (on separate tab?)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self._main_form = main_form
        self.project = main_form.project
        self.section = self.project.snowpacks
        self.new_item = new_item
        if new_item:
            self.set_from(new_item)
        elif edit_these:
            if isinstance(edit_these, list):  # edit first snow pack if given a list
                self.set_from(edit_these[0])
            else:
                self.set_from(edit_these)

    def set_from(self, pack):
        if not isinstance(pack, SnowPack):
            pack = self.section.value[pack]
        if isinstance(pack, SnowPack):
            self.editing_item = pack
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
        self.editing_item.name = self.txtSnow.text()

        self.editing_item.plowable_minimum_melt_coefficient = self.tblPack.item(0,0).text()
        self.editing_item.plowable_maximum_melt_coefficient = self.tblPack.item(1,0).text()
        self.editing_item.plowable_base_temperature = self.tblPack.item(2,0).text()
        self.editing_item.plowable_fraction_free_water_capacity  =self.tblPack.item(3,0).text()
        self.editing_item.plowable_initial_snow_depth = self.tblPack.item(4,0).text()
        self.editing_item.plowable_initial_free_water = self.tblPack.item(5,0).text()

        self.editing_item.impervious_minimum_melt_coefficient = self.tblPack.item(0,1).text()
        self.editing_item.impervious_maximum_melt_coefficient = self.tblPack.item(1,1).text()
        self.editing_item.impervious_base_temperature = self.tblPack.item(2,1).text()
        self.editing_item.impervious_fraction_free_water_capacity = self.tblPack.item(3,1).text()
        self.editing_item.impervious_initial_snow_depth = self.tblPack.item(4,1).text()
        self.editing_item.impervious_initial_free_water = self.tblPack.item(5,1).text()
        self.editing_item.impervious_depth_100_cover = self.tblPack.item(6,1).text()

        self.editing_item.pervious_minimum_melt_coefficient = self.tblPack.item(0,2).text()
        self.editing_item.pervious_maximum_melt_coefficient = self.tblPack.item(1,2).text()
        self.editing_item.pervious_base_temperature = self.tblPack.item(2,2).text()
        self.editing_item.pervious_fraction_free_water_capacity = self.tblPack.item(3,2).text()
        self.editing_item.pervious_initial_snow_depth = self.tblPack.item(4,2).text()
        self.editing_item.pervious_initial_free_water = self.tblPack.item(5,2).text()
        self.editing_item.pervious_depth_100_cover = self.tblPack.item(6,2).text()

        self.editing_item.plowable_fraction_impervious_area = self.txtFraction.text()

        self.editing_item.depth_snow_removal_begins = self.txtRemoval1.text()
        self.editing_item.fraction_transferred_out_watershed = self.txtRemoval2.text()
        self.editing_item.fraction_transferred_impervious_area = self.txtRemoval3.text()
        self.editing_item.fraction_transferred_pervious_area = self.txtRemoval4.text()
        self.editing_item.fraction_converted_immediate_melt = self.txtRemoval5.text()
        self.editing_item.fraction_moved_another_subcatchment = self.txtRemoval6.text()
        self.editing_item.subcatchment_transfer = self.txtRemoval7.text()

        if self.new_item:  # We are editing a newly created item and it needs to be added to the project
            self._main_form.add_item(self.new_item)
        else:
            pass
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
