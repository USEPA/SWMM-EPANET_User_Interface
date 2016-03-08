from core.epanet import patterns
from core.epanet.project import Project
from core.inputfile import Section
import unittest

TEST_TEXT = ("[PATTERNS]",
             ";ID\tMultipliers",
             ";Demand Pattern",
             " 1\t1.0\t1.2\t1.4\t1.6\t1.4\t1.2",
             " 1\t1.0\t0.8\t0.6\t0.4\t0.6\t0.8",
             " 2\t2.0\t2.2\t2.4\t2.6\t2.4\t2.2",
             " 2\t2.0\t2.8\t2.6\t2.4\t2.6\t2.8")

class SimplePatternTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_pattern = patterns.Pattern()

    def setUp(self):
        self.my_pattern = patterns.Pattern()
        self.my_pattern.description = "test pattern"
        self.my_pattern.pattern_id = "XXX"
        self.my_pattern.multipliers = ("1.0", "1.1", "1.2", "1.3")

    def runTest(self):
        assert self.my_pattern.pattern_id == "XXX"
        assert self.my_pattern.description == "test pattern"
        assert self.my_pattern.get_text().split() == ["XXX", "1.0", "1.1", "1.2", "1.3"], "incorrect pattern block"

        # Create new Project with this section populated from TEST_TEXT
        from_text = Project()
        from_text.set_text('\n'.join(TEST_TEXT))
        pattern_list = from_text.patterns.value[2:]  # Skip first two in list, they are comments
        assert len(pattern_list) == 4
        assert int(pattern_list[0].pattern_id) == 1
        assert int(pattern_list[1].pattern_id) == 1
        assert int(pattern_list[2].pattern_id) == 2
        assert int(pattern_list[3].pattern_id) == 2

        assert float(pattern_list[0].multipliers[0]) == 1.0
        assert float(pattern_list[0].multipliers[1]) == 1.2
        assert float(pattern_list[0].multipliers[2]) == 1.4
        assert float(pattern_list[0].multipliers[3]) == 1.6
        assert float(pattern_list[0].multipliers[4]) == 1.4
        assert float(pattern_list[0].multipliers[5]) == 1.2

        assert float(pattern_list[1].multipliers[0]) == 1.0
        assert float(pattern_list[1].multipliers[1]) == 0.8
        assert float(pattern_list[1].multipliers[2]) == 0.6
        assert float(pattern_list[1].multipliers[3]) == 0.4
        assert float(pattern_list[1].multipliers[4]) == 0.6
        assert float(pattern_list[1].multipliers[5]) == 0.8

        assert float(pattern_list[2].multipliers[0]) == 2.0
        assert float(pattern_list[2].multipliers[1]) == 2.2
        assert float(pattern_list[2].multipliers[2]) == 2.4
        assert float(pattern_list[2].multipliers[3]) == 2.6
        assert float(pattern_list[2].multipliers[4]) == 2.4
        assert float(pattern_list[2].multipliers[5]) == 2.2

        assert float(pattern_list[3].multipliers[0]) == 2.0
        assert float(pattern_list[3].multipliers[1]) == 2.8
        assert float(pattern_list[3].multipliers[2]) == 2.6
        assert float(pattern_list[3].multipliers[3]) == 2.4
        assert float(pattern_list[3].multipliers[4]) == 2.6
        assert float(pattern_list[3].multipliers[5]) == 2.8

if __name__ == '__main__':
    my_test = SimplePatternTest()
    my_test.setUp()
    my_test.runTest()
