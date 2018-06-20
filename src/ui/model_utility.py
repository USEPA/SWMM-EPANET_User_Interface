from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QListWidget, QDialog, QVBoxLayout, QTextEdit, QPushButton, QSizePolicy
try:
    from PyQt5.QtCore import QString
except ImportError:
    QString = str

try:
    from_utf8 = QtCore.QString.fromUtf8
except AttributeError:
    def from_utf8(s):
        return s

try:
    transl8_encoding = QApplication.UnicodeUTF8
    def transl8(context, text, disambig=None):
        return QApplication.translate(context, text, disambig, transl8_encoding)
except AttributeError:
    def transl8(context, text, disambig=None):
        return QApplication.translate(context, text, disambig)

process_events = QApplication.processEvents
import matplotlib
matplotlib.use('agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.figure import Figure
from matplotlib import *

from threading import Thread, Event, Condition, Lock
from time import sleep

class ObjectTreeView(QTreeWidget):
    def __init__(self, parent, tree_top_item_list):
        QTreeWidget.__init__(self, parent)
        # self.setEditTriggers(QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)
        # self.setExpandsOnDoubleClick(False)
        # self.itemDoubleClicked.connect(self.edit_options)
        self.setHeaderHidden(True)
        self.setColumnCount(1)
        for top_list in tree_top_item_list:
            top_name = top_list[0]
            top_item = self.add_tree_item(self, 0, top_name, top_name)
            top_item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
            top_item.setExpanded(True)

            if len(top_list) > 1:
                children = top_list[1]
                if children and type(children) is list:
                    for child in children:
                        if child and len(child) > 0:
                            child_name = child[0]
                            child_control = self.add_tree_item(top_item, 0, child_name, child_name)
                            if len(child) > 0 and type(child[1]) is list:
                                for grandchild in child[1]:
                                    self.add_tree_item(child_control, 0, grandchild[0], grandchild[0])

    def add_tree_item(self, parent, column, title, data):
        item = QTreeWidgetItem(parent, [title])
        item.setData(column, QtCore.Qt.UserRole, data)
        return item

    def find_tree_item(self, text, root=None):
        if root is None:
            root = self.invisibleRootItem()
        for index in range(root.childCount()):
            node = root.child(index)
            if node.text(0) == text:
                return node
            else:
                found = self.find_tree_item(text, node)
                if found:
                    return found
        return None


class ObjectListView(QListWidget):
    def __init__(self, parent=None, **kwargs):
        QListWidget.__init__(self, parent)
        self.model = kwargs['model']
        self.ObjRoot = kwargs['ObjRoot']
        self.ObjType = kwargs['ObjType']
        self.ObjList = kwargs['ObjList']
        self.setupUI()

    def set_model(self, model):
        self.model = model

    def set_root(self, root):
        self.ObjRoot = root

    def set_type(self, obj_type):
        self.ObjType = obj_type

    def set_list(self, objList):
        self.ObjList = objList

    def setupUI(self):
        # self.addItem("Test")
        if self.ObjRoot:
            if self.ObjList:
                self.clear()
                for obj in self.ObjList:
                    self.addItem(obj)
                pass


class StatusMonitor0(QDialog):
    def __init__(self, cmd, args, parent=None, **kwargs):
        super(StatusMonitor0, self).__init__(parent)
        self.cmd = cmd
        self.args = args
        self.keepGoing = True
        self.prog = kwargs['model']

        layout = QVBoxLayout()
        self.output = QTextEdit()
        self.butt = QPushButton('Close')
        self.setupConnections()
        self.setWindowTitle('Running ' + self.prog)
        layout.addWidget(self.output)
        layout.addWidget(self.butt)
        layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout)
        self.butt.clicked.connect(self.close)

    def setupConnections(self):
        self.worker = Worker(self.cmd, self.args)
        self.worker.finished.connect(self.end_worker)
        self.worker.sendOutput.connect(self.showOutput)

    @QtCore.pyqtSlot(QString)
    def showOutput(self, output):
        while '\b\b' in output:
            output = output.replace('\b\b', '\b')
        self.output.append(output.replace('\b', '\n'))

    def end_worker(self):
        self.worker.process.kill()
        del self.worker

    def closeEvent(self,event):
        event.accept()

class Worker(QtCore.QObject):
    sendOutput = QtCore.pyqtSignal(QString)
    finished = QtCore.pyqtSignal()
    def __init__(self, cmd, args):
        super(Worker, self).__init__()
        self.cmd = cmd
        self.args = args
        self.process = QtCore.QProcess()
        self.setupProcess()

    def setupProcess(self):
        self.process.readyReadStandardOutput.connect(self.readStdOutput)
        self.process.start(self.cmd, self.args)
        self.finished.emit()

    @QtCore.pyqtSlot()
    def readStdOutput(self):
        output = QString(self.process.readAllStandardOutput())
        self.sendOutput.emit(output)

class ParseData:
    @staticmethod
    def intTryParse(value):
        try:
            if isinstance(value, int):
                return value, True
            else:
                if str(value):
                    if "null" in str(value).lower():
                        return value, False
                    return int(value), True
                else:
                    return None, False
        except ValueError:
            return value, False

    @staticmethod
    def floatTryParse(value):
        try:
            if isinstance(value, float):
                return value, True
            else:
                if str(value):
                    if "null" in str(value).lower():
                        return value, False
                    return float(value), True
                else:
                    return None, False
        except ValueError:
            return value, False

class BasePlot(FigureCanvas):
    def __init__(self, main_form=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.subplots_adjust(bottom=0.2)
        self.fig.subplots_adjust(left=0.15)

        self.axes = self.fig.add_subplot(111)
        self.label_size = 7
        self.axes.tick_params(labelsize=self.label_size)
        #self.axes.tight_layout()
        #self.axes.hold(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(main_form)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def setTitle(self, aTitle):
        if self.axes is not None:
            self.axes.set_title(aTitle)
        pass

    def setXlabel(self, aLabel):
        if self.axes is not None:
            self.axes.set_xlabel(aLabel, fontsize=self.label_size)
        # self.ax = plt.AxesSubplot() #debug only
        pass

    def setYlabel(self, aLabel):
        if self.axes is not None:
            self.axes.set_ylabel(aLabel, fontsize=self.label_size)
        pass

class MyProcess0(Thread):
    def __init__(self, wfunc, loop_steps):
        Thread.__init__(self)
        #flag to pause thread
        self.wfunc = wfunc
        self.loop_steps = loop_steps
        self.can_run = Event()
        self.thing_done = Event()
        self.can_run.set()
        self.thing_done.set()
        self.istart = 1
        self._is_running = True

    def run(self):
        while self._is_running:
            self.can_run.wait()
            try:
                self.thing_done.clear()
                for i in range(self.istart, self.loop_steps):
                    self.wfunc(i)
                    sleep(1)
                pass
            finally:
                self.thing_done.set()
                pass

    def pause(self):
        self.can_run.clear()
        self.thing_done.wait()
        # process_events()

    def resume(self, istart):
        self.istart = istart
        self.can_run.set()

    def stop(self):
        self._is_running = False


class MyProcess(Thread):
    def __init__(self, wfunc, loop_steps):
        Thread.__init__(self)
        #flag to pause thread
        self.wfunc = wfunc
        self.paused = False
        self.loop_steps = loop_steps
        self.pause_cond = Condition(Lock())
        self.istart = 1
        self._is_running = True

    def run(self):
        while True:
            with self.pause_cond:
                try:
                    for i in range(self.istart, self.loop_steps):
                        while self.paused:
                            self.pause_cond.wait()
                        if self._is_running:
                            self.wfunc(i)
                            sleep(2)
                        else:
                            # self._reset_internal_locks()
                            return
                except:
                    pass
                finally:
                    pass
        pass

    def pause(self):
        self.paused = True
        self.pause_cond.acquire()
        # process_events()

    def resume(self, istart):
        # self.istart = istart
        self.paused = False
        self.pause_cond.notify()
        self.pause_cond.release()

    def stop(self):
        self._is_running = False
        if self.paused:
            self.paused = False
            self.pause_cond.notify()
            self.pause_cond.release()

