from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow
from ui.help import HelpHandler
from ui.frmPreferencesDesigner import Ui_frmPreferences

class frmPreferences(QMainWindow, Ui_frmPreferences):
    def __init__(self, main_form=None):
        QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        self.helper = HelpHandler(self)
        if main_form.model == "SWMM":
            self.help_topic = "swmm/src/src/settingprogrampreferences.htm"
        elif main_form.model == "EPANET":
            self.help_topic = "epanet/src/src/setting_.htm"
        self.local_subcatch_preferences = {}
        self.local_node_preferences = {}
        self.local_link_preferences = {}
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self._main_form = main_form
        self.set_from(main_form.project)
        self.icon = main_form.windowIcon()
        self.cboSubcatchment.currentIndexChanged.connect(self.cboSubcatchment_currentIndexChanged)
        self.cboNode.currentIndexChanged.connect(self.cboNode_currentIndexChanged)
        self.cboLink.currentIndexChanged.connect(self.cboLink_currentIndexChanged)
        self.spnSubcatchment.valueChanged.connect(self.spnSubcatchment_valueChanged)
        self.spnNode.valueChanged.connect(self.spnNode_valueChanged)
        self.spnLink.valueChanged.connect(self.spnLink_valueChanged)

    def set_from(self, project):
        if self._main_form.model == "SWMM":
            settings = self._main_form.project_settings
            self.subcatch_keys = settings.subcatchment_numerical_preference_keys
            self.node_keys = settings.node_numerical_preference_keys
            self.link_keys = settings.link_numerical_preference_keys

            for key in self.subcatch_keys:
                self.local_subcatch_preferences[key] = settings.subcatchment_numerical_preferences[key]
            for key in self.node_keys:
                self.local_node_preferences[key] = settings.node_numerical_preferences[key]
            for key in self.link_keys:
                self.local_link_preferences[key] = settings.link_numerical_preferences[key]

            for key in self.subcatch_keys:
                self.cboSubcatchment.addItem(key)
            for key in self.node_keys:
                self.cboNode.addItem(key)
            for key in self.link_keys:
                self.cboLink.addItem(key)

            self.spnSubcatchment.setValue(self.local_subcatch_preferences[self.subcatch_keys[0]])
            self.spnNode.setValue(self.local_node_preferences[self.node_keys[0]])
            self.spnLink.setValue(self.local_link_preferences[self.link_keys[0]])

            if settings.general_preferences[settings.general_preference_keys[0]] > 0:
                self.cbxGeneral1.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[1]] > 0:
                self.cbxGeneral2.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[2]] > 0:
                self.cbxGeneral3.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[3]] > 0:
                self.cbxGeneral4.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[4]] > 0:
                self.cbxGeneral5.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[5]] > 0:
                self.cbxGeneral6.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[6]] > 0:
                self.cbxGeneral7.setChecked(True)

            self.cbxGeneral1.setDisabled(True)
            self.cbxGeneral2.setDisabled(True)
            self.cbxGeneral3.setDisabled(True)
            self.cbxGeneral5.setDisabled(True)
            self.cbxGeneral6.setDisabled(True)
            self.cbxGeneral7.setDisabled(True)

        elif self._main_form.model == "EPANET":
            self.lblSubcatchment.setVisible(False)
            self.cboSubcatchment.setVisible(False)
            self.lblDecimal1.setVisible(False)
            self.spnSubcatchment.setVisible(False)
            self.cbxGeneral5.setText('Bold Fonts')
            self.cbxGeneral6.setVisible(False)
            self.cbxGeneral7.setVisible(False)
            # self.cbxGeneral8.setVisible(False)

            settings = self._main_form.project_settings
            self.node_keys = settings.node_numerical_preference_keys
            self.link_keys = settings.link_numerical_preference_keys

            for key in self.node_keys:
                self.local_node_preferences[key] = settings.node_numerical_preferences[key]
            for key in self.link_keys:
                self.local_link_preferences[key] = settings.link_numerical_preferences[key]

            for key in self.node_keys:
                self.cboNode.addItem(key)
            for key in self.link_keys:
                self.cboLink.addItem(key)

            self.spnNode.setValue(self.local_node_preferences[self.node_keys[0]])
            self.spnLink.setValue(self.local_link_preferences[self.link_keys[0]])

            if settings.general_preferences[settings.general_preference_keys[0]] > 0:
                self.cbxGeneral1.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[1]] > 0:
                self.cbxGeneral2.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[2]] > 0:
                self.cbxGeneral3.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[3]] > 0:
                self.cbxGeneral4.setChecked(True)
            if settings.general_preferences[settings.general_preference_keys[4]] > 0:
                self.cbxGeneral5.setChecked(True)

            self.cbxGeneral1.setDisabled(True)
            self.cbxGeneral2.setDisabled(True)
            self.cbxGeneral3.setDisabled(True)
            self.cbxGeneral5.setDisabled(True)
        pass

    def cboSubcatchment_currentIndexChanged(self, newIndex):
        self.spnSubcatchment.setValue(self.local_subcatch_preferences[self.subcatch_keys[newIndex]])

    def cboNode_currentIndexChanged(self, newIndex):
        self.spnNode.setValue(self.local_node_preferences[self.node_keys[newIndex]])

    def cboLink_currentIndexChanged(self, newIndex):
        self.spnLink.setValue(self.local_link_preferences[self.link_keys[newIndex]])

    def spnSubcatchment_valueChanged(self, newValue):
        subcatch_index = self.cboSubcatchment.currentIndex()
        self.local_subcatch_preferences[self.subcatch_keys[subcatch_index]] = newValue

    def spnLink_valueChanged(self, newValue):
        link_index = self.cboLink.currentIndex()
        self.local_link_preferences[self.link_keys[link_index]] = newValue

    def spnNode_valueChanged(self, newValue):
        node_index = self.cboNode.currentIndex()
        self.local_node_preferences[self.node_keys[node_index]] = newValue

    def cmdOK_Clicked(self):
        settings = self._main_form.project_settings
        if self._main_form.model == "SWMM":
            settings.subcatchment_numerical_preferences = self.local_subcatch_preferences
            if self.cbxGeneral1.isChecked():
                settings.general_preferences[settings.general_preference_keys[0]] = 1
            if self.cbxGeneral2.isChecked():
                settings.general_preferences[settings.general_preference_keys[1]] = 1
            if self.cbxGeneral3.isChecked():
                settings.general_preferences[settings.general_preference_keys[2]] = 1
            if self.cbxGeneral4.isChecked():
                settings.general_preferences[settings.general_preference_keys[3]] = 1
            if self.cbxGeneral5.isChecked():
                settings.general_preferences[settings.general_preference_keys[4]] = 1
            if self.cbxGeneral6.isChecked():
                settings.general_preferences[settings.general_preference_keys[5]] = 1
            if self.cbxGeneral7.isChecked():
                settings.general_preferences[settings.general_preference_keys[6]] = 1
        elif self._main_form.model == "EPANET":
            if self.cbxGeneral1.isChecked():
                settings.general_preferences[settings.general_preference_keys[0]] = 1
            if self.cbxGeneral2.isChecked():
                settings.general_preferences[settings.general_preference_keys[1]] = 1
            if self.cbxGeneral3.isChecked():
                settings.general_preferences[settings.general_preference_keys[2]] = 1
            if self.cbxGeneral4.isChecked():
                settings.general_preferences[settings.general_preference_keys[3]] = 1
            if self.cbxGeneral5.isChecked():
                settings.general_preferences[settings.general_preference_keys[4]] = 1

        settings.node_numerical_preferences = self.local_node_preferences
        settings.link_numerical_preferences = self.local_link_preferences

        if self.cbxGeneral8.isChecked():
            self._main_form.program_settings.setValue('recentProjectList', '')
            self._main_form.update_recent(self._main_form.recent_projects, '')

        self._main_form.project_settings.sync_preferences()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
