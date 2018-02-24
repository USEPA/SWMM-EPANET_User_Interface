import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from ui.help import HelpHandler
from ui.SWMM.frmSummaryReportDesigner import Ui_frmSummaryReport


class frmSummaryReport(QtGui.QMainWindow, Ui_frmSummaryReport):

    def __init__(self, main_form):
        QtGui.QMainWindow.__init__(self, main_form)
        self.helper = HelpHandler(self)
        self.help_topic = "swmm/src/src/viewing_a_summary_report.htm"
        self.setupUi(self)
        QtCore.QObject.connect(self.cmdCancel, QtCore.SIGNAL("clicked()"), self.cmdCancel_Clicked)
        # self.set_from(parent.project)   # do after init to set control type CONTROLS or RULES
        self._main_form = main_form
        self.label.setVisible(False)  # since sorting seems buggy, take this off for now
        self.tblSummary.setSortingEnabled(False)
        self.cboType.currentIndexChanged.connect(self.cboType_currentIndexChanged)
        self.tblSummary.setSortingEnabled(False)

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
                        if line.startswith('  No nodes were surcharged.'):
                            potential_topics.remove('Node Surcharge')
                        elif line.startswith('  No nodes were flooded.'):
                            potential_topics.remove('Node Flooding')
                        elif line.startswith('  No conduits were surcharged.'):
                            potential_topics.remove('Conduit Surcharge')

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
        self.tblSummary.setSortingEnabled(False)
        if self.cboType.count() > 0:
            headers = []
            real_rows = []
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
                                if len(line.strip()) == 0 or line.startswith('  -------'):
                                    reading_real = False
                                    found_start = False
                                else:
                                    line_list = line.split()
                                    real_rows.append(line_list)
                            elif reading_headers:
                                if line.startswith('  -------'):
                                    reading_headers = False
                                    reading_real = True
                                else:
                                    headers.append(line)
                            elif reading_headers == False and line.startswith('  -------'):
                                reading_headers = True
                    nrows = len(real_rows)
                    ncols = len(real_rows[0])
                    self.tblSummary.setRowCount(nrows)
                    self.tblSummary.setColumnCount(ncols)
                    self.tblSummary.verticalHeader().setVisible(False)

                    column_headers = []
                    total_num_headers = len(headers)
                    header_list = headers[total_num_headers-1].split()
                    if self.cboType.currentText() == 'LID Performance':
                        Units1 = header_list[3]
                        column_headers = ['Subcatchment',
                                          'LID Control',
                                          'Total Inflow' + '\n' + Units1,
                                          'Evap Loss' + '\n' + Units1,
                                          'Infil Loss' + '\n' + Units1,
                                          'Surface Outflow' + '\n' + Units1,
                                          'Drain Outflow' + '\n' + Units1,
                                          'Initial Storage' + '\n' + Units1,
                                          'Final Storage' + '\n' + Units1,
                                          'Continuity Error %']
                    elif self.cboType.currentText() == 'Groundwater':
                        Units1 = header_list[3]
                        Units2 = header_list[5]
                        Units3 = header_list[6]
                        column_headers = ['Subcatchment',
                                          'Total' + '\n' + 'Infil' + '\n' + Units1,
                                          'Total' + '\n' + 'Evap' + '\n' + Units1,
                                          'Total' + '\n' + 'Lower' + '\n' + 'Seepage' + '\n' + Units1,
                                          'Total' + '\n' + 'Lateral' + '\n' + 'Outflow' + '\n' + Units1,
                                          'Maximum' + '\n' + 'Lateral' + '\n' + 'Outflow' + '\n' + Units2,
                                          'Average' + '\n' + 'Upper' + '\n' + 'Moisture',
                                          'Average' + '\n' + 'Water' + '\n' + 'Table' + '\n' + Units3,
                                          'Final' + '\n' + 'Upper' + '\n' + 'Moisture',
                                          'Final' + '\n' + 'Water' + '\n' + 'Table' + '\n' + Units3]
                    elif self.cboType.currentText() == 'Node Depth':
                        Units1 = header_list[3]
                        column_headers = ['Node',
                                          'Type',
                                          'Average' + '\n' + 'Depth' + '\n' + Units1,
                                          'Maximum' + '\n' + 'Depth' + '\n' + Units1,
                                          'Maximum' + '\n' + 'HGL' + '\n' + Units1,
                                          'Day of' + '\n' + 'Maximum' + '\n' + ' Depth',
                                          'Hour of' + '\n' + 'Maximum' + '\n' + 'Depth',
                                          'Maximum' + '\n' + 'Reported' + '\n' + 'Depth' + '\n' + Units1]
                    elif self.cboType.currentText() == 'Node Inflow':
                        Units1 = header_list[3]
                        Units2 = header_list[6] + ' ' + header_list[7]
                        column_headers = ['Node',
                                          'Type',
                                          'Maximum' + '\n' + 'Lateral' + '\n' + 'Inflow' + '\n' + Units1,
                                          'Maximum' + '\n' + 'Total' + '\n' + 'Inflow' + '\n' + Units1,
                                          'Day of' + '\n' + 'Maximum' + '\n' + 'Inflow',
                                          'Hour of' + '\n' + 'Maximum' + '\n' + 'Inflow',
                                          'Lateral' + '\n' + 'Inflow' + '\n' + 'Volume' + '\n' + Units2,
                                          'Total' + '\n' + 'Inflow' + '\n' + 'Volume' + '\n' + Units2,
                                          'Flow' + '\n' + 'Balance' + '\n' + 'Error' + '\n' + 'Percent']
                    elif self.cboType.currentText() == 'Node Surcharge':
                        Units1 = header_list[3]
                        column_headers = ['Node',
                                          'Type',
                                          'Hours' + '\n' + 'Surcharged',
                                          'Max Height' + '\n' + 'Above' + '\n' + 'Crown' + '\n' + Units1,
                                          'Min Depth' + '\n' + 'Below' + '\n' + 'Rim' + '\n' + Units1]
                    elif self.cboType.currentText() == 'Node Flooding':
                        Units1 = header_list[2]
                        Units2 = header_list[5] + ' ' + header_list[6]
                        Units3 = header_list[7]
                        column_headers = ['Node',
                                          'Hours' + '\n' + 'Flooded',
                                          'Maximum' + '\n' + 'Rate' + '\n' + Units1,
                                          'Day of' + '\n' + 'Maximum' + '\n' + 'Flooding',
                                          'Hour of' + '\n' + 'Maximum' + '\n' + 'Flooding',
                                          'Total' + '\n' + 'Flood' + '\n' + 'Volume' + '\n' + Units2,
                                          'Maximum' + '\n' + 'Ponded' + '\n' + 'Depth' + '\n' + Units3]
                    elif self.cboType.currentText() == 'Storage Volume':
                        Units1 = header_list[2] + ' ' + header_list[3]
                        Units2 = header_list[12]
                        column_headers = ['Node',
                                          'Average' + '\n' + 'Volume' + '\n' + Units1,
                                          'Average' + '\n' + 'Percent' + '\n' + 'Full',
                                          'Evap' + '\n' + 'Percent' + '\n' + 'Loss',
                                          'Exfil' + '\n' + 'Percent' + '\n' + 'Loss',
                                          'Maximum' + '\n' + 'Volume' + '\n' + Units1,
                                          'Maximum' + '\n' + 'Percent' + '\n' + 'Full',
                                          'Day of' + '\n' + 'Maximum' + '\n' + 'Volume',
                                          'Hour of' + '\n' + 'Maximum' + '\n' + 'Volume',
                                          'Maximum' + '\n' + 'Outflow' + '\n' + Units2]
                    elif self.cboType.currentText() == 'Link Flow':
                        Units1 = header_list[2]
                        Units2 = header_list[5]
                        column_headers = ['Link',
                                          'Type',
                                          'Maximum' + '\n' + '|Flow|' + '\n' + Units1,
                                          'Day of' + '\n' + 'Maximum' + '\n' + 'Flow',
                                          'Hour of' + '\n' + 'Maximum' + '\n' + 'Flow',
                                          'Maximum' + '\n' + '|Velocity|' + '\n' + Units2,
                                          'Max /' + '\n' + 'Full' + '\n' + 'Flow',
                                          'Max /' + '\n' + 'Full' + '\n' + 'Depth']
                    elif self.cboType.currentText() == 'Flow Classification':
                        column_headers = ['Link',
                                          'Adjusted/' + '\n' + 'Actual' + '\n' + 'Length',
                                          'Fully' + '\n' + 'Dry',
                                          'Upstrm' + '\n' + 'Dry',
                                          'Dnstrm' + '\n' + 'Dry',
                                          'Sub' + '\n' + 'Critical',
                                          'Super' + '\n' + 'Critical',
                                          'Upstrm' + '\n' + 'Critical',
                                          'Dnstrm' + '\n' + 'Critical',
                                          'Normal' + '\n' + 'Flow' + '\n' + 'Limited',
                                          'Inlet' + '\n' + 'Control']
                    elif self.cboType.currentText() == 'Conduit Surcharge':
                        column_headers = ['Conduit',
                                          'Hours' + '\n' + 'Both Ends' + '\n' + 'Full',
                                          'Hours' + '\n' + 'Upstream' + '\n' + 'Full',
                                          'Hours' + '\n' + 'Dnstream' + '\n' + 'Full',
                                          'Hours' + '\n' + 'Above' + '\n' + 'Normal' + '\n' + 'Flow',
                                          'Hours' + '\n' + 'Capacity' + '\n' + 'Limited']
                    elif self.cboType.currentText() == 'Pumping':
                        Units1 = header_list[3]
                        Units2 = header_list[6] + ' ' + header_list[7]
                        Units3 = header_list[8]
                        column_headers = ['Pump',
                                          'Percent' + '\n' + 'Utilized',
                                          'Number of' + '\n' + 'Start-Ups',
                                          'Minimum' + '\n' + 'Flow' + '\n' + Units1,
                                          'Average' + '\n' + 'Flow' + '\n' + Units1,
                                          'Maximum' + '\n' + 'Flow' + '\n' + Units1,
                                          'Total' + '\n' + 'Volume' + '\n' + Units2,
                                          'Power' + '\n' + 'Usage' + '\n' + Units3,
                                          '% Time' + '\n' + 'Below' + '\n' + 'Pump' + '\n' + 'Curve',
                                          '% Time' + '\n' + 'Above' + '\n' + 'Pump' + '\n' + 'Curve']
                    else:
                        # more generically get from headers
                        header_list = headers[0].split()
                        total_num_headers = len(headers)
                        header_count = 1
                        for header_row in headers[1:]:
                            header_count += 1
                            temp_header_list = header_row.split()
                            num_column = len(header_list)
                            for i in range(0,num_column):
                                if header_count == total_num_headers:
                                    if temp_header_list[1] == 'Node':
                                        temp_header_list.remove('Node')
                                    if temp_header_list[i+1] == '10^6' and temp_header_list[i+2] == 'gal':
                                        temp_header_list[i+1] = '10^6 gal'
                                        temp_header_list[i+2] = temp_header_list[i+3]
                                        if len(temp_header_list) > i+4:
                                            temp_header_list[i+3] = temp_header_list[i+4]
                                    header_list[i] += '\n' + temp_header_list[i+1]
                                else:
                                    header_list[i] += '\n' + temp_header_list[i]
                        header_list.insert(0,temp_header_list[0])
                        column_headers = header_list

                    # now populate grid
                    self.tblSummary.setSortingEnabled(False)
                    self.tblSummary.setHorizontalHeaderLabels(column_headers)
                    row = -1
                    for line_list in real_rows:
                        col = -1
                        row += 1
                        for value in line_list[0:]:
                            col += 1
                            item = QtGui.QTableWidgetItem(value)
                            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
                            if col == 0:
                                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
                            else:
                                item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                            self.tblSummary.setItem(row,col,item)
                # self.tblSummary.setSortingEnabled(True)
            except Exception as e:
                print("Error reading " + self.status_file_name)

    def cmdCancel_Clicked(self):
        self.close()
