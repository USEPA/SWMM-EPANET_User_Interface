import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydraulics.node import DirectInflow

class SimpleInflowTest(unittest.TestCase):
    """Test INFLOWS section"""

    def test_flow_type(self):
        """Test inflow: FLOW type"""
        self.my_options = DirectInflow()
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

    def test_mass_type(self):
        """Test inflow: mass type"""
        self.my_options = DirectInflow()
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

    def test_flow_ts_type(self):
        """Test inflow: flow time series type"""
        self.my_options = DirectInflow()
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

    def test_inflows_flow(self):
        """Test INFLOWS section with flow type"""
        test_text = r"""
[INFLOWS]
;;                                                   Concen   Conversion
;;Node             Parameter        Time Series      /Mass    Factor
;;----------------------------------------------------------------------
  80408            FLOW             80408
  81009            FLOW             81009
  82309            FLOW             82310"""
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.inflows

        msg = "Expected 3 items in INFLOWS, found " + str(len(project_section.value))
        self.assertTrue(len(project_section.value) == 3, msg)

        inflow = project_section.value[0]
        msg = "Expected first INFLOW node 80408, found " + inflow.node
        self.assertTrue(inflow.node == "80408", msg)

        msg = "Expected first INFLOW Parameter FLOW, found " + inflow.constituent
        self.assertTrue(inflow.constituent == "FLOW", msg)

        msg = "Expected first INFLOW Time Series 80408, found " + inflow.timeseries
        self.assertTrue(inflow.timeseries == "80408", msg)

        inflow = project_section.value[1]
        msg = "Expected second INFLOW node 81009, found " + inflow.node
        self.assertTrue(inflow.node == "81009", msg)

        msg = "Expected second INFLOW Parameter FLOW, found " + inflow.constituent
        self.assertTrue(inflow.constituent == "FLOW", msg)

        msg = "Expected second INFLOW Time Series 81009, found " + inflow.timeseries
        self.assertTrue(inflow.timeseries == "81009", msg)

        inflow = project_section.value[2]
        msg = "Expected third INFLOW node 82309, found " + inflow.node
        self.assertTrue(inflow.node == "82309", msg)

        msg = "Expected third INFLOW Parameter FLOW, found " + inflow.constituent
        self.assertTrue(inflow.constituent == "FLOW", msg)

        msg = "Expected third INFLOW Time Series 82310, found " + inflow.timeseries
        self.assertTrue(inflow.timeseries == "82310", msg)

    def test_inflows_flowts(self):
        """Test INFLOWS section with FLOW TS type"""
        test_text=r"""
[INFLOWS]
;;Node          	Constituent     	Time Series     	Type    	Mfactor 	Sfactor 	Baseline	Pattern
;;--------------	----------------	----------------	--------	--------	--------	--------	--------
Inlet           	FLOW            	Inflow          	FLOW    	1.0     	1.0
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.inflows
        msg = "Expected 1 item in INFLOWS, found " + str(len(project_section.value))
        self.assertTrue(len(project_section.value) == 1, msg)

        inflow = project_section.value[0]
        msg = "Expected INFLOW node Inlet, found " + inflow.node
        self.assertTrue(inflow.node == "Inlet", msg)

        msg = "Expected INFLOW Parameter FLOW, found " + inflow.constituent
        self.assertTrue(inflow.constituent == "FLOW", msg)

        msg = "Expected INFLOW Time Series Inflow, found " + inflow.timeseries
        self.assertTrue(inflow.timeseries == "Inflow", msg)

        msg = "Expected INFLOW Conversion Factor 1.0, found " + inflow.conversion_factor
        self.assertTrue(inflow.conversion_factor == "1.0", msg)

        msg = "Expected INFLOW Scaling Factor 1.0, found " + inflow.scale_factor
        self.assertTrue(inflow.scale_factor == "1.0", msg)
