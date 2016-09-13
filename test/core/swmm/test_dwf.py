import unittest
from core.swmm.hydraulics.node import DryWeatherInflow
from core.swmm.inp_reader_sections import DryWeatherInflowReader
from core.swmm.inp_writer_sections import DryWeatherInflowWriter
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit


class SimpleDWITest(unittest.TestCase):
    """Test DryWeatherInflow(DWF) Section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_example3(self):
        """Test one set of DWI from example 3"""
        test_text = r"""KRO3001          FLOW             1          "" "" "DWF" "" "" "" """""
        my_options = DryWeatherInflowReader.read(test_text)
        actual_text = DryWeatherInflowWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_example8(self):
        """Test one set of DWI from example 8"""
        test_text = r"""J1               FLOW             0.008 """
        my_options = DryWeatherInflowReader.read(test_text)
        actual_text = DryWeatherInflowWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_dwf_section_example3(self):
        """Test DWF section from example 3"""
        source_text = r"""
[DWF]
;;                                  Average    Time
;;Node             Parameter        Value      Patterns
;;-----------------------------------------------------
  KRO3001          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO6015          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO6016          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO6017          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1002          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1003          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1004          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1005          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1006          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1007          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1008          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1009          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1010          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1012          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1013          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO1015          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO2001          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4004          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4008          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4009          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4010          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4011          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4012          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4013          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4014          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4015          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4017          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4018          FLOW             1          "" "" "DWF" "" "" "" ""
  KRO4019          FLOW             1          "" "" "DWF" "" "" "" ""
  SU1              FLOW             1          "" "" "DWF" "" "" "" ""
        """
        section_from_text = self.project_reader.read_dwf.read(source_text)
        actual_text = self.project_writer.write_dwf.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

    def test_dwf_section_example8(self):
        """Test DWF section from example 8"""
        source_text = r"""[DWF]
;;                                Average    Time
;;Node           Parameter        Value      Patterns
;;-------------- ---------------- ---------- ----------
J1               FLOW             0.008
J2a              FLOW             0.01
J12              FLOW             0.0125
J13              FLOW             0.0123
Aux3             FLOW             0.004     """
        section_from_text = self.project_reader.read_dwf.read(source_text)
        actual_text = self.project_writer.write_dwf.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()