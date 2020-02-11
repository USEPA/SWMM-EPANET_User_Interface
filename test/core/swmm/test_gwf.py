import unittest
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from core.swmm.inp_reader_sections import GWFReader
from core.swmm.inp_writer_sections import GWFWriter
from test.core.section_match import match, match_omit
from core.swmm.hydrology.subcatchment import GroundwaterFlowType


class SimpleGWFTest(unittest.TestCase):
    """Test GWF section"""

    TEST_TEXT = ("[GWF]",
                 ";;Subcatchment   Flow    Equation",
                 ";;-------------- ------- --------",
                 "CA-11            LATERAL 0.001 * (Hgw - 5) * STEP(Hgw - 5)")

    def test_gwf(self):
        """Test GWF section using the Project class"""
        source_text = '\n'.join(self.TEST_TEXT)
        project_reader = ProjectReader()
        project_writer = ProjectWriter()
        section_from_text = project_reader.read_gwf.read(source_text)

        actual_text = project_writer.write_gwf.as_text(section_from_text)
        msg = '\nSet:'+source_text+'\nGet:'+actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

        val = section_from_text.value[0]

        assert val.subcatchment_name == "CA-11"
        assert val.groundwater_flow_type == GroundwaterFlowType.LATERAL
        assert val.custom_equation == ''.join("0.001 * (Hgw - 5) * STEP(Hgw - 5)".split())  # remove formatting


    def test_gwf(self):
        """Test one set of GWF parameters"""
        test_text = "CA-11            DEEP    0.01*Hgs"
        my_options = GWFReader.read(test_text)
        actual_text = GWFWriter.as_text(my_options) # display purpose
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()