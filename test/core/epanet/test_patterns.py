from core.epanet import patterns
from core.epanet.project import Project
import unittest


class SimplePatternTest2(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):
        self.my_options = patterns.Pattern()

    def runTest(self):

        # Test created based on manual
        # Multiple lines
        # set_text takes input test_text
        # get_text writes output actual_text
        # will rewrite string to three rows each with 6, 6, 3 numbers.
        # So to compare I stripped P1, space, and \n
        test_text = "P1\t1.2\t1.4\t1.6\t1.8\t2.0\n" \
                    "P1\t2.2\t2.4\t2.6\t2.8\t3.0\n" \
                    "P1\t3.2\t3.4\t3.6\t3.8\t4.0"
        self.my_options.set_text(test_text)
        new_test = test_text.replace(' ','').replace('\n','').replace('P1','')
        actual_text = self.my_options.get_text().replace(' ','').replace('\n','').replace('P1','')
        self.assertEquals(actual_text,new_test)
        pass


class SimplePatternTest(unittest.TestCase):

    TEST_TEXT = ("[PATTERNS]",
                 ";ID\tMultipliers",
                 ";Demand Pattern",
                 " 1\t1.0\t1.2\t1.4\t1.6\t1.4\t1.2",
                 " 1\t1.0\t0.8\t0.6\t0.4\t0.6\t0.8",
                 " 2\t2.0\t2.2\t2.4\t2.6\t2.4\t2.2",
                 " 2\t2.0\t2.8\t2.6\t2.4\t2.6\t2.8")

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
        assert self.my_pattern.get_text().split() == [";test", "pattern", "XXX", "1.0", "1.1", "1.2", "1.3"], "get_text"

        # Create new Project with this section populated from TEST_TEXT
        from_text = Project()
        from_text.set_text('\n'.join(SimplePatternTest.TEST_TEXT))
        pattern_list = from_text.patterns.value
        assert len(pattern_list) == 2
        assert int(pattern_list[0].pattern_id) == 1
        assert int(pattern_list[1].pattern_id) == 2

        assert float(pattern_list[0].multipliers[0]) == 1.0
        assert float(pattern_list[0].multipliers[1]) == 1.2
        assert float(pattern_list[0].multipliers[2]) == 1.4
        assert float(pattern_list[0].multipliers[3]) == 1.6
        assert float(pattern_list[0].multipliers[4]) == 1.4
        assert float(pattern_list[0].multipliers[5]) == 1.2

        assert float(pattern_list[0].multipliers[6]) == 1.0
        assert float(pattern_list[0].multipliers[7]) == 0.8
        assert float(pattern_list[0].multipliers[8]) == 0.6
        assert float(pattern_list[0].multipliers[9]) == 0.4
        assert float(pattern_list[0].multipliers[10]) == 0.6
        assert float(pattern_list[0].multipliers[11]) == 0.8

        assert float(pattern_list[1].multipliers[0]) == 2.0
        assert float(pattern_list[1].multipliers[1]) == 2.2
        assert float(pattern_list[1].multipliers[2]) == 2.4
        assert float(pattern_list[1].multipliers[3]) == 2.6
        assert float(pattern_list[1].multipliers[4]) == 2.4
        assert float(pattern_list[1].multipliers[5]) == 2.2

        assert float(pattern_list[1].multipliers[6]) == 2.0
        assert float(pattern_list[1].multipliers[7]) == 2.8
        assert float(pattern_list[1].multipliers[8]) == 2.6
        assert float(pattern_list[1].multipliers[9]) == 2.4
        assert float(pattern_list[1].multipliers[10]) == 2.6
        assert float(pattern_list[1].multipliers[11]) == 2.8

if __name__ == '__main__':
    my_test = SimplePatternTest()
    my_test.setUp()
    my_test.runTest()

    my_test = SimplePatternTest2()
    my_test.setUp()
    my_test.runTest()

