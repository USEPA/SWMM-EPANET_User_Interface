from core.inputfile import Section
from core.epanet.project import Project
from core.epanet.hydraulics.node import SourceType
import unittest


class SimpleSourcesTest(unittest.TestCase):

    TEST_TEXT = ("[SOURCES]",
                 ";Node         \tType         \tQuality \tPattern",
                 " JUNCTION-9090\tCONCEN       \t8330    \tPattern-A",
                 " JUNCTION-9091\tMASS         \t8331    \tPattern-B",
                 " JUNCTION-9092\tFLOWPACED    \t8332    \tPattern-C",
                 " JUNCTION-9093\tSETPOINT     \t8333    \tPattern-D",
                 " JUNCTION-9094\tCONCEN       \t8334")

    def runTest(self):
        from_text = Project()
        source_text = '\n'.join(self.TEST_TEXT)
        from_text.set_text(source_text)
        project_sources = from_text.sources

        assert Section.match_omit(project_sources.get_text(), source_text, " \t-;\n")

        assert project_sources.value[0].id == "JUNCTION-9090"
        assert project_sources.value[0].source_type == SourceType.CONCEN
        assert project_sources.value[0].baseline_strength == "8330"
        assert project_sources.value[0].pattern_id == "Pattern-A"

        assert project_sources.value[1].id == "JUNCTION-9091"
        assert project_sources.value[1].source_type == SourceType.MASS
        assert project_sources.value[1].baseline_strength == "8331"
        assert project_sources.value[1].pattern_id == "Pattern-B"

        assert project_sources.value[2].id == "JUNCTION-9092"
        assert project_sources.value[2].source_type == SourceType.FLOWPACED
        assert project_sources.value[2].baseline_strength == "8332"
        assert project_sources.value[2].pattern_id == "Pattern-C"

        assert project_sources.value[3].id == "JUNCTION-9093"
        assert project_sources.value[3].source_type == SourceType.SETPOINT
        assert project_sources.value[3].baseline_strength == "8333"
        assert project_sources.value[3].pattern_id == "Pattern-D"

        assert project_sources.value[4].id == "JUNCTION-9094"
        assert project_sources.value[4].source_type == SourceType.CONCEN
        assert project_sources.value[4].baseline_strength == "8334"
        assert project_sources.value[4].pattern_id == ""

