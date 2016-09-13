import unittest
from core.epanet.epanet_project import EpanetProject
from core.epanet.inp_reader_project import ProjectReader
from core.epanet.inp_writer_project import ProjectWriter
from core.epanet.inp_reader_sections import DemandReader
from core.epanet.inp_writer_sections import DemandWriter
from test.core.section_match import match, match_omit
from core.epanet.hydraulics.node import Demand


class SimpleDemandsTest(unittest.TestCase):
    """Test Demands section"""

    TEST_TEXT = ("[DEMANDS]",
                 ";ID  Demand Pattern Category",
                 ";---------------------------",
                 "JUNCTION-0 0.0 PATTERN-1",
                 "JUNCTION-1\t0.1\tPATTERN-2",
                 "JUNCTION-12 \t0.2 \tPATTERN-12 \tCategory-12")

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def runTest(self):
        """Test set_text and get_text of demand options"""
        source_text = '\n'.join(self.TEST_TEXT)
        section_from_text = self.project_reader.read_demands.read(source_text)
        actual_text = self.project_writer.write_demands.as_text(section_from_text)
        msg = '\nSet:' + source_text + '\nGet:' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

        project_demands = section_from_text
        assert project_demands.value[0].junction_name == "JUNCTION-0"
        assert project_demands.value[0].base_demand == "0.0"
        assert project_demands.value[0].demand_pattern == "PATTERN-1"
        assert project_demands.value[0].category == ''

        assert project_demands.value[1].junction_name == "JUNCTION-1"
        assert project_demands.value[1].base_demand == "0.1"
        assert project_demands.value[1].demand_pattern == "PATTERN-2"
        assert project_demands.value[1].category == ''

        assert project_demands.value[2].junction_name == "JUNCTION-12"
        assert project_demands.value[2].base_demand == "0.2"
        assert project_demands.value[2].demand_pattern == "PATTERN-12"
        assert project_demands.value[2].category == "Category-12"

def main():
    unittest.main()

if __name__ == "__main__":
    main()