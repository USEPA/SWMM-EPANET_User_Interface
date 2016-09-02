import unittest
from core.epanet.options import reactions
from core.epanet.inp_reader_sections import ReactionsReader
from core.epanet.inp_writer_sections import ReactionsWriter
from test.core.section_match import match


class SimpleReactionsTest(unittest.TestCase):
    """Test Reaction section"""

    def test_get(self):
        """Test ReactionsWriter through match()"""
        my_reactions = reactions.Reactions()
        my_reactions.order_bulk = 1.1
        my_reactions.order_wall = 1.2
        my_reactions.order_tank = 1.3
        my_reactions.global_bulk = 2.1
        my_reactions.global_wall = 2.2
        my_reactions.limiting_potential = 0.1
        my_reactions.roughness_correlation = 0.2

        name = my_reactions.SECTION_NAME
        assert name == "[REACTIONS]"
        expected_text = "[REACTIONS]\n" \
            " Order Tank         	1.3\n" \
            " Global Wall        	2.2\n" \
            " Roughness Correlation	0.2\n" \
            " Limiting Potential 	0.1\n" \
            " Global Bulk        	2.1\n" \
            " Order Bulk         	1.1\n" \
            " Order Wall         	1.2"

        actual_text = ReactionsWriter.as_text(my_reactions)
        msg = '\nSet:'+expected_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

    def test_setget(self):
        """Test set_text and get_text"""
        test_text = "[REACTIONS]\n" \
            " Order Tank         	1.3\n" \
            " Global Wall        	2.2\n" \
            " Roughness Correlation	0.2\n" \
            " Limiting Potential 	0.1\n" \
            " Global Bulk        	2.1\n" \
            " Order Bulk         	1.1\n" \
            " Order Wall         	1.2"
        my_reactions = ReactionsReader.read(test_text)
        actual_text = ReactionsWriter.as_text(my_reactions)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()


