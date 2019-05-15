"""
    EPANET Report Generation
    Based on Ureport.pas from EPANET2W 2.0 9/7/00 Author: L. Rossman
    Converted to Python April 2016 by Mark Gray, RESPEC
"""

import sys
import traceback
from core.epanet.epanet_project import EpanetProject
from Externals.epanet.outputapi.ENOutputWrapper import *
from datetime import datetime
# See Also: from core.epanet.options.report import ReportOptions


class Reports:
    PAGESIZE = 55
    ULINE = '----------------------------------------------------------------------'
    FMT18 = '  Page 1                                          {:>22}'
    FMT_DATE = '%Y/%m/%d %I:%M%p'
    FMT82 = '  Page {:4d} {:60}'
    FMT71 = 'Energy Usage:'
    FMT72 = '                  Usage   Avg.     Kw-hr      Avg.      Peak      Cost'
    FMT73 = 'Pump             Factor Effic.     {:5}        Kw        Kw      /day'
    FMT74 = '{:45} Demand Charge: {:9.2f}'
    FMT75 = '{:45} Total Cost:    {:9.2f}'
    TXT_perM3 = '/m3'
    TXT_perMGAL = '/Mgal'
    TXT_CONTINUED = ' (continued)'
    TXT_INPUT_FILE = 'Input File: '
    TXT_LINK_INFO = 'Link - Node Table:'
    TXT_NODE_RESULTS = 'Node Results'
    TXT_LINK_RESULTS = 'Link Results'
    TXT_AT = ' at '
    TXT_ID = 'ID'
    TXT_NODE = 'Node'
    TXT_LINK = 'Link'
    TXT_START = 'Start'
    TXT_END = 'End'

    TimeStat = ['Single Period', 'Average', 'Minimum', 'Maximum', 'Range']

    def __init__(self, epanet_project, model_output):
        self.LogoTxt = (
            '**********************************************************************',
            '*                             E P A N E T                            *',
            '*                     Hydraulic and Water Quality                    *',
            '*                     Analysis for Pipe Networks                     *',
            '*                           Version 2.0                              *',
            '**********************************************************************')
        self.F = None  # File being written to
        if isinstance(epanet_project, EpanetProject):
            self.project = epanet_project
        elif isinstance(epanet_project, str):
            self.project = EpanetProject()
            self.project.read_file(epanet_project)
        else:
            raise Exception("Report Initialization: could not read EPANET project.")

        if isinstance(model_output, OutputObject):
            self.output = model_output
        elif isinstance(model_output, str):
            self.output = OutputObject(model_output)
        else:
            raise Exception("Report Initialization: could not read output of model.\n"
                            "Run the model to generate new output.")

        self.RptTitle = self.project.title.title
        self.PageNum = 0
        self.LineNum = 0
        self.Progstep = 0
        self.Nprogress = 0

    def write_line(self, line):
        if (self.LineNum >= self.PAGESIZE):
            self.PageNum += 1
            self.F.write('\n\f\n')  # newline form-feed newline
            self.F.write(self.FMT82.format(self.PageNum, self.RptTitle) + '\n')
            self.LineNum = 3
        self.F.write('  ' + line + '\n')
        self.LineNum += 1

    def write_logo(self):
        self.PageNum = 1
        self.LineNum = 1
        self.write_line(self.FMT18.format(datetime.now().strftime(self.FMT_DATE)))
        for line in self.LogoTxt:
            self.write_line(line)
        self.write_line('')
        self.write_line(self.TXT_INPUT_FILE + self.project.file_name)
        self.write_line('')
        self.write_line(self.RptTitle)
        self.write_line(self.project.title.notes)
        # self.write_line('')

    def write_energy_header(self, ContinueFlag):
        if self.LineNum + 11 > self.PAGESIZE:
            self.LineNum = self.PAGESIZE
        units = (self.TXT_perMGAL, self.TXT_perM3)[self.output.unit_system]
        line = self.FMT71
        if ContinueFlag:
            line += self.TXT_CONTINUED
        self.write_line(line)
        self.write_line(self.ULINE)
        line = self.FMT72
        self.write_line(line)
        line = self.FMT73.format(units)
        self.write_line(line)
        self.write_line(self.ULINE)

    def write_energy(self):
        self.write_energy_header(False)
        Csum = 0.0
        Dcharge = 0
        for pump in self.project.pumps.value:
            x = [0,0,0,0,0,0]
            Dcharge = 0
            # Uoutput.GetPumpEnergy(k,x,Dcharge)
            Csum += x[5]
            if (self.LineNum >= self.PAGESIZE):
                self.write_energy_header(True)
            line = '{:15}  {:6.2f} {:6.2f} {:9.2f} {:9.2f} {:9.2f} {:9.2f}'.format(
                    pump.name, x[0],   x[1],   x[2],   x[3],   x[4],   x[5])
            self.write_line(line)

        self.write_line(self.ULINE)
        line = self.FMT74.format('', Dcharge)
        self.write_line(line)
        line = self.FMT75.format('', Csum + Dcharge)
        self.write_line(line)
        self.write_line('')

    def write_node_header(self, period, table_attributes, ContinueFlag):
        if self.LineNum + 11 > self.PAGESIZE:
            self.LineNum = self.PAGESIZE
        line = self.TXT_NODE_RESULTS
        if self.output.num_periods > 1:
            line += self.TXT_AT + self.output.get_time_string(period)
        line += ':'
        if ContinueFlag:
            line += self.TXT_CONTINUED
        self.write_line(line)
        self.write_line(self.ULINE)

        names = '{:15} '.format(self.TXT_NODE)
        units = '{:15} '.format(self.TXT_ID)
        for attribute_type in table_attributes:
            names += '{:>10}'.format(attribute_type.name)
            units += '{:>10}'.format(attribute_type.units(self.output.unit_system))
        self.write_line(names)
        self.write_line(units)
        self.write_line(self.ULINE)

    def write_link_header(self, period, table_attributes, ContinueFlag):
        if self.LineNum + 11 > self.PAGESIZE:
            self.LineNum = self.PAGESIZE
        line = self.TXT_LINK_RESULTS
        if self.output.num_periods > 1:
            line += self.TXT_AT + self.output.get_time_string(period)
        line += ':'
        if ContinueFlag:
            line += self.TXT_CONTINUED
        self.write_line(line)
        self.write_line(self.ULINE)
        names = '{:15} '.format(self.TXT_LINK)
        units = '{:15} '.format(self.TXT_ID)
        for attribute_type in table_attributes:
            names += '{:10}'.format(attribute_type.name)
            units += '{:10}'.format(attribute_type.units(self.output.unit_system))
        self.write_line(names)
        self.write_line(units)
        self.write_line(self.ULINE)

    def write_link_info_header(self, ContinueFlag):
        S = self.TXT_LINK_INFO
        if ContinueFlag:
            S += self.TXT_CONTINUED
        self.write_line(S)
        self.write_line(self.ULINE)
        S = '{:15}{:15}{:15}{:10}{:10}'.format(self.TXT_LINK, self.TXT_START, self.TXT_END, "Length", "Diameter")
        self.write_line(S)

        len_units = ('ft','m')[self.output.unit_system]
        dia_units = ('in','mm')[self.output.unit_system]
        S = '{:15}{:15}{:15}{:>10}{:>10}'.format(self.TXT_ID, self.TXT_NODE, self.TXT_NODE, len_units, dia_units)
        self.write_line(S)
        self.write_line(self.ULINE)

    def write_link_info(self):
        self.write_link_info_header(False)
        for conduits in (self.project.pipes, self.project.pumps, self.project.valves):
            # TODO: update progress bar: MainForm.UpdateProgressBar(Nprogress, ProgStep)
            for conduit in conduits.value:
                # Note: Pascal report got these values from binary, we get them here from input
                # length = self.output.get_LinkValue(conduits.name, 0, 1) # Uoutput.GetLinkValStr(LINKLENGTH,0,I,J)
                if (self.LineNum >= self.PAGESIZE):
                    self.write_link_info_header(True)
                if hasattr(conduit, "length"):
                    length = conduit.length
                else:
                    length = "#N/A"
                if hasattr(conduit, "diameter"):
                    diameter = conduit.diameter
                else:
                    diameter = "#N/A"
                S = '{:15}{:15}{:15}{:>10}{:>10}'.format(conduit.name, conduit.inlet_node, conduit.outlet_node,
                                                         length, diameter)
                if conduits is self.project.pumps:
                    S += ' Pump'
                elif conduits is self.project.valves:
                    S += ' Valve'
                self.write_line(S)
        self.write_line('')

    def write_node_table(self, period):
        table_attributes = (ENR_node_type.AttributeDemand,
                            ENR_node_type.AttributeHead,
                            ENR_node_type.AttributePressure,
                            ENR_node_type.AttributeQuality)
        self.write_node_header(period, table_attributes, False)
        for nodes in (self.project.junctions, self.project.reservoirs, self.project.tanks):
            for input_node in nodes.value:
                #         MainForm.UpdateProgressBar(Nprogress, ProgStep)
                output_node = self.output.nodes[input_node.name]
                if not output_node:
                    line = '{:15} {}'.format(input_node.name, 'not found in output.')
                else:
                    values = output_node.get_all_attributes_at_time(self.output, period)
                    values_formatted = []
                    for attribute_type in table_attributes:
                        values_formatted.append(attribute_type.str(values[attribute_type.index]))
                    line = '{:15} {}'.format(output_node.name, ' '.join(values_formatted))
                if nodes is self.project.reservoirs:
                    line += ' Reservoir'
                elif nodes is self.project.tanks:
                    line += ' Tank'
                if (self.LineNum >= self.PAGESIZE):
                    self.write_node_header(period, table_attributes, True)
                self.write_line(line)
        self.write_line('')

    def write_link_table(self, period):
        table_attributes = (ENR_link_type.AttributeFlow,
                            ENR_link_type.AttributeVelocity,
                            ENR_link_type.AttributeHeadloss,
                            ENR_link_type.AttributeStatus)
        self.write_link_header(period, table_attributes, False)
        for links in (self.project.pipes, self.project.pumps, self.project.valves):
            for input_link in links.value:
                # MainForm.UpdateProgressBar(Nprogress, ProgStep)
                output_link = self.output.links[input_link.name]
                if not output_link:
                    line = '{:15} {}'.format(input_link.name, 'not found in output.')
                else:
                    values = output_link.get_all_attributes_at_time(self.output, period)
                    values_formatted = []
                    for attribute in table_attributes:
                        if attribute == ENR_link_type.AttributeStatus:  # use default formatting of link status
                            values_formatted.append(attribute.str(values[attribute.index]))
                        else:                                           # custom formatting of numeric attributes
                            values_formatted.append('{:9.2f}'.format(values[attribute.index]))
                    line = '{:15} {}'.format(input_link.name, ' '.join(values_formatted))
                if links is self.project.pumps:
                    line += ' Pump'
                elif links is self.project.valves:
                    line += ' Valve'

                if (self.LineNum >= self.PAGESIZE):
                    self.write_link_header(period, table_attributes, True)
                self.write_line(line)
        self.write_line('')

    def write_results(self):
        for period in range(0, self.output.num_periods):
            # Application.ProcessMessages
            self.write_node_table(period)
            # Application.ProcessMessages
            self.write_link_table(period)

    def write_report(self, report_file_name):
        #   MainForm.ShowProgressBar('Writing full report...')
        with open(report_file_name, 'w') as self.F:
            try:
                # Total = self.output.nodeCount + self.output.linkCount
                # Total *= self.output.num_periods
                # Total += self.output.linkCount
                # with MainForm.ProgressBar do
                #   N = Max div Step
                # ProgStep = Round(Total/N)
                # Nprogress = 0
                self.write_logo()
                #     Application.ProcessMessages
                self.write_link_info()
                if self.project.pumps:
                    if len(self.project.pumps.value) > 0:
                        self.write_energy()
                self.write_results()
                return True
            finally:
                print ("Finished writing report " + report_file_name + "\n")
                #   MainForm.HideProgressBar

    def all_links_set_category(self):
        items = []
        for input_links, category in [(self.project.pipes.value, "Pipe"),
                                       (self.project.pumps.value, "Pump"),
                                       (self.project.valves.value, "Valve")]:
            for link in input_links:
                item = self.output.links[link.name]
                if item:
                    item.category = category
                    items.append(item)
                else:
                    print("Skipping link " + link.name + " because it was not found in output")
        return items

    def all_nodes_set_category(self):
        items = []
        for input_nodes, category in [(self.project.junctions.value, "Junction"),
                                       (self.project.reservoirs.value, "Reservoir"),
                                       (self.project.tanks.value, "Tank")]:
            for node in input_nodes:
                item = self.output.nodes[node.name]
                if item:
                    item.category = category
                    items.append(item)
                else:
                    print("Skipping node " + node.name + " because it was not found in output")
        return items

    def node_distances(self, node_names):
        return range(0, len(node_names))
        # TODO: compute distance from node coordinates
        distances = [0]
        x = None
        y = None
        for node_name in node_names:
            for nodes in (self.project.junctions, self.project.reservoirs, self.project.tanks):
                for node in nodes.value:
                    if node.name == node_name:
                        if x and y:
                            distances.append(sqrt((x - node.x) ^ 2 + (y - node.y) ^ 2))
                        else:  # default: return distances = 0, 1, 2, ...
                            distances.append(len(distances))
        return distances
