import os, inspect
import core.epanet.epanet_project
import core.epanet.inp_reader_project
import core.epanet.inp_writer_project

# This is a stand-alone module for internal testing of refactored code during the refactoring effort.
# This is not part of the unit and regression testing that is routinely run.

if __name__ == '__main__':
    directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

    # Get example path
    # All tests are under Examples or immediate level sub directories
    example_root_path = os.path.join(directory, "Examples")

    my_project = core.epanet.epanet_project.EpanetProject()
    project_reader = core.epanet.inp_reader_project.ProjectReader()
    project_reader.read_file(my_project, os.path.join(example_root_path, "Net1.inp"))
    project_writer = core.epanet.inp_writer_project.ProjectWriter()
    project_writer.write_file(my_project, my_project.file_name + ".written.txt")
