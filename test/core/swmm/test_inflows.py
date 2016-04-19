from core.swmm.hydraulics.node import DirectInflow
import unittest


class SingleInflowTest(unittest.TestCase):

    def setUp(self):

        self.my_options = DirectInflow()

    def runTest(self):

        # Test examples from SWMM 5.1 manual
        test_text = r"""NODE2  FLOW  N2FLOW """
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        test_text = r"""NODE65 BOD N65BOD MASS 126"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        test_text = r"""N176 FLOW FLOW176 FLOW 1.0 0.5 12.7 FlowPat"""
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)

        pass

class MultiInflowsTest(unittest.TestCase):

    def setUp(self):

        self.my_options = DirectInflow()

    def runTest(self):

        test_text = r"""
[INFLOWS]
;;                                                   Concen   Conversion
;;Node             Parameter        Time Series      /Mass    Factor
;;----------------------------------------------------------------------
  80408            FLOW             80408
  81009            FLOW             81009
  82309            FLOW             82309
[INFLOWS]
;;Node          	Constituent     	Time Series     	Type    	Mfactor 	Sfactor 	Baseline	Pattern
;;--------------	----------------	----------------	--------	--------	--------	--------	--------
Inlet           	FLOW            	Inflow          	FLOW    	1.0     	1.0


        """
        # --Test set_text


        pass