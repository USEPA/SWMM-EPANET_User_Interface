import unittest
from core.swmm.hydrology.subcatchment import Groundwater
from core.swmm.inp_reader_sections import GroundwaterReader
from core.swmm.inp_writer_sections import GroundwaterWriter
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit


class SimpleGroundwaterTest(unittest.TestCase):
    """Test GROUNDWATER section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_groundwater(self):
        """Test one set of groundwater parameters"""
        test_text = \
            "SUB1    AQF1 	ND2 	6     	0.1   	1     	0     	0     	0     	0     	4"
        my_options = GroundwaterReader.read(test_text)
        actual_text = GroundwaterWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_groundwater_section(self):
        """Test GROUNDWATER section through Project Class"""
        # -- Failed Empty string get_text
        source_text =" [GROUNDWATER]\n" \
                     ";;Subcatchment  	Aquifer         	Node            	Elev  	A1    	B1    	A2    	B2    	A3    	Hsw   	Hcb   	BEL   	WTEL  	UZM\n" \
                     ";;--------------	----------------	----------------	------	------	------	------	------	------	------	------	------	------	------\n" \
                     "1               	1               	2               	6     	0.1   	1     	0     	0     	0     	0     	4"
        section_from_text = self.project_reader.read_groundwater.read(source_text)
        actual_text = self.project_writer.write_groundwater.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
