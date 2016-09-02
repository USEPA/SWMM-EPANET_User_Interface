import unittest
from core.swmm.inp_reader_sections import DirectInflowReader
from core.swmm.inp_writer_sections import DirectInflowWriter
from core.swmm.hydraulics.node import DirectInflow
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleInflowTest(unittest.TestCase):
    """Test INFLOWS section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_flow_type(self):
        """Test inflow: FLOW type"""
        # Test examples from SWMM 5.1 manual
        test_text = "NODE2  FLOW  N2FLOW "
        my_options = DirectInflowReader.read(test_text)
        actual_text = DirectInflowWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        assert my_options.node == 'NODE2'
        assert my_options.constituent == 'FLOW'
        assert my_options.timeseries == 'N2FLOW'
        # assert self.my_options.format.name == 'CONCENTRATION' # Default,this is odd
        assert my_options.conversion_factor == '1.0'  # Default
        assert my_options.scale_factor == '1.0'       # Default
        assert my_options.baseline == '0.0'           # Default
        assert my_options.baseline_pattern == ''
        # assert self.my_options.matches(test_text)
        # -- Does not match as defaults are provided in output, but not in input, OK

    def test_mass_type(self):
        """Test inflow: mass type"""
        test_text = "NODE65 BOD N65BOD MASS 126"
        my_options = DirectInflowReader.read(test_text)
        actual_text = DirectInflowWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        assert my_options.node == 'NODE65'
        assert my_options.constituent == 'BOD'       # Default
        assert my_options.timeseries == 'N65BOD'
        # assert self.my_options.format.name == 'MASS'
        assert my_options.conversion_factor == '126'  # Default
        assert my_options.scale_factor == '1.0'       # Default
        assert my_options.baseline == '0.0'           # Default
        assert my_options.baseline_pattern == ''
        # assert self.my_options.matches(test_text)
        # -- Does not match as defaults are provided in output, but not in input, OK

    def test_flow_ts_type(self):
        """Test inflow: flow time series type"""
        test_text = "N176 FLOW FLOW176 FLOW 1.0 0.5 12.7 FlowPat"
        my_options = DirectInflowReader.read(test_text)
        actual_text = DirectInflowWriter.as_text(my_options)
        msg = '\nSet:' + test_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        assert my_options.node == 'N176'
        assert my_options.constituent == 'FLOW'
        assert my_options.timeseries == 'FLOW176'
        # assert self.my_options.format.name == 'FLOW'
        assert my_options.conversion_factor == '1.0'  # Default
        assert my_options.scale_factor == '0.5'       # Default
        assert my_options.baseline == '12.7'           # Default
        assert my_options.baseline_pattern == 'FlowPat'

    def test_inflows_flow(self):
        """Test INFLOWS section with flow type"""
        source_text = r"""
[INFLOWS]
;;                                                   Concen   Conversion
;;Node             Parameter        Time Series      /Mass    Factor
;;----------------------------------------------------------------------
  80408            FLOW             80408
  81009            FLOW             81009
  82309            FLOW             82310"""
        section_from_text = self.project_reader.read_inflows.read(source_text)
        actual_text = self.project_writer.write_inflows.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

        project_section = section_from_text

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
        source_text=r"""
[INFLOWS]
;;Node          	Constituent     	Time Series     	Type    	Mfactor 	Sfactor 	Baseline	Pattern
;;--------------	----------------	----------------	--------	--------	--------	--------	--------
Inlet           	FLOW            	Inflow          	FLOW    	1.0     	1.0
        """
        section_from_text = self.project_reader.read_inflows.read(source_text)
        actual_text = self.project_writer.write_inflows.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

        project_section = section_from_text
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

def main():
    unittest.main()

if __name__ == "__main__":
    main()
