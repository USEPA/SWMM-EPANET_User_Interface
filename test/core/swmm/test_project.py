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

    def runTest(self):
        directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

        # Get example path and file names
        example_path = os.path.join(directory, "Examples")
        example_files = os.listdir(example_path)

        # Get path to swmm5.exe, copy the exe file to /Examples
        source_root_path = os.path.split(os.path.split(os.path.split(directory)[0])[0])[0]
        exe_path = os.path.join(os.path.join(source_root_path, "src"),"Externals")
        exe_name = "swmm5.exe"
        exe_full_path = os.path.join(exe_path, exe_name)
        exe_to_example_path = os.path.join(example_path, exe_name)
        shutil.copy(exe_full_path, exe_to_example_path)

        # Loop through all .inp files in the Examples folder
        for filename in example_files:
            prefix, extension = os.path.splitext(filename)
            if extension.lower() == ".inp":
                # Read .inp file, count the number of sections
                my_file = os.path.join(example_path,filename)
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
                        raise "Error in executing exes"

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
                        raise "Error in executing exes"
                    os.rename(temp_file, new_filename)
                    # Return to current directory
                    os.chdir(current_directory)
                    # args = []
                    # if os.path.isfile(exe_path):
                    #     args.append(file_name)
                    #     args.append(prefix + '.rpt')
                    #     args.append(prefix + '.out')
                    #    # running the Exe
                    #    status = StatusMonitor0(exe_path, args, self, model='SWMM')
                    #    status.show()
                # for (old_section, new_section) in \
                #         zip(self.my_project.sections, self.new_project.sections):
                #    pass
            # Sequences are different, how do we test these? Think about it now.
            # How about run the SWMM and check the results ?
            pass

            # assert len(self.my_project.sections) == 43
            # with open(inp_filename + ".written.txt", 'w') as writer:
            #     writer.writelines(self.my_project.get_text())
            # with open(inp_filename + ".written_inp_spaces.inp", 'w') as writer:
            #     writer.writelines('\n'.join(self.my_project.get_text().split()))
            # with open(inp_filename + ".written_orig_spaces.inp", 'w') as writer:
            #     with open(inp_filename, 'r') as read_inp:
            #         writer.writelines('\n'.join(read_inp.read().split()))

            # with open(inp_filename, 'r') as read_inp:
            #     assert ' '.join(self.my_project.get_text().split()) == ' '.join(read_inp.read().split())
