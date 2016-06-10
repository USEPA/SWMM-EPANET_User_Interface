import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.swmm.project
import ui.convenience
from ui.SWMM.frmTimeSeriesPlotDesigner import Ui_frmTimeSeriesPlot
from ui.SWMM.frmTimeSeriesSelection import frmTimeSeriesSelection
from core.graph import SWMM as graphSWMM

class frmTimeSeriesPlot(QtGui.QMainWindow, Ui_frmTimeSeriesPlot):
    MAGIC = "TSGRAPHSPEC:\n"

    def __init__(self, main_form):
        self._main_form = main_form
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        QtCore.QObject.connect(self.rbnDate, QtCore.SIGNAL("clicked()"), self.rbnDate_Clicked)
        QtCore.QObject.connect(self.rbnElapsed, QtCore.SIGNAL("clicked()"), self.rbnDate_Clicked)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        QtCore.QObject.connect(self.btnAdd, QtCore.SIGNAL("clicked()"), self.btnAdd_Clicked)
        QtCore.QObject.connect(self.btnRemove, QtCore.SIGNAL("clicked()"), self.btnRemove_Clicked)
        self.cboStart.currentIndexChanged.connect(self.cboStart_currentIndexChanged)
        self.cboEnd.currentIndexChanged.connect(self.cboEnd_currentIndexChanged)
        # self.installEventFilter(self)

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboStart.clear()
        if project and self.output:
            self.rbnElapsed.setChecked(True)
            self.rbnDate_Clicked()
            try:
                self.set_from_text(QtGui.QApplication.clipboard().text())
            except Exception as ex:
                print(str(ex))
                self.lstData.clear()

    def rbnDate_Clicked(self):
        self.cboStart.clear()
        self.cboEnd.clear()
        elapsed = self.rbnElapsed.isChecked()
        for time_index in range(0, self.output.numPeriods):
            if elapsed:
                time_string = self.output.get_time_string(time_index)
            else:
                time_string = self.output.get_date_string(time_index)
            self.cboStart.addItem(time_string)
            self.cboEnd.addItem(time_string)
        # if self.cboStart.currentIndex < 0:
        self.cboStart.setCurrentIndex(0)
        self.cboEnd.setCurrentIndex(self.cboEnd.count() - 1)

    def add(self, object_type, object_id, variable, axis, legend):
        item = object_type + ',' + object_id + ',' + variable + ',' + axis + ',"' + legend + '"'
        self.lstData.addItem(item)

    def cboStart_currentIndexChanged(self):
        if self.cboEnd.currentIndex() < self.cboStart.currentIndex():
            self.cboEnd.setCurrentIndex(self.cboStart.currentIndex())

    def cboEnd_currentIndexChanged(self):
        if self.cboEnd.currentIndex() < self.cboStart.currentIndex():
            self.cboStart.setCurrentIndex(self.cboEnd.currentIndex())

    def btnAdd_Clicked(self):
        self._frmTimeSeriesSelection = frmTimeSeriesSelection(self._main_form)
        self._frmTimeSeriesSelection.set_from(self.project, self.output, self.add)
        self._frmTimeSeriesSelection.show()

    def btnRemove_Clicked(self):
        for item in self.lstData.selectedItems():
            self.lstData.takeItem(self.lstData.row(item))

    def cmdOK_Clicked(self):
        elapsed_flag = self.rbnElapsed.isChecked()
        start_index = self.cboStart.currentIndex()
        end_index = self.cboEnd.currentIndex()
        num_steps = end_index - start_index + 1
        lines_list = ui.convenience.all_list_items(self.lstData)
        graphSWMM.plot_time(self.output, lines_list, elapsed_flag, start_index, num_steps)
        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.get_text(), mode=cb.Clipboard)

    def cmdCancel_Clicked(self):
        self.close()

    def get_text(self):
        return self.MAGIC + '\n'.join([str(self.lstData.item(i).text()) for i in range(self.lstData.count())])

    def set_from_text(self, text):
        if text.startswith(self.MAGIC):
            self.lstData.clear()
            for line in text[len(self.MAGIC):].split('\n'):
                self.lstData.addItem(line)

    # def keyPressEvent(self, event):
    #     if type(event) == QtGui.QKeyEvent:
    #          #here accept the event and do something
    #         print event.key()   # Key Code gets printed to the console
    #         event.accept()
    #         print(event.text())
    #
    # def eventFilter(self, obj, event):
    #     if event.type() == QtCore.QEvent.KeyPress:
    #         print "eventFilter " + event.key()   # Key Code gets printed to the console
    #         if event.key() in [QtCore.Qt.Key_Copy]:
    #             cb = QtGui.QApplication.clipboard()
    #             cb.clear(mode=cb.Clipboard)
    #             cb.setText('\n'.join([str(self.lstData.item(i).text()) for i in range(self.lstData.count())]),
    #                        mode=cb.Clipboard)
    #             return True
    #         elif event.key() in [QtCore.Qt.Key_Paste]:
    #             cb = QtGui.QApplication.clipboard()
    #             self.lstData.clear()
    #             for line in cb.getText():
    #                 self.lstData.addItem(line)
    #             return True
    #     return False
