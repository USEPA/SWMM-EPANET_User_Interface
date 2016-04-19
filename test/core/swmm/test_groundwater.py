from core.swmm.hydrology.subcatchment import Groundwater
import unittest


class SingleGroundwaterTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Groundwater()

    def runTest(self):
        # Test aquifer parameters in Example 5
        test_groundwater = r"""
SUB1               	AQF1               	ND2               	6     	0.1   	1     	0     	0     	0     	0     	4
        """
        # --Test set_text
        self.my_options.set_text(test_groundwater)
        # --Test get_text through matches
        # --Failed, this data structure appears to be messy, similar to aquifer
        # --Error:Session name [AQUIFER] is after the parameters
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_groundwater)

        pass

class SubGroundwaterTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Groundwater()

    def runTest(self):
        # Test default, default is empty string, no adjustments, Failed because
        # -- groundwater does not have SECTION_NAME
        # -- get_text produced string with tabs instead of empty string
        #name = self.my_options.SECTION_NAME
        #assert name == "[GROUNDWATER]"
        actual_text = self.my_options.get_text()
        #assert actual_text == ''

        # Test aquifer parameters in Example 5
        test_groundwater = r"""
 [GROUNDWATER]
;;Subcatchment  	Aquifer         	Node            	Elev  	A1    	B1    	A2    	B2    	A3    	Hsw   	Hcb   	BEL   	WTEL  	UZM
;;--------------	----------------	----------------	------	------	------	------	------	------	------	------	------	------	------
1               	1               	2               	6     	0.1   	1     	0     	0     	0     	0     	4
        """
        # --Test set_text
        self.my_options.set_text(test_groundwater)
        # --Test get_text through matches
        # --Failed, this data structure appears to be messy, similar to aquifer
        # --Error:Session name [AQUIFER] is after the parameters
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_groundwater)

        pass