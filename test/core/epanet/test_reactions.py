from core.epanet.options.options import Options
from core.epanet.options import reactions
import unittest


class SimpleReactionsTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = Options()

    def setUp(self):

        self.my_reactions = reactions.Reactions()
        self.my_reactions.order_bulk = 1.1
        self.my_reactions.order_wall = 1.2
        self.my_reactions.order_tank = 1.3
        self.my_reactions.global_bulk = 2.1
        self.my_reactions.global_wall = 2.2
        self.my_reactions.limiting_potential = 0.1
        self.my_reactions.roughness_correlation = 0.2

    def runTest(self):

        name = self.my_reactions.SECTION_NAME
        assert name == "[REACTIONS]"
        expected_text = "[REACTIONS]\n" \
            " Order Tank         	1.2\n" \
            " Global Wall        	2.2\n" \
            " Roughness Correlation	0.2\n" \
            " Limiting Potential 	0.1\n" \
            " Global Bulk        	2.1\n" \
            " Order Bulk         	1.1\n" \
            " Order Wall         	1.3"

        actual_text = self.my_reactions.get_text()
        assert actual_text == expected_text
