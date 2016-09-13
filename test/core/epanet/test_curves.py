import unittest
from core.epanet.epanet_project import EpanetProject
from core.epanet.inp_reader_project import ProjectReader
from core.epanet.inp_writer_project import ProjectWriter
from core.epanet.inp_reader_sections import CurveReader
from core.epanet.inp_writer_sections import CurveWriter
from test.core.section_match import match, match_omit
from core.epanet import curves


class SimpleCurveTest(unittest.TestCase):
    """Test Curves section"""

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_curve(self):
        """Test one curve line"""
        test_text = "C1 0 200"
        my_options = CurveReader.read(test_text)
        actual_text = CurveWriter.as_text(my_options)
        msg = '\nSet:\n' + test_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        my_curve = curves.Curve()
        my_curve.name = "XXX"
        my_curve.description = "test curve"
        my_curve.curve_type = curves.CurveType.HEADLOSS
        my_curve.curve_xy = ((1500, 250), (1400, 200))

        actual_text = CurveWriter.as_text(my_curve)

        assert actual_text.split() == [';HEADLOSS:', 'test', 'curve',
                                       'XXX', '1500', '250', 'XXX', '1400', '200'], "incorrect pattern block"

    def test_curves(self):
        """Test Curves section"""

        # Create new project with new text
        test_text = ("[CURVES]",
                       ";ID\tX-Value\tY-Value",
                       ";--\t-------\t-------",
                       ";PUMP: Pump Curve for Pump 9",
                       " 1\t1500\t250\t")
        source_text = "\n".join(test_text)
        section_from_text = self.project_reader.read_curves.read(source_text)
        actual_text = self.project_writer.write_curves.as_text(section_from_text)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

        project_curves = section_from_text
        assert len(project_curves.value) == 1
        this_curve = project_curves.value[0]
        assert this_curve.name == '1'
        assert this_curve.description == "Pump Curve for Pump 9"
        assert this_curve.curve_type == curves.CurveType.PUMP
        assert this_curve.curve_xy == [("1500", "250")]

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# if __name__ == '__main__':
#     my_test = SimpleCurveTest()
#     my_test.setUp()
#     my_test.test_curve()
#     my_test.test_curves()
