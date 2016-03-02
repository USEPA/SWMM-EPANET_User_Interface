import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmTitleDesigner import Ui_frmTitle


class frmTitle(QtGui.QMainWindow, Ui_frmTitle):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        self.txtTitle.setPlainText(project.title.title)

    def cmdOK_Clicked(self):
        section = self._parent.project.title
        section.title = self.txtTitle.toPlainText()
        self.close()

    def cmdCancel_Clicked(self):
        self.close()