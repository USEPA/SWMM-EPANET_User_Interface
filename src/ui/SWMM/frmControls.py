import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
from ui.SWMM.frmControlsDesigner import Ui_frmControls
from ui.help import HelpHandler


class frmControls(QtGui.QMainWindow, Ui_frmControls):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.help_topic = "swmm/src/src/controlrules.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

        self.set_from(parent.project)
        self._parent = parent

    def set_from(self, project):
        # section = core.epanet.project.Control()
        section = project.find_section("CONTROLS")
        self.txtControls.setPlainText(str(section.get_text()))

    def cmdOK_Clicked(self):
        section = self._parent.project.find_section("CONTROLS")
        section.set_text(str(self.txtControls.toPlainText()))
        self.close()

    def cmdCancel_Clicked(self):
        self.close()

    # def keyPressEvent(self, event):
    #     if event.key() == 16777264:
    #         # open qt assistant for help
    #         program = "/Qt/Qt5.5.1/5.5/msvc2013_64/bin/assistant.exe"
    #         arguments = ["-collectionFile", "/dev/Python/SWMM-EPANET_User_Interface_svn/trunk/doc/SWMM/swmm.qhc", "-enableRemoteControl"]
    #         self.process = QtCore.QProcess()
    #         self.process.start(program, arguments)
    #
    #         # set to the right page
    #         ba = QtCore.QByteArray()
    #         ba.append("setSource qthelp://swmm/src/src/controlrules.htm\n")
    #         self.process.write(ba)