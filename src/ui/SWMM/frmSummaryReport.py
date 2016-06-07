import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmSummaryReportDesigner import Ui_frmSummaryReport
import Externals.swmm.outputapi.SMOutputWrapper as SMO


class frmSummaryReport(QtGui.QMainWindow, Ui_frmSummaryReport):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._main_form = main_form
        self.cboType.currentIndexChanged.connect(self.cboType_currentIndexChanged)

    def set_from(self, project, output):
        self.project = project
        self.output = output
        self.cboType.clear()
        if project and self.output:
            self.subcatchment_items = self.output.subcatchment_ids
            self.subcatchment_variables = SMO.SMO_subcatchAttributeNames
            # ('Precipitation', 'Snow Depth', 'Evaporation', 'Infiltration', 'Runoff', 'Groundwater Flow', 'Groundwater Elevation', 'Soil Moisture', 'Concentration')
            self.node_items = self.output.node_ids
            self.node_variables = SMO.SMO_nodeAttributeNames
            # ('Depth', 'Head', 'Volume', 'Lateral Inflow', 'Total Inflow', 'Flooding', 'TSS')
            self.link_items = self.output.link_ids
            self.link_variables = SMO.SMO_linkAttributeNames
            # ('Flow', 'Depth', 'Velocity', 'Volume', 'Capacity', 'Concentration')

            topics = ['Subcatchment Runoff',
                    'LID Performance',
                    'Groundwater',
                    'Subcatchment Washoff',
                    'Node Depth',
                    'Node Inflow',
                    'Node Surcharge',
                    'Node Flooding',
                    'Storage Volume',
                    'Outfall Loading',
                    'Link Flow',
                    'Flow Classification',
                    'Conduit Surcharge',
                    'Pumping',
                    'Link Pollutant Load']
            self.cboType.addItems(topics)
            self.cboType.setCurrentIndex(0)

    def cboType_currentIndexChanged(self, newIndex):
        nrows = 0
        ncols = 0
        headers = []
        if self.cboType.currentText() == 'Subcatchment Runoff':
            nrows = len(self.subcatchment_items)
            ncols = 8
            self.tblSummary.setVerticalHeaderLabels(self.subcatchment_items)
            Units1 = ' in'
            Units2 = ' 10^6 gal'
            Units3 = ' CFS'
            headers = ['Precip' + Units1,'Runon' + Units1,'Total Evap' + Units1,'Total Infil' + Units1,
                       'Total Runoff' + Units1,'Total Runoff' + Units2,'Peak Runoff' + Units3,'Runoff Coeff']
        elif self.cboType.currentText() == 'LID Performance':
            nrows = len(self.subcatchment_items)
            ncols = 9
            self.tblSummary.setVerticalHeaderLabels(self.subcatchment_items)
            Units1 = ' in'
            headers = ['LID Control','Total Inflow' + Units1,'Evap Loss' + Units1,'Infil Loss' + Units1,
                       'Surface Outflow' + Units1,'Drain Outflow' + Units1,'Initial Storage' + Units1,
                       'Final Storage' + Units1,'Continuity Error %']
        elif self.cboType.currentText() == 'Groundwater':
            nrows = len(self.subcatchment_items)
            ncols = 9
            self.tblSummary.setVerticalHeaderLabels(self.subcatchment_items)
            Units1 = ' in'
            Units2 = ' 10^6 gal'
            Units3 = ' CFS'
            headers = ['Total Infil' + Units1,'Total Evap' + Units1,'Total Lower Seepage' + Units1,
                       'Total Lateral Outflow' + Units1,'Maximum Lateral Outflow' + Units2,'Average Upper Moisture',
                       'Average Water Table' + Units3,'Final Upper Moisture','Final Water Table' + Units3]
        elif self.cboType.currentText() == 'Subcatchment Washoff':
            nrows = len(self.subcatchment_items)
            ncols = 2   # need actual number of pollutants
            self.tblSummary.setVerticalHeaderLabels(self.subcatchment_items)
            Units1 = ' in'
            headers = ['Pollutant 1' + Units1,'Pollutant 2' + Units1]
        elif self.cboType.currentText() == 'Node Depth':
            nrows = len(self.node_items)
            ncols = 7
            self.tblSummary.setVerticalHeaderLabels(self.node_items)
            Units1 = ' in'
            headers = ['Type','Average Depth' + Units1,'Maximum Depth' + Units1,'Maximum HGL' + Units1,
                       'Day of Maximum Depth','Hour of Maximum Depth','Maximum Reported Depth' + Units1]
        elif self.cboType.currentText() == 'Node Inflow':
            nrows = len(self.node_items)
            ncols = 8
            self.tblSummary.setVerticalHeaderLabels(self.node_items)
            Units1 = ' in'
            Units2 = ' in'
            headers = ['Type','Maximum Lateral Inflow' + Units1,'Maximum Total Inflow' + Units1,'Day of Maximum Inflow',
                       'Hour of Maximum Inflow','Lateral Inflow Volume' + Units2,'Total Inflow Volume' + Units2,
                       'Flow Balance Error Percent']
        elif self.cboType.currentText() == 'Node Surcharge':
            nrows = len(self.node_items)
            ncols = 4
            self.tblSummary.setVerticalHeaderLabels(self.node_items)
            Units1 = ' in'
            headers = ['Type','Hours Surcharged','Max Height Above Crown' + Units1,'Min Depth Below Rim' + Units1]
        elif self.cboType.currentText() == 'Node Flooding':
            nrows = len(self.node_items)
            ncols = 6
            self.tblSummary.setVerticalHeaderLabels(self.node_items)
            Units1 = ' in'
            Units2 = ' 10^6 gal'
            Units3 = ' CFS'
            headers = ['Hours Flooded','Maximum Rate' + Units1,'Day of Maximum Flooding','Hour of Maximum Flooding',
                       'Total Flood Volume' + Units2,'Maximum Ponded Volume' + Units3]
        elif self.cboType.currentText() == 'Storage Volume':
            nrows = len(self.node_items)
            ncols = 9
            self.tblSummary.setVerticalHeaderLabels(self.node_items)
            Units1 = ' in'
            Units2 = ' 10^6 gal'
            headers = ['Average Volume' + Units1,'Average Percent Full','Evap Percent Loss','Exfil Percent Loss',
                       'Maximum Volume' +Units1,'Maximum Percent Full','Day of Maximum Volume','Hour of Maximum Volume',
                       'Maximum Outflow' +Units2]
        elif self.cboType.currentText() == 'Outfall Loading':
            nrows = len(self.node_items)
            ncols = 6
            self.tblSummary.setVerticalHeaderLabels(self.node_items)
            Units1 = ' in'
            Units2 = ' 10^6 gal'
            Units3 = ' CFS'
            headers = ['Flow Freq. Pcnt.','Avg. Flow' + Units1,'Max. Flow' + Units1,'Total Volume' + Units2,
                       'Pollutant 1' + Units3,'Pollutant 2' + Units3]
        elif self.cboType.currentText() == 'Link Flow':
            nrows = len(self.link_items)
            ncols = 7
            self.tblSummary.setVerticalHeaderLabels(self.link_items)
            Units1 = ' in'
            Units2 = ' 10^6 gal'
            headers = ['Type','Maximum |Flow|' + Units1,'Day of Maximum Flow','Hour of Maximum Flow',
                       'Maximum |Velocity|' + Units2,'Max / Full Flow','Max / Full Depth']
        elif self.cboType.currentText() == 'Flow Classification':
            nrows = len(self.link_items)
            ncols = 10
            self.tblSummary.setVerticalHeaderLabels(self.link_items)
            headers = ['Adjusted/ Actual Length','Fully Dry','Upstrm Dry','Dnstrm Dry','Sub Critical','Super Critical',
                       'Upstrm Critical','Dnstrm Critical','Normal Flow Limited','Inlet Control']
        elif self.cboType.currentText() == 'Conduit Surcharge':
            nrows = len(self.link_items)
            ncols = 5
            self.tblSummary.setVerticalHeaderLabels(self.link_items)
            headers = ['Hours Both Ends Full','Hours Upstream Full','Hours Dnstream Full','Hours Above Normal Flow',
                       'Hours Capacity Limited']
        elif self.cboType.currentText() == 'Pumping':
            nrows = len(self.link_items)
            ncols = 9
            self.tblSummary.setVerticalHeaderLabels(self.link_items)
            Units1 = ' in'
            Units2 = ' 10^6 gal'
            Units3 = ' CFS'
            headers = ['Percent Utilized','Number of Start-Ups','Minimum Flow' + Units1,'Average Flow' + Units1,
                       'Maximum Flow' + Units1,'Total Volume' + Units2,'Power Usage' + Units3,
                       '% Time Below Pump Curve','% Time Above Pump Curve']
        elif self.cboType.currentText() == 'Link Pollutant Load':
            nrows = len(self.link_items)
            ncols = 2
            self.tblSummary.setVerticalHeaderLabels(self.link_items)
            Units1 = ' in'
            headers = ['Pollutant 1' + Units1,'Pollutant 2' + Units1]

        self.tblSummary.setRowCount(nrows)
        self.tblSummary.setColumnCount(ncols)
        self.tblSummary.setHorizontalHeaderLabels(headers)
        for col in range(ncols):
            for row in range(nrows):
                led = QtGui.QLineEdit(str(1.0))
                item = QtGui.QTableWidgetItem(led.text())
                item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                self.tblSummary.setItem(row,col,item)

    def cmdCancel_Clicked(self):
        self.close()
