from core.swmm.hydraulics.node import DirectInflow
import unittest


class SingleInflowTest(unittest.TestCase):

    def setUp(self):

        self.my_options = DirectInflow()

    def runTest(self):

        # Test examples from SWMM 5.1 manual
        test_text = "NODE2  FLOW  N2FLOW "
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.node == 'NODE2'
        assert self.my_options.constituent == 'FLOW'
        assert self.my_options.timeseries == 'N2FLOW'
        # assert self.my_options.format.name == 'CONCENTRATION' # Default,this is odd
        assert self.my_options.conversion_factor == '1.0'  # Default
        assert self.my_options.scale_factor == '1.0'       # Default
        assert self.my_options.baseline == '0.0'           # Default
        assert self.my_options.baseline_pattern == ''
        # assert self.my_options.matches(test_text)
        # -- Does not match as defaults are provided in output, but not in input, OK

        test_text = "NODE65 BOD N65BOD MASS 126"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.node == 'NODE65'
        assert self.my_options.constituent == 'BOD'       # Default
        assert self.my_options.timeseries == 'N65BOD'
        # assert self.my_options.format.name == 'MASS'
        assert self.my_options.conversion_factor == '126'  # Default
        assert self.my_options.scale_factor == '1.0'       # Default
        assert self.my_options.baseline == '0.0'           # Default
        assert self.my_options.baseline_pattern == ''
        # assert self.my_options.matches(test_text)
        # -- Does not match as defaults are provided in output, but not in input, OK

        test_text = "N176 FLOW FLOW176 FLOW 1.0 0.5 12.7 FlowPat"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.node == 'N176'
        assert self.my_options.constituent == 'FLOW'
        assert self.my_options.timeseries == 'FLOW176'
        # assert self.my_options.format.name == 'FLOW'
        assert self.my_options.conversion_factor == '1.0'  # Default
        assert self.my_options.scale_factor == '0.5'       # Default
        assert self.my_options.baseline == '12.7'           # Default
        assert self.my_options.baseline_pattern == 'FlowPat'
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