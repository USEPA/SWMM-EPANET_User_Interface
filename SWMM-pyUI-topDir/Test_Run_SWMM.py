import os, sys
import sip
for typ in ["QString","QVariant", "QDate", "QDateTime", "QTextStream", "QTime", "QUrl"]:
    sip.setapi(typ, 2)
from Externals.swmm.model.swmm5 import pyswmm
import Externals.swmm.outputapi.SMOutputSWIG as SMO
from core.project_base import ProjectBase
from core.swmm.swmm_project import SwmmProject as Project
from core.swmm.inp_reader_project import ProjectReader
from datetime import *

inp_file_name = 'C:\Data\SWMM\Example1.inp'
status_file_name = 'C:\Data\SWMM\Example1.rpt'
output_filename = 'C:\Data\SWMM\Example1.out'
model_path = '..\..\Externals\swmm\model\swmm5_x64.dll'
model_api = pyswmm(inp_file_name, status_file_name, output_filename, model_path)
_last_displayed_days = -1

project = Project()
project_reader = ProjectReader()
project_reader.read_file(project, inp_file_name)
if project_reader.input_err_msg:
    print('problem reading input file')

def compute_total_days(project):
    #  Compute the simulation duration in days from the Project's simulation options.
    try:
        end_date = datetime.strptime(project.options.dates.end_date + ' ' +
                                     project.options.dates.end_time, "%m/%d/%Y %H:%M:%S")
        start_date = datetime.strptime(project.options.dates.start_date + ' ' +
                                       project.options.dates.start_time, "%m/%d/%Y %H:%M:%S")
        return (end_date - start_date).days
    except:
        return 0.0


# self.add_map_constituents()
print("Running SWMM " + str(model_api.swmm_getVersion()))
model_api.swmm_run()
model_api.swmm_open()
model_api.swmm_start()
date_updated = datetime.now()
total_days = compute_total_days(project)
while model_api.errcode == 0:
    elapsed_days = model_api.swmm_step()
    if elapsed_days > 0:
        if total_days:
            date_now = datetime.now()
            if (date_now - date_updated).microseconds > 100000:
                # update_progress_days(elapsed_days, total_days)
                # update_progress_bar(round(elapsed_days), total_days)
                date_updated = date_now
    else:
        model_api.swmm_end()
        break

ErrRunoff, ErrFlow, ErrQual = model_api.swmm_getMassBalErr()

if model_api.Errflag:
    print("\n\nSWMM completed. There are errors.\n")
    # set_status(RunStatus.rsError)
elif model_api.Warnflag:
    print("\n\nSWMM completed. There are warnings.\n")
    # set_status(RunStatus.rsWarning)
else:
    print("\n\nSWMM completed.\n")
    # set_status(RunStatus.rsSuccess)

if os.path.isfile(output_filename):
    # model_api.swmm_end()
    # self.model_api.swmm_close()
    # self.model_api = None
    # QMessageBox.information(None, "SWMM", "pause", QMessageBox.Ok)
    try:
        output = SMO.SwmmOutputObject(output_filename)
        output.build_units_dictionary()
        print("output file is good")
    except Exception as ex:
        print("problem access output")
