from core.epanet import patterns
import unittest


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
        assert self.my_pattern.get_text() == 'XXX	1.0	1.1	1.2	1.3', 'incorrect pattern block'
