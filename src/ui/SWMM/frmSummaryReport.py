import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.SWMM.frmSummaryReportDesigner import Ui_frmSummaryReport


class frmSummaryReport(QtGui.QMainWindow, Ui_frmSummaryReport):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._main_form = main_form
        self.cboType.currentIndexChanged.connect(self.cboType_currentIndexChanged)

    def set_from(self, project, status_file_name):
        self.project = project
        self.status_file_name = status_file_name
        self.cboType.clear()
        if project and self.status_file_name:

            potential_topics = ['Subcatchment Runoff',
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

            topics = []
            try:
                with open(status_file_name, 'r') as inp_reader:
                    for line in iter(inp_reader):
                        for potential_topic in potential_topics:
                            if line.startswith('  ' + potential_topic + ' Summary'):
                                topics.append(potential_topic)
                    self.cboType.addItems(topics)
                    self.cboType.setCurrentIndex(0)
            except Exception as e:
               print("Error reading " + status_file_name)

    def cboType_currentIndexChanged(self, newIndex):
        if self.cboType.count() > 0:
            headers = []
            real_rows = []
            row_labels = []
            nrows = 0
            ncols = 0
            try:
                with open(self.status_file_name, 'r') as inp_reader:
                    found_start = False
                    reading_headers = False
                    reading_real = False
                    for line in iter(inp_reader):
                        if line.startswith('  ' + self.cboType.currentText() + ' Summary'):
                            found_start = True
                        elif found_start:
                            if reading_real:
                                if len(line.strip()) == 0:
                                    reading_real = False
                                    found_start = False
                                else:
                                    line_list = line.split()
                                    real_rows.append(line_list)
                                    row_labels.append(line_list[0])
                            elif reading_headers:
                                if line.startswith('  -------'):
                                    reading_headers = False
                                    reading_real = True
                                else:
                                    headers.append(line)
                            elif reading_headers == False and line.startswith('  -------'):
                                reading_headers = True
                    self.tblSummary.setVerticalHeaderLabels(row_labels)
                    nrows = len(real_rows)
                    ncols = len(real_rows[0]) - 1
                    self.tblSummary.setRowCount(nrows)
                    self.tblSummary.setColumnCount(ncols)

                    column_headers = []
                    if self.cboType.currentText() == 'Subcatchment Runoff':
                        Units1 = ' in'
                        Units2 = ' 10^6 gal'
                        Units3 = ' CFS'
                        headers = ['Precip' + Units1,'Runon' + Units1,'Total Evap' + Units1,'Total Infil' + Units1,
                                  'Total Runoff' + Units1,'Total Runoff' + Units2,'Peak Runoff' + Units3,'Runoff Coeff']
                    elif self.cboType.currentText() == 'LID Performance':
                        Units1 = ' in'
                        headers = ['LID Control','Total Inflow' + Units1,'Evap Loss' + Units1,'Infil Loss' + Units1,
                                   'Surface Outflow' + Units1,'Drain Outflow' + Units1,'Initial Storage' + Units1,
                                   'Final Storage' + Units1,'Continuity Error %']
                    elif self.cboType.currentText() == 'Groundwater':
                        Units1 = ' in'
                        Units2 = ' 10^6 gal'
                        Units3 = ' CFS'
                        headers = ['Total Infil' + Units1,'Total Evap' + Units1,'Total Lower Seepage' + Units1,
                                   'Total Lateral Outflow' + Units1,'Maximum Lateral Outflow' + Units2,'Average Upper Moisture',
                                  'Average Water Table' + Units3,'Final Upper Moisture','Final Water Table' + Units3]
                    elif self.cboType.currentText() == 'Subcatchment Washoff':
                        Units1 = ' in'
                        headers = ['Pollutant 1' + Units1,'Pollutant 2' + Units1]
                    elif self.cboType.currentText() == 'Node Depth':
                        Units1 = ' in'
                        headers = ['Type','Average Depth' + Units1,'Maximum Depth' + Units1,'Maximum HGL' + Units1,
                                   'Day of Maximum Depth','Hour of Maximum Depth','Maximum Reported Depth' + Units1]
                    elif self.cboType.currentText() == 'Node Inflow':
                        Units1 = ' in'
                        Units2 = ' in'
                        headers = ['Type','Maximum Lateral Inflow' + Units1,'Maximum Total Inflow' + Units1,'Day of Maximum Inflow',
                                   'Hour of Maximum Inflow','Lateral Inflow Volume' + Units2,'Total Inflow Volume' + Units2,
                                   'Flow Balance Error Percent']
                    elif self.cboType.currentText() == 'Node Surcharge':
                        Units1 = ' in'
                        headers = ['Type','Hours Surcharged','Max Height Above Crown' + Units1,'Min Depth Below Rim' + Units1]
                    elif self.cboType.currentText() == 'Node Flooding':
                        Units1 = ' in'
                        Units2 = ' 10^6 gal'
                        Units3 = ' CFS'
                        headers = ['Hours Flooded','Maximum Rate' + Units1,'Day of Maximum Flooding','Hour of Maximum Flooding',
                                   'Total Flood Volume' + Units2,'Maximum Ponded Volume' + Units3]
                    elif self.cboType.currentText() == 'Storage Volume':
                        Units1 = ' in'
                        Units2 = ' 10^6 gal'
                        headers = ['Average Volume' + Units1,'Average Percent Full','Evap Percent Loss','Exfil Percent Loss',
                                   'Maximum Volume' +Units1,'Maximum Percent Full','Day of Maximum Volume','Hour of Maximum Volume',
                                   'Maximum Outflow' +Units2]
                    elif self.cboType.currentText() == 'Outfall Loading':
                        Units1 = ' in'
                        Units2 = ' 10^6 gal'
                        Units3 = ' CFS'
                        headers = ['Flow Freq. Pcnt.','Avg. Flow' + Units1,'Max. Flow' + Units1,'Total Volume' + Units2,
                                   'Pollutant 1' + Units3,'Pollutant 2' + Units3]
                    elif self.cboType.currentText() == 'Link Flow':
                        Units1 = ' in'
                        Units2 = ' 10^6 gal'
                        headers = ['Type','Maximum |Flow|' + Units1,'Day of Maximum Flow','Hour of Maximum Flow',
                                   'Maximum |Velocity|' + Units2,'Max / Full Flow','Max / Full Depth']
                    elif self.cboType.currentText() == 'Flow Classification':
                        headers = ['Adjusted/ Actual Length','Fully Dry','Upstrm Dry','Dnstrm Dry','Sub Critical','Super Critical',
                                   'Upstrm Critical','Dnstrm Critical','Normal Flow Limited','Inlet Control']
                    elif self.cboType.currentText() == 'Conduit Surcharge':
                        headers = ['Hours Both Ends Full','Hours Upstream Full','Hours Dnstream Full','Hours Above Normal Flow',
                                   'Hours Capacity Limited']
                    elif self.cboType.currentText() == 'Pumping':
                        Units1 = ' in'
                        Units2 = ' 10^6 gal'
                        Units3 = ' CFS'
                        headers = ['Percent Utilized','Number of Start-Ups','Minimum Flow' + Units1,'Average Flow' + Units1,
                                   'Maximum Flow' + Units1,'Total Volume' + Units2,'Power Usage' + Units3,
                                   '% Time Below Pump Curve','% Time Above Pump Curve']
                    elif self.cboType.currentText() == 'Link Pollutant Load':
                        Units1 = ' in'
                        headers = ['Pollutant 1' + Units1,'Pollutant 2' + Units1]
                    self.tblSummary.setHorizontalHeaderLabels(headers)

                    row = -1
                    for line_list in real_rows:
                        col = -1
                        row += 1
                        for value in line_list[1:]:
                            col += 1
                            item = QtGui.QTableWidgetItem(value)
                            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                            self.tblSummary.setItem(row,col,item)
            except Exception as e:
                print("Error reading " + self.status_file_name)

    def cmdCancel_Clicked(self):
        self.close()
