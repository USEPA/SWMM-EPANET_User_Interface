import os
import core.swmm.project
import unittest
import inspect
import shutil
import filecmp
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

    @staticmethod
    def readline_nowhite(f):
        """ Readline_nowhite
         Strip all carriage returns, tabs and spaces
         If it is empty line, read the next line
         Return the lines read, and the line without white
        """
        f_line = f.readline()
        line_no = 1
        f_line_nw = f_line.replace('\n', '').replace('\t', '').replace(' ', '')

        while f_line_nw == '' and f_line != '':
            f_line = f.readline()
            line_no += 1
            f_line_nw = f_line.replace('\n', '').replace('\t', '').replace(' ', '')
        f_line = f_line_nw
        return line_no, f_line

    @staticmethod
    def compare_two_files(fname1, fname2, exempted_strings):
        """Reference: http://www.opentechguides.com/how-to/article/python/58/python-file-comparison.html
        Modified by xw 2016/05/12
        Strip all white spaces, empty lines and exempt the lines with exempted_strings
        Return a list of messages diff_msg. If identical, return empty list
        """

        diff_msg = ''
        # Open file for reading in text mode (default mode)
        f1 = open(fname1)
        f2 = open(fname2)

        # Initialize counter for line number
        line_no_f1 = 0
        line_no_f2 = 0

        # Readline_nowhite
        # Strip all carriage returns, tabs and spaces
        # If it is empty line, read the next line
        # File 1:
        line_read, f1_line = ProjectTest.readline_nowhite(f1)
        line_no_f1 = line_no_f1 + line_read

        # File 2:
        line_read, f2_line = ProjectTest.readline_nowhite(f2)
        line_no_f2 = line_no_f2 + line_read

        # Loop if either file1 or file2 has not reached EOF
        while f1_line != '' or f2_line != '':

            # Compare the lines from both file
            if f1_line != f2_line:

                is_diff = True
                # Loop through lines with keyword(s) indicating an exemption
                for exempted_string in exempted_strings:
                    str_nw = exempted_string.replace(' ','')
                    if f1_line.find(str_nw) != -1 \
                            and f2_line.find(str_nw) != -1:
                        is_diff = False
                        # Break when the exempted_string hit
                        break

                if is_diff:
                    diff_msg = fname1+'\n'\
                               +'>Line-'+str(line_no_f1)+':'+f1_line+'\n'\
                               +'<Line-'+str(line_no_f2)+':'+f2_line+'\n'
                    # Break on the first difference
                    break

            # File 1:
            line_read, f1_line = ProjectTest.readline_nowhite(f1)
            line_no_f1 = line_no_f1 + line_read

            # File 2:
            line_read, f2_line = ProjectTest.readline_nowhite(f2)
            line_no_f2 = line_no_f2 + line_read

        # Close the files
        f1.close()
        f2.close()
        return diff_msg

    def runTest(self):
        directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))

        # Get path to swmm5.exe
        source_root_path = os.path.split(os.path.split(os.path.split(directory)[0])[0])[0]
        exe_path = os.path.join(os.path.join(source_root_path, "src"), "Externals")
        exe_name = "swmm5.exe"
        exe_full_path = os.path.join(exe_path, exe_name)

        # Get example path and the paths to its first level sub directories
        # Assuming all tests are under Examples or immediate level sub directories
        example_root_path = os.path.join(directory, "Examples")
        example_paths = []
        example_paths.append(example_root_path)
        example_sub_directories = ProjectTest.get_immediate_subdirectories(example_root_path)
        if example_sub_directories:
            for subdir in example_sub_directories:
                example_paths.append(os.path.join(example_root_path, subdir))

        # Loop through all .inp files in /Examples and first-level sub directories
        # Record results in diff_summaries.txt under /Examples
        # Need to use assert -- Thinking
        diff_file = os.path.join(example_root_path, "diff_summaries.txt")
        with open(diff_file, "w") as text_file:
            text_file.write('Loop through all .inp files: \n')
            for example_path in example_paths:

                text_file.write(example_path+'\n')
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
                            current_directory = os.getcwd() #current test/core/
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

                            # Run new_file (copy of original .inp)
                            # Must rename the .inp_copy to renameit.inp
                            # swmm5.exe requires .inp as input files
                            # but the duplicates should not be named as .inp
                            # They will be renamed to .inp_copy after the run
                            temp_file = "renameit.inp"
                            try:
                                os.remove(temp_file)
                            except OSError:
                                pass
                            os.rename(new_filename, temp_file)
                            inp_file = temp_file
                            rpt_file = prefix + '_copy'+ '.rpt'
                            out_file = prefix + '_copy'+ '.out'
                            command_line = exe_name + " " + inp_file + " " + rpt_file + " "+out_file
                            try:
                                os.system(command_line)
                            except:
                                raise "Error in executing{}".format(command_line)

                            # Compare two out files
                            original_ = os.path.join(example_path, prefix + '.out')
                            copy_ = os.path.join(example_path, prefix + '_copy'+ '.out')
                            if os.path.isfile(original_) and os.path.isfile(copy_):
                                same_ = filecmp.cmp(original_,copy_)
                                if not same_:
                                    text_file.write(prefix+'.out binary differ\n')
                                else:
                                    text_file.write(prefix + '.out binary same\n')
                            else:
                                #.out may not be produced if model fails
                                text_file.write(prefix + '.out does not exist\n')

                            # Compare two rpt files
                            exempted_strings = ["Analysis begun on", "Analysis ended on",
                                                "Total elapsed time", "ERROR"]
                            original_ = os.path.join(example_path, prefix + '.rpt')
                            copy_ = os.path.join(example_path, prefix + '_copy'+ '.rpt')
                            if os.path.isfile(original_) and os.path.isfile(copy_):
                                diff_msg = ProjectTest.compare_two_files(original_, copy_, exempted_strings)
                                if diff_msg:
                                    text_file.write(prefix + '.rpt:'+'\n')
                                    text_file.write(diff_msg + '\n')
                                else:
                                    text_file.write(prefix + '.rpt same text none white' + '\n')
                            else:
                                text_file.write(prefix + '.rpt does not exist' + '\n')

                            # Rename file to .inp_test because use .inp only for originals
                            os.rename(temp_file, new_filename)

                            # Return to current directory
                            os.chdir(current_directory)

