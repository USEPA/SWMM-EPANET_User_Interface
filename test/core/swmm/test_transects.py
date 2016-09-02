import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydraulics.link import Transect, Transects
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleTransectTest(unittest.TestCase):
    """Test TRANSECTS section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_one_transect(self):
        """Test one transect from Example-7-final"""
        test_text ="NC\t0.016\t0.016\t0.016\n" \
                   "X1\tFull_Street\t7\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\t0.0\n" \
                   "GR\t1.3\t-40\t0.5\t-20\t0\t-20\t0.8\t0\t0\t20\n" \
                   "GR\t0.5\t20\t1.3\t40"
        self.my_options = Transect()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() #Check this
        new_text = actual_text.replace(" ","")
        #assert new_text == actual_text
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(self.my_options.matches(test_text), msg)

    def test_transects(self):
        """Test transects:Example-7-final inp
        # -- Output does not match input, only one transect was kept and GRs gets combined"""
        test_text = r"""[TRANSECTS]
        NC 0.015    0.015    0.015
        X1 Full_Street       7        0.0      0.0      0.0      0.0      0.0      0.0      0.0
        GR 1.3      -40      0.5      -20      0        -20      0.8      0        0        20
        GR 0.5      20       1.3      40

        NC 0.016    0.016    0.016
        X1 Half_Street       5        0.0      0.0      0.0      0.0      0.0      0.0      0.0
        GR 1.3      -40      0.5      -20      0        -20      0.8      0        1.3      0
        """
        self.my_options = Transects()
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() #Check this
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(self.my_options.matches(test_text), msg)

    def test_transect_section(self):
        """Test transects: using Project
        # -- Output does not match input, only one transect was kept and GRs gets combined"""
        test_text = r"""[TRANSECTS]
        NC 0.015    0.015    0.015
        X1 Full_Street       7        0.0      0.0      0.0      0.0      0.0      0.0      0.0
        GR 1.3      -40      0.5      -20      0        -20      0.8      0        0        20
        GR 0.5      20       1.3      40
        NC 0.016    0.016    0.016
        X1 Half_Street       5        0.0      0.0      0.0      0.0      0.0      0.0      0.0
        GR 1.3      -40      0.5      -20      0        -20      0.8      0        1.3      0
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.transects
        # assert match_omit(project_section.get_text(), test_text, " \t-;\n")
        actual_text = project_section.get_text()
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(project_section.matches(test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()