import os
import core.epanet.project
import unittest


class ProjectTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_project = core.epanet.project.Project()

    def runTest(self):
        for inp_filename in ["Net1.inp"]:
            self.my_project.read_file(inp_filename)
            assert len(self.my_project.sections) == 29

            with open(inp_filename + ".written_inp.txt", 'w') as writer:
                writer.writelines(self.my_project.get_text())
            with open(inp_filename + ".written_inp_spaces.inp", 'w') as writer:
                writer.writelines(' '.join(self.my_project.get_text().split()))
            with open(inp_filename + ".written_orig_spaces.inp", 'w') as writer:
                with open(inp_filename, 'r') as read_inp:
                    writer.writelines(' '.join(read_inp.read().split()))

            with open(inp_filename, 'r') as read_inp:
                assert ' '.join(self.my_project.get_text().split()) == ' '.join(read_inp.read().split())
