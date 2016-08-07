import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydrology.subcatchment import Groundwater


class SimpleGroundwaterTest(unittest.TestCase):
    """Test GROUNDWATER section"""

    def test_groundwater(self):
        """Test one set of groundwater parameters"""
        self.my_options = Groundwater()
        test_text = \
            "SUB1    AQF1 	ND2 	6     	0.1   	1     	0     	0     	0     	0     	4"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() # display purpose
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(self.my_options.matches(test_text), msg)

    def test_groundwater_section(self):
        """Test GROUNDWATER section through Project Class"""
        # -- Failed Empty string get_text
        from_text = Project()
        test_text =" [GROUNDWATER]\n" \
                     ";;Subcatchment  	Aquifer         	Node            	Elev  	A1    	B1    	A2    	B2    	A3    	Hsw   	Hcb   	BEL   	WTEL  	UZM\n" \
                     ";;--------------	----------------	----------------	------	------	------	------	------	------	------	------	------	------	------\n" \
                     "1               	1               	2               	6     	0.1   	1     	0     	0     	0     	0     	4"
        from_text.set_text(test_text)
        project_section = from_text.groundwater
        actual_text = project_section.get_text()
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(project_section.matches(test_text), msg)

        # assert match_omit(project_section.get_text(), source_text, " \t-;\n")
