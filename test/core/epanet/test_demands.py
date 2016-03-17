from core.inputfile import Section
from core.epanet.project import Project
from core.epanet.hydraulics.node import Demand
import unittest


class SimpleDemandsTest(unittest.TestCase):

    TEST_TEXT = ("[DEMANDS]",
                 ";ID  Demand Pattern Category",
                 ";---------------------------",
                 "JUNCTION-0 0.0 PATTERN-1",
                 "JUNCTION-1\t0.1\tPATTERN-2",
                 "JUNCTION-12 \t0.2 \tPATTERN-12 \tCategory-12")

    def runTest(self):
        from_text = Project()
        source_text = '\n'.join(self.TEST_TEXT)
        from_text.set_text(source_text)
        project_demands = from_text.demands

        assert Section.match_omit(project_demands.get_text(), source_text, " \t-;\n")

        assert project_demands.value[0].junction_id == "JUNCTION-0"
        assert project_demands.value[0].base_demand == "0.0"
        assert project_demands.value[0].demand_pattern == "PATTERN-1"
        assert project_demands.value[0].category == ''

        assert project_demands.value[1].junction_id == "JUNCTION-1"
        assert project_demands.value[1].base_demand == "0.1"
        assert project_demands.value[1].demand_pattern == "PATTERN-2"
        assert project_demands.value[1].category == ''

        assert project_demands.value[2].junction_id == "JUNCTION-12"
        assert project_demands.value[2].base_demand == "0.2"
        assert project_demands.value[2].demand_pattern == "PATTERN-12"
        assert project_demands.value[2].category == "Category-12"
