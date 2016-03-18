from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.climatology.climatology import EvaporationFormat
import unittest


class SimpleEvaporationTest(unittest.TestCase):
    TEST_TEXT_CONSTANT = ("[EVAPORATION]",
                          ";;Type      \tParameters",
                          ";;----------\t----------",
                          "CONSTANT    \t0.2",
                          "DRY_ONLY    \tNO")

    # TODO: Add testing of each EvaporationFormat

    def runTest(self):
        from_text = Project()
        source_text = '\n'.join(self.TEST_TEXT_CONSTANT)
        from_text.set_text(source_text)
        project_section = from_text.evaporation

        assert Section.match_omit(project_section.get_text(), source_text, " \t-;\n")
        assert project_section.format == EvaporationFormat.CONSTANT
        assert project_section.constant == "0.2"
        assert project_section.monthly == ()
        assert project_section.timeseries == ''
        assert project_section.monthly_pan_coefficients == ()
        assert project_section.recovery_pattern == ''
        assert project_section.dry_only is False
