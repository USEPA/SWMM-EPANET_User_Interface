import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmProfilePlotDesigner import Ui_frmProfilePlot
from ui.help import HelpHandler


class frmProfilePlot(QtGui.QMainWindow, Ui_frmProfilePlot):
    MAGIC = "SWMM_PROFILE_GRAPH_SPEC:\n"

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/profileplotoptionsdialog.htm"
        self._main_form = main_form
        self.setupUi(self)
        self.cmdFind.setEnabled(False)  # TODO: Enable when functionality is ready
        self.cmdSave.setText("Copy")
        self.cmdUse.setText("Paste")
        QtCore.QObject.connect(self.cmdSave, QtCore.SIGNAL("clicked()"), self.cmdSave_Clicked)
        QtCore.QObject.connect(self.cmdUse, QtCore.SIGNAL("clicked()"), self.cmdUse_Clicked)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        self.cboEnd.clear()
        if project and self.output:
            for node in self.output.nodes:
                self.cboStart.addItem(node.id)
                self.cboEnd.addItem(node.id)
            for link in self.output.links:
                self.lstData.addItem(link.id)

    def get_text(self):
        return self.MAGIC + '\n'.join([str(self.lstData.item(i).text()) for i in range(self.lstData.count())])

    def set_from_text(self, text):
        if text.startswith(self.MAGIC):
            self.lstData.clear()
            for line in text[len(self.MAGIC):].split('\n'):
                self.lstData.addItem(line)

    def cmdSave_Clicked(self):
        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.get_text(), mode=cb.Clipboard)

    def cmdUse_Clicked(self):
        try:
            self.set_from_text(QtGui.QApplication.clipboard().text())
        except Exception as ex:
            print(str(ex))
            self.lstData.clear()

    def cmdOK_Clicked(self):
        pass

    def cmdCancel_Clicked(self):
        self.close()
