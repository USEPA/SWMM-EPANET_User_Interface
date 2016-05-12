import os
import core.swmm.project
import unittest
import inspect
import shutil
# from ui.swmm.frmRunSWMM import frmRunSWMM
# from ui.model_utility import StatusMonitor0


class ProjectTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_project = core.swmm.project.Project()
        self.new_project = core.swmm.project.Project()

    @staticmethod
    def get_immediate_subdirectories(a_dir):
        return [name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))]

    def runTest(self):
        directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

        # Get path to swmm5.exe
        source_root_path = os.path.split(os.path.split(os.path.split(directory)[0])[0])[0]
        exe_path = os.path.join(os.path.join(source_root_path, "src"), "Externals")
        exe_name = "swmm5.exe"
        exe_full_path = os.path.join(exe_path, exe_name)

        # Get example path and the paths to its first level sub directories
        # Assuming all tests are under Examples or immediate level sub directories
        example_path = os.path.join(directory, "Examples")
        example_paths = []
        example_paths.append(example_path)
        example_sub_directories = ProjectTest.get_immediate_subdirectories(example_path)
        if example_sub_directories:
            for subdir in example_sub_directories:
                example_paths.append(os.path.join(example_path, subdir))

        # Loop through all .inp files in /Examples and first-level sub directories
        for example_path in example_paths:

            # Get all file names
            example_files = os.listdir(example_path)

            # Test all examples in the /Examples folder
            # Copy the exe file to /Examples or sub directory
            exe_to_example_path = os.path.join(example_path, exe_name)
            shutil.copy(exe_full_path, exe_to_example_path)

            # Loop through all .inp files in the /Examples folder
            for filename in example_files:
                prefix, extension = os.path.splitext(filename)
                if extension.lower() == ".inp":

                    # Read .inp file, count the number of sections
                    my_file = os.path.join(example_path, filename)
                    self.my_project.read_file(my_file)
                    number_of_sections = len(self.my_project.sections)

                    # Write my_project to new file .inptest
                    new_filename = filename + "_copy"
                    new_file = os.path.join(example_path, new_filename)
                    self.my_project.write_file(new_file)

                    # Read .inptest into new_project, count the number of sections, assert
                    self.new_project.read_file(new_file)
                    new_number_of_sections = len(self.new_project.sections)
                    assert number_of_sections == new_number_of_sections

                    # If the numbers of sections agree, run swmm5.exe using:
                    # swmm5.exe XXXXX1.inp XXXXXX1.rpt XXXXXX1.out
                    # Have trouble with path, copied swmm5.exe into the Examples folder
                    if number_of_sections == new_number_of_sections:

                        # Get current_directory for restoring it later
                        current_directory = os.getcwd()
                        os.chdir(example_path)
                        # Run my_file
                        inp_file = filename
                        rpt_file = prefix + '.rpt'
                        out_file = prefix + '.out'
                        command_line = exe_name + " " + inp_file + " " + rpt_file + " "+out_file
                        try:
                            os.system(command_line)
                        except:
                            raise "Error in executing{}".format(command_line)

                        #Run new_file
                        temp_file = "renameit.inp"
                        os.rename(new_filename, temp_file)
                        inp_file = temp_file
                        rpt_file = prefix + '_copy'+ '.rpt'
                        out_file = prefix + '_copy'+ '.out'
                        command_line = exe_name + " " + inp_file + " " + rpt_file + " "+out_file
                        try:
                            os.system(command_line)
                        except:
                            raise "Error in executing{}".format(command_line)

                        # Rename file to .inp_test because .inp only for originals
                        os.rename(temp_file, new_filename)

                        # Return to current directory
                        os.chdir(current_directory)

