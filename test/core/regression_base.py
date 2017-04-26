import os
import inspect
import webbrowser
from section_match import get_immediate_subdirectories, compare_two_analysis_blocks


class RegressTestBase(object):
    def __init__(self):
        self.my_project = None
        self.new_project = None
        self.reader = None
        self.writer = None
        self.model_type = None # "EPANET" or "SWMM"
        self.test_meta = {"EPANET": ["epanet","epanet2d.exe", "Test_Example_Summaries_EPANET.html"],
                          "SWMM": ["swmm", "swmm5.exe", 'Test_Example_Summaries_SWMM.html']}

    def runTest(self):
        # Get path to epanet2d.exe
        current_directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))
        directory = os.path.join(current_directory, self.test_meta[self.model_type][0])
        source_root_path = os.path.split(os.path.split(os.path.split(directory)[0])[0])[0]
        exe_path = os.path.join(source_root_path, "src", "Externals", self.test_meta[self.model_type][0], "model")
        exe_name = self.test_meta[self.model_type][1]
        exe_full_path = os.path.join(exe_path, exe_name)

        # Get example path and the paths to its first level sub directories
        # Assuming all tests are under Examples or immediate level sub directories
        example_root_path = os.path.join(directory, "Examples")
        example_paths = []
        example_paths.append(example_root_path)
        example_sub_directories = get_immediate_subdirectories(example_root_path)
        if example_sub_directories:
            for subdir in example_sub_directories:
                example_paths.append(os.path.join(example_root_path, subdir))

        # Loop through all .inp files in /Examples and first-level sub directories
        # Record results in diff_summaries.txt under /Examples
        # Need to use assert -- Thinking
        # diff_file = os.path.join(example_root_path, "diff_summaries.txt")
        examples = [] # example name
        status = []   # example test status 'Pass' or 'Fail'
        remarks = []  # error message goes here
        html_file = os.path.join(directory, self.test_meta[self.model_type][2])

        # Open html file
        text_file = open(html_file, "w")
        text_file.write('<header><h1>'+'EXAMPLES TEST REPORT:'+'</h1></header>')

        # Test all examples in /Examples or first level sub directory of /Examples
        for example_path in example_paths:

            # Get current_directory for restoring it later
            current_directory = os.getcwd()  # current test/core/

            # Get example directory
            os.chdir(example_path)

            # Get all file names under this example directory
            example_files = os.listdir(example_path)

            # Copy the exe file to each example directory
            # exe_to_example_path = os.path.join(example_path, exe_name)
            # shutil.copy(exe_full_path, exe_to_example_path)

            # Loop through all .inp files in the /Examples folder
            for filename in example_files:
                prefix, extension = os.path.splitext(filename)
                if extension.lower() == ".inp":

                    # Read .inp file, count the number of sections
                    my_file = os.path.join(example_path, filename)
                    self.reader().read_file(self.my_project,my_file)
                    number_of_sections = len(self.my_project.sections)

                    # Write my_project to new file .inptest
                    new_filename = filename + "_copy"
                    new_file = os.path.join(example_path, new_filename)
                    self.writer().write_file(self.my_project, new_file)

                    # Read .inptest into new_project, count the number of sections, assert
                    self.reader().read_file(self.new_project, new_file)
                    new_number_of_sections = len(self.new_project.sections)
                    assert number_of_sections == new_number_of_sections

                    # If the numbers of sections agree, run epanet2d.exe using:
                    # epanet2d.exe XXXXX1.inp XXXXXX1.rpt XXXXXX1.out
                    # Have trouble with path, copied epanet2d.exe into the Examples folder
                    if number_of_sections == new_number_of_sections:

                        # Run my_file
                        inp_file = filename
                        rpt_file = prefix + '.rpt'
                        out_file = prefix + '.out'
                        command_line = '"' + exe_full_path + '" ' + inp_file + ' ' + rpt_file + ' ' + out_file
                        try:
                            os.system(command_line)
                        except:
                            msg = "Error in executing{}".format(command_line)
                            examples.append(my_file)
                            status.append('----')
                            remarks.append(msg)
                            pass

                        # Run new_file (copy of original .inp)
                        # Must rename the .inp_copy to renameit.inp
                        # epanet2d.exe requires .inp as input files
                        # but the duplicates should not be named as .inp
                        # They will be renamed to .inp_copy after the run
                        # Note that epanet factors the input file name and
                        # some minor differences in the .out file
                        # Binary comparison is not really valid

                        temp_file = "renameit.inp"
                        try:
                            os.remove(temp_file)
                        except OSError:
                            pass
                        os.rename(new_filename, temp_file)
                        inp_file = temp_file
                        rpt_file = prefix + '_copy'+ '.rpt'
                        out_file = prefix + '_copy'+ '.out'
                        command_line = '"' + exe_full_path + '" ' + inp_file + ' ' + rpt_file + ' ' + out_file
                        try:
                            os.system(command_line)
                        except:
                            msg = "Error in executing{}".format(command_line)
                            examples.append(new_file)
                            status.append('----')
                            remarks.append(msg)
                            pass

                        # Compare two rpt files
                        exempted_strings = ["Analysis begun", "Analysis ended",
                                            "Total elapsed time", "ERROR",
                                            "Input Data File", "Page 1"]
                        original_ = os.path.join(example_path, prefix + '.rpt')
                        copy_ = os.path.join(example_path, prefix + '_copy'+ '.rpt')
                        if os.path.isfile(original_) and os.path.isfile(copy_):
                            # diff_msg = ProjectTest.compare_two_files(original_, copy_, exempted_strings)
                            diff_msg = compare_two_analysis_blocks(original_, copy_, exempted_strings)
                            if diff_msg:
                                msg = prefix + '.rpt:'\
                                      +'results of modified differ from results of original'+'\n'\
                                      + diff_msg + '\n'
                                examples.append(original_)
                                status.append('Fail')
                                remarks.append(msg)
                            else:
                                msg = prefix + '.rpt successful matching' + '\n'
                                examples.append(original_)
                                status.append('Pass')
                                remarks.append(msg)

                        # If the original does not produce .out '----'
                        elif not os.path.isfile(original_):
                            msg = prefix + '.rpt does not exist, ' \
                                           'original input did not run\n'
                            examples.append(original_)
                            status.append('----')
                            remarks.append(msg)

                        # If the original does but the copy does not produce .out 'Fail'
                        else:
                            msg = prefix + '_copy.rpt does not exist,' \
                                           'original ran but modified did not\n'
                            examples.append(original_)
                            status.append('Fail')
                            remarks.append(msg)

                        # Rename file to .inp_test because use .inp only for originals
                        os.rename(temp_file, new_filename)

            # Do clean-up in the example directory:
            # try:
            #     # Remove epanet2d.exe from the example path
            #     # os.remove(exe_to_example_path)
            #     # Keep the outputs for examining them.
            #     # os.remove(original_)
            #     # os.remove(copy_)
            # except:
            #     pass
            # Return to current directory -- May not need since relative directory was not used anywhere
            os.chdir(current_directory)

        # Write HTML table
        # Print opening HTML tags -------------------------
        text_file.write("<html><body><table border='1'>")
        # Print the content of the table, line by line ----
        for i in range(0, len(examples)):
            cur_status = status[i]
            if cur_status == 'Fail':
                cur_status = '<font color="red">' + status[i] + '</font>'
            text_file.write("<tr><td>" + examples[i].replace(example_root_path, '').strip(os.pathsep) + "</td><td>"
                        + cur_status + "</td><td>"
                        + remarks[i].replace(example_root_path.strip(os.pathsep), '') + "</td></tr>")
        # Print closing HTML tags -------------------------
        text_file.write("</table></body></html>")
        text_file.close()
        try:
            webbrowser.open_new_tab('file://' + html_file)
        except:
            print("Error writing test results to " + html_file)
