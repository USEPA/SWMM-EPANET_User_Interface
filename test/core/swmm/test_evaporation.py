import unittest
from core.swmm.climatology import Evaporation
from core.swmm.climatology import EvaporationFormat
from core.swmm.inp_reader_sections import EvaporationReader
from core.swmm.inp_writer_sections import EvaporationWriter
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit


class EvaporationTest(unittest.TestCase):
    """Test all options provided in EVAPORATION section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_bare(self):
        """testing bare section"""
        my_options = Evaporation()
        # default is empty string, no evaporation
        name = my_options.SECTION_NAME
        assert name == "[EVAPORATION]"

        test_text = ""
        my_options = EvaporationReader.read(test_text)
        actual_text = EvaporationWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        # -- [EVAPORATION] always written regardless of inputs, OK with bare session

    def test_constant_only(self):
        """testing constant only without DRY_ONLY"""
        test_text = "[EVAPORATION]\n" \
                    ";;Data Source    Parameters\n" \
                    ";;-------------- ----------------\n" \
                    " CONSTANT         0.0"
        my_options = EvaporationReader.read(test_text)
        actual_text = EvaporationWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        assert my_options.constant == '0.0'
        assert my_options.dry_only == False
        # assert self.my_options.matches(test_constant_wo_dryonly),
        # "If DRY_ONLY is not specified, match returns False."
        # -- DRY_ONLY is always written regardless of inputs
        # DRY only is False (NO) by default, OK.

    def test_constant_wt_dry_only(self):
        """Test constant with DRY_ONLY, consistent with most examples"""
        test_text = "[EVAPORATION]\n" \
                        ";;Data Source    Parameters\n" \
                        ";;-------------- ----------------\n" \
                        " CONSTANT         0.0\n" \
                        " DRY_ONLY         NO"
        my_options = EvaporationReader.read(test_text)
        actual_text = EvaporationWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_monthly(self):
        """Test monthly Example User2 and a few others"""
        test_text = "[EVAPORATION]\n" \
                       ";;Type         Parameters\n" \
                       ";;-----------------------\n" \
                       "MONTHLY      0.01   0.04   0.05   0.05   0.1    0.24" \
                       "   0.25   0.24   0.16   0.11   0.03   0.01\n" \
                       "DRY_ONLY     Yes"
        my_options = EvaporationReader.read(test_text)
        actual_text = EvaporationWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_monthly_fail(self):
        """MONTHLY - edge case missing a month"""
        # -- I think the case should fail because it is missing a month
        # -- Currently do not have the missing value detection ability
        test_text = "[EVAPORATION]\n" \
                       ";;Type         Parameters\n" \
                       ";;-----------------------\n" \
                       " MONTHLY      0.01   0.04   0.05   0.05   0.1    0.24" \
                       "   0.25   0.24   0.16   0.11   0.03\n" \
                       "DRY_ONLY No"
        my_options = EvaporationReader.read(test_text)
        actual_text = EvaporationWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_timeseries(self):
        """TIMESERIES Tseries"""
        test_text = "[EVAPORATION]\n" \
                    ";;Type         Parameters\n" \
                    ";;-----------------------\n" \
                    "TIMESERIES TS1"
        my_options = EvaporationReader.read(test_text)
        actual_text = EvaporationWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_temperature(self):
        """test temperature option"""
        test_text = "[EVAPORATION]\n" \
                    ";;Type         Parameters\n" \
                    ";;-----------------------\n" \
                    "TEMPERATURE"
        my_options = EvaporationReader.read(test_text)
        actual_text = EvaporationWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_file(self):
        """Test file option"""
        test_text = "[EVAPORATION]\n" \
                    ";;Type         Parameters\n" \
                    ";;-----------------------\n" \
                    "FILE"
        my_options = EvaporationReader.read(test_text)
        actual_text = EvaporationWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_recovery(self):
        """Test recovery option RECOVERY PatternID"""
        test_text = "[EVAPORATION]\n" \
                    ";;Type         Parameters\n" \
                    ";;-----------------------\n" \
                    "RECOVERY  pattern1"
        my_options = EvaporationReader.read(test_text)
        actual_text = EvaporationWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_project_section(self):
        """Test EVAPORATION use project section"""
        source_text = "[EVAPORATION]\n" \
                      ";;Type      \tParameters\n" \
                      ";;----------\t----------\n" \
                      "CONSTANT    \t0.2\n" \
                      "DRY_ONLY    \tNO"
        section_from_text = self.project_reader.read_evaporation.read(source_text)
        actual_text = self.project_writer.write_evaporation.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)

        assert section_from_text.format == EvaporationFormat.CONSTANT
        assert section_from_text.constant == "0.2"
        assert section_from_text.monthly == ()
        assert section_from_text.timeseries == ''
        assert section_from_text.monthly_pan_coefficients == ()
        assert section_from_text.recovery_pattern == ''
        assert section_from_text.dry_only is False

def main():
    unittest.main()

if __name__ == "__main__":
    main()