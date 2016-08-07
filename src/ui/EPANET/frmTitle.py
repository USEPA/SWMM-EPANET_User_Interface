import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.EPANET.frmTitleDesigner import Ui_frmTitle


class frmTitle(QtGui.QMainWindow, Ui_frmTitle):
    def __init__(self, main_form=None):
        QtGui.QMainWindow.__init__(self, main_form)
        self.help_topic = "epanet/src/src/Pipes.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(main_form.project)
        self._main_form = main_form

    def set_from(self, project):
        # section = core.epanet.project.Title()
        self.txtTitle.setPlainText(str(project.title.title))

    def cmdOK_Clicked(self):
        section = self._main_form.project.title
        section.title = self.txtTitle.toPlainText()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()
