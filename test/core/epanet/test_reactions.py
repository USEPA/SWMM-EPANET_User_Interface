import unittest
from core.epanet.options import reactions


class SimpleReactionsTest(unittest.TestCase):
    """Test Reaction section"""

    def test_get(self):
        """Test get_text through matches()"""
        self.my_reactions = reactions.Reactions()
        self.my_reactions.order_bulk = 1.1
        self.my_reactions.order_wall = 1.2
        self.my_reactions.order_tank = 1.3
        self.my_reactions.global_bulk = 2.1
        self.my_reactions.global_wall = 2.2
        self.my_reactions.limiting_potential = 0.1
        self.my_reactions.roughness_correlation = 0.2

        name = self.my_reactions.SECTION_NAME
        assert name == "[REACTIONS]"
        expected_text = "[REACTIONS]\n" \
            " Order Tank         	1.3\n" \
            " Global Wall        	2.2\n" \
            " Roughness Correlation	0.2\n" \
            " Limiting Potential 	0.1\n" \
            " Global Bulk        	2.1\n" \
            " Order Bulk         	1.1\n" \
            " Order Wall         	1.2"

        assert self.my_reactions.matches(expected_text)

    def test_setget(self):
        """Test set_text and get_text"""
        self.my_reactions = reactions.Reactions()
        test_text = "[REACTIONS]\n" \
            " Order Tank         	1.3\n" \
            " Global Wall        	2.2\n" \
            " Roughness Correlation	0.2\n" \
            " Limiting Potential 	0.1\n" \
            " Global Bulk        	2.1\n" \
            " Order Bulk         	1.1\n" \
            " Order Wall         	1.2"
        self.my_reactions.set_text(test_text)
        assert self.my_reactions.matches(test_text)


