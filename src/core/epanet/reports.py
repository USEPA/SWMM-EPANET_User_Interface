"""
    EPANET Report Generation
    Based on Ureport.pas from EPANET2W 2.0 9/7/00 Author: L. Rossman
    Converted to Python April 2016 by Mark Gray, RESPEC
"""

import sys
import traceback
from datetime import datetime
from core.epanet.project import Project
import Externals.epanet.outputapi.outputapi
from Externals.epanet.outputapi.ENOutputWrapper import *
import Externals.epanet.outputapi.functionalwrapper
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
        if isinstance(epanet_project, Project):
            self.project = epanet_project
        elif isinstance(epanet_project, str):
            self.project = Project()
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
                    pump.id, x[0],   x[1],   x[2],   x[3],   x[4],   x[5])
            self.write_line(line)

        self.write_line(self.ULINE)
        line = self.FMT74.format('', Dcharge)
        self.write_line(line)
        line = self.FMT75.format('', Csum + Dcharge)
        self.write_line(line)
        self.write_line('')

    def write_node_header(self, period, ContinueFlag):
        if self.LineNum + 11 > self.PAGESIZE:
            self.LineNum = self.PAGESIZE
        line = self.TXT_NODE_RESULTS
        if self.output.numPeriods > 1:
            line += self.TXT_AT + self.output.get_time_string(period)
        line += ':'
        if ContinueFlag:
            line += self.TXT_CONTINUED
        self.write_line(line)
        self.write_line(self.ULINE)
        line = '{:15} {:>10}{:>10}{:>10}{:>10}'.format(self.TXT_NODE,
                                                       ENR_node_type.AttributeDemand.name,
                                                       ENR_node_type.AttributeHead.name,
                                                       ENR_node_type.AttributePressure.name,
                                                       ENR_node_type.AttributeQuality.name)
        self.write_line(line)
        line = '{:15} {:>10}{:>10}{:>10}{:>10}'.format(self.TXT_ID,
                                                       ENR_node_type.AttributeDemand.units(self.output.unit_system),
                                                       ENR_node_type.AttributeHead.units(self.output.unit_system),
                                                       ENR_node_type.AttributePressure.units(self.output.unit_system),
                                                       ENR_node_type.AttributeQuality.units(self.output.unit_system))
        self.write_line(line)
        self.write_line(self.ULINE)

    def write_link_header(self, period, ContinueFlag):
        if self.LineNum + 11 > self.PAGESIZE:
            self.LineNum = self.PAGESIZE
        S = self.TXT_LINK_RESULTS
        if self.output.numPeriods > 1:
            S += self.TXT_AT + self.output.get_time_string(period)
        S += ':'
        if ContinueFlag:
            S += self.TXT_CONTINUED
        self.write_line(S)
        self.write_line(self.ULINE)
        S = '{:15} {:10}{:10}{:10}{:10}'.format(self.TXT_LINK,
                                                ENR_link_type.AttributeFlow.name,
                                                ENR_link_type.AttributeVelocity.name,
                                                ENR_link_type.AttributeHeadloss.name,
                                                ENR_link_type.AttributeStatus.name)
        self.write_line(S)
        S = '{:15} {:10}{:10}{:10}'.format(self.TXT_ID,
                                           ENR_link_type.AttributeFlow.units(self.output.unit_system),
                                           ENR_link_type.AttributeVelocity.units(self.output.unit_system),
                                           ENR_link_type.AttributeHeadloss.units(self.output.unit_system))
        self.write_line(S)
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
                # length = self.output.get_LinkValue(conduits.id, 0, 1) # Uoutput.GetLinkValStr(LINKLENGTH,0,I,J)
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
                S = '{:15}{:15}{:15}{:>10}{:>10}'.format(conduit.id, conduit.inlet_node, conduit.outlet_node,
                                                         length, diameter)
                if conduits is self.project.pumps:
                    S += ' Pump'
                elif conduits is self.project.valves:
                    S += ' Valve'
                self.write_line(S)
        self.write_line('')

    def write_node_table(self, period):
        self.write_node_header(period, False)
        for nodes in (self.project.junctions, self.project.reservoirs, self.project.tanks):
            for input_node in nodes.value:
                #         MainForm.UpdateProgressBar(Nprogress, ProgStep)
                output_node = self.output.get_itemById(self.output.nodes, input_node.id)
                if not output_node:
                    line = '{:15} {}'.format(input_node.id, 'not found in output.')
                else:
                    demand     = output_node.get_value(self.output, ENR_node_type.AttributeDemand, period)
                    head       = output_node.get_value(self.output, ENR_node_type.AttributeHead, period)
                    pressure   = output_node.get_value(self.output, ENR_node_type.AttributePressure, period)
                    quality    = output_node.get_value(self.output, ENR_node_type.AttributeQuality, period)
                    line = '{:15} {:7.2f} {:7.2f} {:7.2f} {:7.2f}'.format(output_node.id, demand, head, pressure, quality)
                if nodes is self.project.reservoirs:
                    line += ' Reservoir'
                elif nodes is self.project.tanks:
                    line += ' Tank'
                if (self.LineNum >= self.PAGESIZE):
                    self.write_node_header(period, True)
                self.write_line(line)
        self.write_line('')

    def write_link_table(self, period):
        self.write_link_header(period, False)
        for links in (self.project.pipes, self.project.pumps, self.project.valves):
            for input_link in links.value:
                # MainForm.UpdateProgressBar(Nprogress, ProgStep)
                output_link = self.output.get_itemById(self.output.links, input_link.id)
                if not output_link:
                    line = '{:15} {}'.format(input_link.id, 'not found in output.')
                else:
                    flow     = output_link.get_value(self.output, ENR_link_type.AttributeFlow, period)
                    velocity = output_link.get_value(self.output, ENR_link_type.AttributeVelocity, period)
                    headloss = output_link.get_value(self.output, ENR_link_type.AttributeHeadloss, period)
                    linkstat = output_link.get_value_formatted(self.output, ENR_link_type.AttributeStatus, period)
                    line = '{:15} {:9.2f} {:9.2f} {:9.2f} {:>10}'.format(input_link.id, flow, velocity, headloss, linkstat)
                if links is self.project.pumps:
                    line += ' Pump'
                elif links is self.project.valves:
                    line += ' Valve'

                if (self.LineNum >= self.PAGESIZE):
                    self.write_link_header(period, True)
                self.write_line(line)
        self.write_line('')

    def write_results(self):
        for period in range(0, self.output.numPeriods):
            # Application.ProcessMessages
            self.write_node_table(period)
            # Application.ProcessMessages
            self.write_link_table(period)

    def write_report(self, report_file_name):
        #   MainForm.ShowProgressBar('Writing full report...')
        with open(report_file_name, 'w') as self.F:
            try:
                # Total = self.output.nodeCount + self.output.linkCount
                # Total *= self.output.numPeriods
                # Total += self.output.linkCount
                # with MainForm.ProgressBar do
                #   N = Max div Step
                # ProgStep = Round(Total/N)
                # Nprogress = 0
                self.write_logo()
                #     Application.ProcessMessages
                self.write_link_info()
                if self.output.pumpCount > 0:
                    self.write_energy()
                self.write_results()
                return True
            finally:
                print "Finished writing report " + report_file_name
                #   MainForm.HideProgressBar

    def all_links_set_category(self):
        items = []
        for input_links, category in [(self.project.pipes.value, "Pipe"),
                                       (self.project.pumps.value, "Pump"),
                                       (self.project.valves.value, "Valve")]:
            for link in input_links:
                item = self.output.get_itemById(self.output.links, link.id)
                if item:
                    item.category = category
                    items.append(item)
                else:
                    print("Skipping link " + link.id + " because it was not found in output")
        return items

    def all_nodes_set_category(self):
        items = []
        for input_nodes, category in [(self.project.junctions.value, "Junction"),
                                       (self.project.reservoirs.value, "Reservoir"),
                                       (self.project.tanks.value, "Tank")]:
            for node in input_nodes:
                item = self.output.get_itemById(self.output.nodes, node.id)
                if item:
                    item.category = category
                    items.append(item)
                else:
                    print("Skipping node " + node.id + " because it was not found in output")
        return items

    def node_distances(self, node_ids):
        return range(0, len(node_ids))
        # TODO: compute distance from node coordinates
        distances = [0]
        x = None
        y = None
        for node_id in node_ids:
            for nodes in (self.project.junctions, self.project.reservoirs, self.project.tanks):
                for node in nodes.value:
                    if node.id == node_id:
                        if x and y:
                            distances.append(sqrt((x - node.x) ^ 2 + (y - node.y) ^ 2))
                        else:  # default: return distances = 0, 1, 2, ...
                            distances.append(len(distances))
        return distances
