""" Regression testing of EPANET model.
    Open Examples folder in same folder as this module and find *.inp files in Examples and its first-level sub-folders.
    For each file, e.g. "model_name.inp", check whether there is corresponding output named "benchmark/model_name.out"
        If benchmark output is not found, create a benchmark output:
            run the model and generate "benchmark/model_name.out" (and .rpt) and do not try to compare it.
        If benchmark output already exists:
            delete any existing "candidate/model_name.out" (and candidate/model_name.rpt)
            run the model and generate "candidate/model_name.out" (and .rpt)
            compare with "benchmark/model_name.out" (and .rpt) and generate a report

    This can be run from within a unit testing framework or can be run directly via __main__ check at the end.

    Based on two existing modules:
        https://github.com/USEPA/SWMM-EPANET_User_Interface/blob/master/test/core/epanet/test_project.py
        https://github.com/OpenWaterAnalytics/EPANET/blob/dev-2.1/tools/outputapi/ENBinaryOutDiff.py
"""

import os, sys
import math
import inspect
import shutil
import unittest
import webbrowser
from Externals.epanet.outputapi.ENOutputWrapper import OutputObject, ENR_node_type, ENR_link_type


class RegressionTest(unittest.TestCase):    
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.show_html_report = True

    def runTest(self):
        # Get full path this module is in, e.g. "C:\dev\SWMM-EPANET_User_Interface_master\src\Externals\test\epanet"
        test_directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))
        any_passed = False
        any_failed = False

        # Get path to epanet2d.exe
        source_root_path = os.path.split(os.path.split(os.path.split(test_directory)[0])[0])[0]
        exe_path = os.path.join(source_root_path, "Externals", "epanet", "model")
        exe_name = "epanet2d.exe"
        exe_full_path = os.path.join(exe_path, exe_name)

        # Get example path and the paths to its first level sub directories
        # Assuming all tests are under Examples or immediate level sub directories
        example_root_path = os.path.join(test_directory, "Examples")
        example_paths = list()
        example_paths.append(example_root_path)
        example_sub_directories = RegressionTest.get_immediate_subdirectories(example_root_path)
        if example_sub_directories:
            for subdir in example_sub_directories:
                example_paths.append(os.path.join(example_root_path, subdir))

        # Loop through all .inp files in Examples and first-level sub directories
        status = list()   # example test status 'Pass' or 'Fail'
        remarks = list()  # error message goes here

        # Get current_directory for restoring it later
        current_directory = os.getcwd()  # current test/core/

        # Test all examples in /Examples or first level sub directory of /Examples
        for example_path in example_paths:

            # Get example directory
            os.chdir(example_path)

            # Get all file names under this example directory
            example_files = os.listdir(example_path)

            # Loop through all .inp files in the /Examples folder
            for filename in example_files:
                inp_filename_base, extension = os.path.splitext(filename)
                if extension.lower() == ".inp":
                    inp_file = filename

                    benchmark_dir = os.path.join(os.path.dirname(inp_filename_base), "benchmark")
                    benchmark_prefix = os.path.join(benchmark_dir, os.path.split(inp_filename_base)[-1])
                    benchmark_rpt = benchmark_prefix + '.rpt'
                    benchmark_out = benchmark_prefix + '.out'
                    if os.path.isfile(benchmark_out):
                        # Already have a benchmark, want to produce and check a candidate.
                        # Run this input file with outputs saved in "candidate" folder.
                        out_dir = os.path.join(os.path.dirname(inp_filename_base), "candidate")
                    else:
                        # Do not yet have a benchmark, run to create one.
                        out_dir = benchmark_dir

                    if not os.path.exists(out_dir):
                        os.makedirs(out_dir)
                    out_prefix = os.path.join(out_dir, os.path.split(inp_filename_base)[-1])
                    ran_rpt = out_prefix + '.rpt'
                    ran_out = out_prefix + '.out'
                    if os.path.isfile(ran_rpt):
                        os.remove(ran_rpt)
                    if os.path.isfile(ran_out):
                        os.remove(ran_out)

                    command_line = '"' + exe_full_path + '" ' + inp_file + ' ' + ran_rpt + ' ' + ran_out
                    try:
                        os.system(command_line)
                    except:
                        status.append('----')
                        remarks.append("Error in executing {}".format(command_line))

                    if out_dir == benchmark_dir:
                        # Created benchmark version, no need to compare
                        status.append('Pass')
                        any_passed = True
                        remarks.append(inp_filename_base + ': Created benchmark run\n')
                    else:
                        diff_msg = RegressionTest.compare_binary_files(benchmark_out, ran_out, 5)
                        if diff_msg:
                            status.append('Fail')
                            any_failed = True
                            remarks.append(
                                inp_filename_base + ' output:' +
                                'results of modified differ from results of original binary output' + '\n' +
                                diff_msg + '\n')
                        else:
                            status.append('Pass')
                            any_passed = True
                            remarks.append(inp_filename_base + ' output successful matching' + '\n')

                        # Compare two rpt files
                        exempted_strings = ["Analysis begun", "Analysis ended",
                                            "Total elapsed time", "ERROR",
                                            "Input Data File", "Page 1"]
                        if os.path.isfile(benchmark_rpt) and os.path.isfile(ran_rpt):
                            diff_msg = RegressionTest.compare_text_files(benchmark_rpt, ran_rpt, exempted_strings)
                            if diff_msg:
                                status.append('Fail')
                                any_failed = True 
                                remarks.append(
                                    inp_filename_base + ' rpt:' +
                                    'results of modified differ from results of original\n' +
                                    diff_msg + '\n')
                            else:
                                status.append('Pass')
                                any_passed = True
                                remarks.append(inp_filename_base + ' rpt successful matching' + '\n')

                        # If the original does not produce .out '----'
                        elif not os.path.isfile(benchmark_rpt):
                            status.append('----')
                            remarks.append(benchmark_rpt + ' does not exist, original input did not run\n')

                        # If the original does but the copy does not produce .out 'Fail'
                        else:
                            status.append('Fail')
                            all_passed = False
                            remarks.append(ran_rpt + ' does not exist, original ran but modified did not\n')

            os.chdir(current_directory)

        if self.show_html_report:
            html_file = os.path.join(test_directory, 'Test_Summary_EPANET.html')
            with open(html_file, "w") as html_file_writer:
                html_file_writer.write('<header><h1>'+'TEST REPORT:'+'</h1></header>')
                # Write HTML table
                # Print opening HTML tags -------------------------
                html_file_writer.write("<html><body><table border='1'>")
                # Print the content of the table, line by line ----
                for i in range(0, len(status)):
                    cur_status = status[i]
                    if cur_status == 'Fail':
                        cur_status = '<font color="red">' + status[i] + '</font>'
                    html_file_writer.write( #"<tr><td>" + examples[i].replace(example_root_path, '').strip(os.pathsep) + "</td>
                        "<td>" + cur_status + "</td><td>"
                               + remarks[i].replace(example_root_path.strip(os.pathsep), '') + "</td></tr>")
                # Print closing HTML tags -------------------------
                html_file_writer.write("</table></body></html>")
                html_file_writer.close()
                try:
                    webbrowser.open_new_tab('file://' + html_file)
                except:
                    print("Error writing test results to " + html_file)

        return any_passed and not any_failed

    @staticmethod
    def compare_binary_files(benchmark_file, candidate_file, significant_digits):
        """ Compare two EPANET binary output files.
            Returns
            Empty string if all node and link attributes at all time steps match within significant_digits.
            Report string indicating first mismatched value if any value does not match within significant_digits.
        """
        report = list()
        output_file_benchmark = OutputObject(benchmark_file)
        output_file_candidate = OutputObject(candidate_file)
        assert output_file_candidate.num_periods == output_file_benchmark.num_periods

        for time_index in range(output_file_benchmark.num_periods):
            # Compare Node Attributes
            for attribute in ENR_node_type.Attributes:
                # Get attribute for all nodes at time_index
                va_benchmark = ENR_node_type.get_attribute_for_all_at_time(output_file_benchmark, attribute, time_index)
                va_candidate = ENR_node_type.get_attribute_for_all_at_time(output_file_candidate, attribute, time_index)
                for node_index, benchmark_value in enumerate(va_benchmark):
                    candidate_value = va_candidate[node_index]
                    if RegressionTest.large_difference(benchmark_value, candidate_value, significant_digits):
                        diff = abs(benchmark_value - candidate_value)
                        report.append("At time index {} node {} attribute {} differs before {} significant digits:\n"\
                              "{} = {}\n{} = {}\ndelta = {}".format(
                            time_index, node_index, attribute.name, significant_digits,
                            benchmark_file, benchmark_value, candidate_file, candidate_value, diff))

            # Compare Link Attributes
            for attribute in ENR_link_type.Attributes:
                # Get attribute for all links at time_index
                va_benchmark = ENR_link_type.get_attribute_for_all_at_time(output_file_benchmark, attribute, time_index)
                va_candidate = ENR_link_type.get_attribute_for_all_at_time(output_file_candidate, attribute, time_index)
                for link_index, benchmark_value in enumerate(va_benchmark):
                    candidate_value = va_candidate[link_index]
                    if RegressionTest.large_difference(benchmark_value, candidate_value, significant_digits):
                        diff = abs(benchmark_value - candidate_value)
                        report.append("At time index {} link {} attribute {} differs before {} significant digits:\n"\
                                "{} = {}\n{} = {} :: delta = {}".format(
                            time_index, link_index, attribute.name, significant_digits,
                            benchmark_file, benchmark_value, candidate_file, candidate_value, diff))
        return '<br>\n'.join(report)

    @staticmethod
    def large_difference(benchmark_value, candidate_value, significant_digits):
        """True if benchmark_value and candidate_value differ within the first decimal_places significant digits"""
        diff = abs(benchmark_value - candidate_value)
        return diff > 0 and significant_digits + math.log10(diff) > 0

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
    def compare_text_files(fname1, fname2, exempted_strings):
        """Reference: http://www.opentechguides.com/how-to/article/python/58/python-file-comparison.html
        Modified by xw 2016/05/12
        Strip all white spaces, empty lines and exempt the lines with exempted_strings
        Return a string message diff_msg. If identical, return empty string
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
        line_read, f1_line = RegressionTest.readline_nowhite(f1)
        line_no_f1 = line_no_f1 + line_read

        # File 2:
        line_read, f2_line = RegressionTest.readline_nowhite(f2)
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
                    diff_msg = '<br>[old]Line-'+str(line_no_f1)+':'+f1_line+'<br>'+ \
                               '[new]Line-'+str(line_no_f2)+':'+f2_line+'<br>'
                    # Break on the first difference
                    break

            # File 1:
            line_read, f1_line = RegressionTest.readline_nowhite(f1)
            line_no_f1 = line_no_f1 + line_read

            # File 2:
            line_read, f2_line = RegressionTest.readline_nowhite(f2)
            line_no_f2 = line_no_f2 + line_read

        # Close the files
        f1.close()
        f2.close()
        return diff_msg


if __name__ == '__main__':
    my_test = RegressionTest()
    my_test.setUp()
    if my_test.runTest():
        sys.exit(0)
    else:
        sys.exit(1)
