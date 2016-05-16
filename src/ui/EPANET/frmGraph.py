import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
import core.epanet.project
from ui.EPANET.frmGraphDesigner import Ui_frmGraph


class frmGraph(QtGui.QMainWindow, Ui_frmGraph):

    def __init__(self, parent):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdOK, QtCore.SIGNAL("clicked()"), self.cmdOK_Clicked)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._parent = parent
        # self.set_from(parent.project)

    # def set_from(self, project):
        # section = core.epanet.project.Control()
        # section = project.find_section(control_type)
        # self.txtControls.setPlainText(str(section.get_text()))

    def cmdOK_Clicked(self):
        # section = self._parent.project.find_section(self.control_type)
        # section.set_text(str(self.txtControls.toPlainText()))

        import matplotlib.pyplot as plt1
        # plt1.plot([1,2,3,4])
        # plt1.ylabel('some numbers')
        # plt1.show()

        import numpy as np
        import matplotlib.pyplot as plt2
        import matplotlib.dates as mdates
        # days, impressions = np.loadtxt("page-impressions.csv", unpack=True,
        # converters={ 0: mdates.strpdate2num('%Y-%m-%d')})

        days = ['2012-01-23','2012-01-24','2012-01-25','2012-01-29','2012-01-30']
        y_values = [3.0,4.1,5.0,2.3,3.1]
        mdates.strpdate2num('%Y-%m-%d')
        days_num = [mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[0]),
                    mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[1]),
                    mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[2]),
                    mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[3]),
                    mdates.strpdate2num.__call__(mdates.strpdate2num('%Y-%m-%d'), days[4])]

        plt2.plot_date(x=days_num, y=y_values, fmt="r-")
        plt2.title("Example time series plot")
        plt2.ylabel("Flow")
        plt2.grid(True)
        plt2.show()

        self.close()

    def cmdCancel_Clicked(self):
        self.close()
