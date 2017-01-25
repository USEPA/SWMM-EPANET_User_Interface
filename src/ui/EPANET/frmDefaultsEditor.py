import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui
from ui.frmGenericDefaultsEditorDesigner import Ui_frmGenericDefaultsEditor
from ui.inifile import ini_setting

class frmDefaultsEditor(QtGui.QMainWindow, Ui_frmGenericDefaultsEditor):
    def __init__(self, session, project, qsettings):
        QtGui.QMainWindow.__init__(self, session)
        self.setupUi(self)
        self.qsettings = qsettings
        self.session = session
        self.project = project
        if self.session is not None:
            self.setWindowTitle(self.session.model + " Project Defaults")
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.populate_defaults()

    def populate_defaults(self):
        while self.tabDefaults.count() < 3:
            c = self.tabDefaults.count()
            new_tab = QtGui.QWidget(self.tabDefaults)
            self.tabDefaults.addTab(new_tab, "tab_" + str(c + 1))

        while self.tabDefaults.count() > 3:
            c = self.tabDefaults.count()
            w = self.tabDefaults.widget(c - 1)
            self.tabDefaults.removeTab(c - 1)
            if w:
                del w


    def cmdOK_Clicked(self):
        self.close()
        pass

    def cmdCancel_Clicked(self):
        self.close()
        pass
