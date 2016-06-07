import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydrology.subcatchment import Groundwater


class SimpleGroundwaterTest(unittest.TestCase):
    """Test GROUNDWATER section"""

    def test_groundwater(self):
        """Test one set of groundwater parameters"""
        self.my_options = Groundwater()
        test_groundwater = \
            "SUB1    AQF1 	ND2 	6     	0.1   	1     	0     	0     	0     	0     	4"
        self.my_options.set_text(test_groundwater)
        assert self.my_options.matches(test_groundwater)


    def test_groundwater_section(self):
        """Test GROUNDWATER section through Project Class"""
        from_text = Project()
        source_text =" [GROUNDWATER]\n" \
                     ";;Subcatchment  	Aquifer         	Node            	Elev  	A1    	B1    	A2    	B2    	A3    	Hsw   	Hcb   	BEL   	WTEL  	UZM\n" \
                     ";;--------------	----------------	----------------	------	------	------	------	------	------	------	------	------	------	------\n" \
                     "1               	1               	2               	6     	0.1   	1     	0     	0     	0     	0     	4"
        # --Test set_text
        from_text.set_text(source_text)
        project_section = from_text.groundwater
        assert Section.match_omit(project_section.get_text(), source_text, " \t-;\n")
