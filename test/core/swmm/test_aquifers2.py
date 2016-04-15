from core.swmm.hydrology.aquifer import Aquifer
import unittest


class HydrologyAquiferTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Aquifer()

    def runTest(self):
        # Test default, default is empty string, no adjustments, Failed because
        # -- aquifer does not have SECTION_NAME
        # -- get_text produced string with tabs instead of empty string
        name = self.my_options.SECTION_NAME
        assert name == "[AQUIFERS]"
        actual_text = self.my_options.get_text()
        assert actual_text == ''

        # Test aquifer parameters in Example 5
        test_aquifer = r"""
        [AQUIFERS]
        ;;Aquifer       	Phi   	WP    	FC    	HydCon	Kslope	Tslope	UEF   	LED   	LGLR  	BEL   	WTEL  	UZM   	UEF Pat
        ;;--------------	------	------	------	------	------	------	------	------	------	------	------	------	------
               1            	0.5   	0.15  	0.30  	0.1   	12    	15.0  	0.35  	14.0  	0.002 	0.0   	3.5   	0.40
        """
        # --Test set_text
        self.my_options.set_text(test_aquifer)
        # --Test get_text through matches
        # --Failed, this data structure appears to be messy
        # --Error:Session name [AQUIFER] is after the parameters
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_aquifer)