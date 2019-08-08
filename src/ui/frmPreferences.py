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

        elif self._main_form.model == "EPANET":
            self.lblSubcatchment.setVisible(False)
            self.cboSubcatchment.setVisible(False)
            self.lblDecimal1.setVisible(False)
            self.spnSubcatchment.setVisible(False)

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
        settings.node_numerical_preferences = self.local_node_preferences
        settings.link_numerical_preferences = self.local_link_preferences
        self._main_form.project_settings.sync_preferences()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
