import os
import core.swmm.project
import unittest
import inspect


class ProjectTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_project = core.swmm.project.Project()
        self.new_project = core.swmm.project.Project()

    def runTest(self):
        directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))
        example_path = os.path.join(directory, "Examples")
        example_files = os.listdir(example_path)

        # Loop through all .inp files in the Examples folder
        for filename in example_files:
            file_extension = os.path.splitext(filename)[1]
            if file_extension.lower() == ".inp":
                # Read .inp file, count the number of sections
                my_file = os.path.join(example_path,filename)
                self.my_project.read_file(my_file)
                number_of_sections = len(self.my_project.sections)

                # Writing my_project to new file .inptest
                new_file = my_file + "test"
                self.my_project.write_file(new_file)

                # Read .inptest into new_project, count the number of sections, assert
                self.new_project.read_file(new_file)
                new_number_of_sections = len(self.new_project.sections)
                assert number_of_sections == new_number_of_sections

                # If the numbers of sections agree, match each section
                if number_of_sections == new_number_of_sections:
                    for (old_section, new_section) in \
                            zip(self.my_project.sections, self.new_project.sections):

                        pass
                    # assert old_section == new_section
                    # Sequences are different, how do we test these? Think about it now.
                    # How about run the SWMM and check the results ?
                # os.remove(new_filename)
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
