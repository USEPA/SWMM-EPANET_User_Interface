import unittest
from core.swmm.inp_reader_sections import SubcatchmentReader
from core.swmm.inp_writer_sections import SubcatchmentWriter
from core.swmm.hydrology.subcatchment import Subcatchment
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleSubcatchmentTest(unittest.TestCase):
    """Test SUBCATCHMENTS section"""

    TEST_TEXTS = ["SUB1  RG1	OT2	5	0	140     0.05 	0 s1"]
    SOURCE_TEXTS = ["""[SUBCATCHMENTS]
;;                                                   Total    Pcnt.             Pcnt.    Curb     Snow
;;Name             Raingage         Outlet           Area     Imperv   Width    Slope    Length   Pack
;;----------------------------------------------------------------------------------------------------
  1                RG1              9                10       50       500      0.01     0
  2                RG1              10               10       50       500      0.01     0
  3                RG1              13               5        50       500      0.01     0
  4                RG1              22               5        50       500      0.01     0
  5                RG1              15               15       50       500      0.01     0
  6                RG1              23               12       10       500      0.01     0
  7                RG1              19               4        10       500      0.01     0
  8                RG1              18               10       10       500      0.01     0
"""]

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_pk(self):
        """Test one set of subcatchment parameters with spack"""
        for test_text in self.TEST_TEXTS:
            my_options = SubcatchmentReader.read(test_text)
            actual_text = SubcatchmentWriter.as_text(my_options)
            msg = '\nSet:'+test_text+'\nGet:'+actual_text
            self.assertTrue(match(actual_text, test_text), msg)

    def test_nopk(self):
        """Test one set of subcatchment parameters without spack"""
        # This should print fine
        test_subcatchment_wospack = "SUB1	RG1	OT2	5	0 140	0.5	0"
        for test_text in [test_subcatchment_wospack]:
            my_options = SubcatchmentReader.read(test_text)
            actual_text = SubcatchmentWriter.as_text(my_options)
            msg = '\nSet:'+test_text+'\nGet:'+actual_text
            self.assertTrue(match(actual_text, test_text), msg)

    def test_missing(self):
        """Test one set of subcatchment parameters missing last two parameters Slope and Clength"""
        # This should report error
        test_text = "SUB1	RG1	OT2	5 0 140"
        try:
            my_options = SubcatchmentReader.read(test_text)
            actual_text = SubcatchmentWriter.as_text(my_options)
            msg = '\nSet:' + test_text + '\nGet:' + actual_text
            msg = "\nShould detected error and not read/write"
            find_error = False
        except Exception as e:
            msg = "\nSet:" + test_text + '\nGet:' + str(e)
            find_error = True
        self.assertTrue(find_error, msg)

        # self.assertFalse(self.my_options.matches(test_subcatchment_partial))

    def test_subcatchments(self):
        """Test SUBCATCHMENTS section from Example 1"""
        for source_text in self.SOURCE_TEXTS:
            section_from_text = self.project_reader.read_subcatchments.read(source_text)
            actual_text = self.project_writer.write_subcatchments.as_text(section_from_text)
            msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
            self.assertTrue(match(actual_text, source_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
