from core.swmm.hydrology.subcatchment import Subareas
import unittest


class SubAreasTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Subareas()

    def runTest(self):
        # Do not have Subareas at this moment
        # This is MTP-3, place holder only
        # Test default, default is empty string, no adjustments, Failed because
        #name = self.my_options.SECTION_NAME
        #assert name == "[SUBAREAS]"
        #actual_text = self.my_options.get_text()
        #assert actual_text == ''

        # Test aquifer parameters in Example 5
        test_subarea = r"""
[SUBAREAS]
;;Subcatchment  	N-Imperv  	N-Perv    	S-Imperv  	S-Perv    	PctZero   	RouteTo   	PctRouted
;;--------------	----------	----------	----------	----------	----------	----------	----------
1               	0.01      	0.1       	0.05      	0.05      	25        	OUTLET
"""
        # --Test set_text
        self.my_options.set_text(test_subarea)
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subarea)

        pass