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
            assert len(my_project.sections) == 29

            with open(inp_filename + ".written_inp.txt", 'w') as writer:
                writer.writelines(my_project.text)
            with open(inp_filename + ".written_inp_spaces.inp", 'w') as writer:
                writer.writelines(' '.join(my_project.text.split()))
            with open(inp_filename + ".written_orig_spaces.inp", 'w') as writer:
                with open(inp_filename, 'r') as read_inp:
                    writer.writelines(' '.join(read_inp.read().split()))

            with open(inp_filename, 'r') as read_inp:
                assert ' '.join(self.my_project.text.split()) == ' '.join(read_inp.read().split())

my_project = core.epanet.project.Project()
my_project.read_file("Net1.inp")
with open("Net1.written.inp", 'w') as writer:
    writer.writelines(my_project.text)