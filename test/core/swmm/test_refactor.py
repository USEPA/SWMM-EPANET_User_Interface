import os, inspect
import core.swmm.project
import core.swmm.inp_reader_project

# This is a stand-alone module for internal testing of refactored code during the refactoring effort.
# This is not part of the unit and regression testing that is routinely run.

if __name__ == '__main__':
    directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

    # Get example path
    # All tests are under Examples or immediate level sub directories
    example_root_path = os.path.join(directory, "Examples")

    my_project = core.swmm.project.Project()
    project_reader = core.swmm.inp_reader_project.ProjectReader()
    project_reader.read_file(my_project, os.path.join(example_root_path, "Example1.inp"))
    number_of_sections = len(my_project.sections)
    print(str(number_of_sections))