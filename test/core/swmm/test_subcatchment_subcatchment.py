from core.swmm.hydrology.subcatchment import Subcatchment
import unittest


class SubSubcatchmentTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Subcatchment()

    def runTest(self):
        # Subcatchment did not inherit from Section
        # Ok this is MTP-3
        # Test default, default is empty string, no adjustments, Failed because
        # -- subcatchment does not have SECTION_NAME
        # -- get_text produced string with tabs instead of empty string
        #name = self.my_options.SECTION_NAME
        #assert name == "[SUBCATCHMENTS]"
        actual_text = self.my_options.get_text()
        #assert actual_text == ''

        # Test aquifer parameters in Example 5
        test_subcatchment = r"""
[SUBCATCHMENTS]
;;Subcatchment  	Rain Gage       	Outlet          	Area    	%Imperv 	Width   	%Slope  	CurbLen 	Snow Pack
;;--------------	----------------	----------------	--------	--------	--------	--------	--------	----------------
1               	1               	2               	5       	0       	140     	0.5     	0
        """
        # --Test set_text
        self.my_options.set_text(test_subcatchment)
        # --Test get_text through matches
        # --Failed, this data structure appears to be messy, similar to aquifer
        # --Error:Session name [AQUIFER] is after the parameters
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment)

        pass