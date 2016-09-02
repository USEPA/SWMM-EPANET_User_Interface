import unittest
from core.swmm.inp_reader_sections import JunctionReader
from core.swmm.inp_writer_sections import JunctionWriter
from core.swmm.hydraulics.node import Junction
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleJunctionTest(unittest.TestCase):
    """Test JUNCTIONS section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_all_opts(self):
        """Test junction with all options"""
        test_text = " J1 2.0 0.1 0.2 0.3 0.4"
        my_options = JunctionReader.read(test_text)
        actual_text = JunctionWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_selected_parameters(self):
        """Test junction omit some parameters"""
        test_text = " J1 2.0 "
        my_options = JunctionReader.read(test_text)
        actual_text = JunctionWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_junctions(self):
        """Test JUNCTIONS section through Project class"""
        source_text = r"""
[JUNCTIONS]
;;               Invert     Max.       Init.      Surcharge  Ponded
;;Name           Elev.      Depth      Depth      Depth      Area
;;-------------- ---------- ---------- ---------- ---------- ----------
J1               4973       0          0          0          0
J2               4969       0          0          0          0
J3               4973       0          0          0          0
J4               4971       0          0          0          0
J5               4969.8     0          0          0          0
J6               4969       0          0          0          0
J7               4971.5     0          0          0          0
J8               4966.5     0          0          0          0
J9               4964.8     0          0          0          0
J10              4963.8     0          0          0          0
J11              4963       0          0          0          0
J12              4973.8     0          0          0          0
J13              4970.7     0          0          0          0
J14              4972.9     0          0          0          0
J15              4974.5     0          0          0          0
J16              4973.5     0          0          0          0
J17              4973.5     0          0          0          0
        """
        section_from_text = self.project_reader.read_junctions.read(source_text)
        actual_text = self.project_writer.write_junctions.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
