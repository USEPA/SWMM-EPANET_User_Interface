import os
import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import traceback
from ui.help import HelpHandler
import ui.convenience
from ui.SWMM.frmTimeSeriesPlotDesigner import Ui_frmTimeSeriesPlot
from ui.SWMM.frmTimeSeriesSelection import frmTimeSeriesSelection
from core.graph import SWMM as graphSWMM

class frmTimeSeriesPlot(QMainWindow, Ui_frmTimeSeriesPlot):
    MAGIC = "TSGRAPHSPEC:"

    def __init__(self, session):
        self.session = session
        QMainWindow.__init__(self, session)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/timeseriesplotdialog.htm"
        self.setupUi(self)
        self.rbnDate.clicked.connect(self.rbnDate_Clicked)
        self.rbnElapsed.clicked.connect(self.rbnDate_Clicked)
        self.cmdOK.clicked.connect(self.cmdOK_Clicked)
        self.cmdCancel.clicked.connect(self.cmdCancel_Clicked)
        self.btnAdd.clicked.connect(self.btnAdd_Clicked)
        self.btnRemove.clicked.connect(self.btnRemove_Clicked)
        self.btnSave.clicked.connect(self.save_file)
        self.btnLoad.clicked.connect(self.load_file)
        self.btnScript.clicked.connect(self.save_script)
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
            # try:
            #     self.set_from_text(QApplication.clipboard().text())
            # except Exception as ex:
            #     print(str(ex))
            #     self.lstData.clear()

    def rbnDate_Clicked(self):
        self.cboStart.clear()
        self.cboEnd.clear()
        elapsed = self.rbnElapsed.isChecked()
        for time_index in range(0, self.output.num_periods):
            if elapsed:
                time_string = self.output.get_time_string(time_index)
            else:
                time_string = self.output.get_date_string(time_index)
            self.cboStart.addItem(time_string)
            self.cboEnd.addItem(time_string)
        # if self.cboStart.currentIndex < 0:
        self.cboStart.setCurrentIndex(0)
        self.cboEnd.setCurrentIndex(self.cboEnd.count() - 1)

    def add(self, object_type, object_name, variable, axis, legend):
        item = object_type + ',' + object_name + ',' + variable + ',' + axis + ',"' + legend + '"'
        self.lstData.addItem(item)

    def cboStart_currentIndexChanged(self):
        if self.cboEnd.currentIndex() < self.cboStart.currentIndex():
            self.cboEnd.setCurrentIndex(self.cboStart.currentIndex())

    def cboEnd_currentIndexChanged(self):
        if self.cboEnd.currentIndex() < self.cboStart.currentIndex():
            self.cboStart.setCurrentIndex(self.cboEnd.currentIndex())

    def btnAdd_Clicked(self):
        self._frmTimeSeriesSelection = frmTimeSeriesSelection(self.session)
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
        try:
            graphSWMM.plot_time(self.output, lines_list, elapsed_flag, start_index, num_steps)
        except Exception as e1:
            msg = str(e1) + '\n' + str(traceback.print_exc())
            print(msg)
            QMessageBox.information(None, "Plot",
                                    "Error plotting:\n" + msg,
                                    QMessageBox.Ok)

        # cb = QApplication.clipboard()
        # cb.clear(mode=cb.Clipboard)
        # cb.setText(self.get_text(), mode=cb.Clipboard)

    def save_script(self):
        directory = self.session.program_settings.value("ScriptDir", "")
        file_name, ftype = QFileDialog.getSaveFileName(self, "Save Plot Script As...", directory,
                                                            "Python Files (*.py);;All files (*.*)")
        if file_name:
            path_only, file_only = os.path.split(file_name)
            try:
                with open(file_name, 'w') as writer:
                    writer.write("from Externals.swmm.outputapi import SMOutputWrapper\n")
                    writer.write("from core.graph import SWMM as graphSWMM\n")
                    writer.write("output = SMOutputWrapper.SwmmOutputObject('" + self.output.output_file_name + "')\n")
                    writer.write("elapsed_flag = " + str(self.rbnElapsed.isChecked()) + "\n")
                    writer.write("start_index = " + str(self.cboStart.currentIndex()) + "\n")
                    if self.cboEnd.currentIndex() == self.output.num_periods:
                        writer.write("num_steps = -1\n")
                    else:
                        writer.write("end_index = " + str(self.cboEnd.currentIndex()) + "\n")
                        writer.write("num_steps = end_index - start_index + 1\n")
                    writer.write("lines_list = []\n")
                    for line in ui.convenience.all_list_items(self.lstData):
                        writer.write("lines_list.append('" + line + "')\n")
                    writer.write("graphSWMM.plot_time(output, lines_list, elapsed_flag, start_index, num_steps)\n")

                if path_only != directory:
                    self.session.program_settings.setValue("ScriptDir", path_only)
                    self.session.program_settings.sync()

            except Exception as e:
                print("Error writing {0}: {1}\n{2}".format(file_name, str(e), str(traceback.print_exc())))

    def cmdCancel_Clicked(self):
        self.close()

    def get_text_lines(self):
        return self.MAGIC + '\n' + '\n'.join([str(self.lstData.item(i).text()) for i in range(self.lstData.count())])

    def set_from_text_lines(self, lines):
        first_line = True
        for line in lines:  # text[len(self.MAGIC):].split('\n'):
            line = line.strip()
            if line:
                if first_line:
                    if line == self.MAGIC:
                        self.lstData.clear()
                        first_line = False
                    else:
                        return
                else:
                    self.lstData.addItem(line)

    def save_file(self):
        directory = self.session.program_settings.value("PlotSpecDir", "")
        file_name, ftype = QFileDialog.getSaveFileName(self, "Save Plot Specification As...", directory,
                                                           "Time Series Plot (*.tsplt);;All files (*.*)")
        if file_name:
            try:
                with open(file_name, 'w') as writer:
                    writer.write(self.get_text_lines())
                    path_only, file_only = os.path.split(file_name)
                    if path_only != directory:
                        self.session.program_settings.setValue("PlotSpecDir", path_only)
                        self.session.program_settings.sync()

            except Exception as e:
                print("Error writing {0}: {1}\n{2}".format(file_name, str(e), str(traceback.print_exc())))

    def load_file(self):
        directory = self.session.program_settings.value("PlotSpecDir", "")
        file_name, ftype = QFileDialog.getOpenFileName(self, "Open Time Series Plot Specification...", directory,
                                                            "Time Series Plot (*.tsplt);;All files (*.*)")
        if file_name:
            try:
                with open(file_name, 'r') as inp_reader:
                    self.set_from_text_lines(iter(inp_reader))
                    path_only, file_only = os.path.split(file_name)
                    if path_only != directory:
                        self.session.program_settings.setValue("PlotSpecDir", path_only)
                        self.session.program_settings.sync()
            except Exception as e:
                print("Error reading {0}: {1}\n{2}".format(file_name, str(e), str(traceback.print_exc())))

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
