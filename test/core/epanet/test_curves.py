import unittest
from core.inputfile import Section
from core.epanet import curves
from core.epanet.project import Project


class SimpleCurveTest(unittest.TestCase):
    """Test Curves section"""

    def test_curve(self):
        """Test one curve line"""
        self.my_options = curves.Curve()
        test_text = "C1 0 200"
        self.my_options.set_text(test_text)
        actual_text = self.my_options.get_text()
        assert self.my_options.matches(test_text)

    def test_curves(self):
        """Test Curves section"""
        self.my_curve = curves.Curve()
        self.my_curve = curves.Curve()
        self.my_curve.curve_id = "XXX"
        self.my_curve.description = "test curve"
        self.my_curve.curve_type = curves.CurveType.HEADLOSS
        self.my_curve.curve_xy = ((1500, 250), (1400, 200))

        assert self.my_curve.curve_id == "XXX"
        assert self.my_curve.description == "test curve"
        assert self.my_curve.get_text().split() == [';HEADLOSS:', 'test', 'curve',
                                                    'XXX', '1500', '250', 'XXX', '1400', '200'], "incorrect pattern block"

        # Create new project with new text
        test_text = ("[CURVES]",
                     ";ID\tX-Value\tY-Value",
                     ";--\t-------\t-------",
                     ";PUMP: Pump Curve for Pump 9",
                     " 1\t1500\t250\t")
        from_text = Project()
        from_text.set_text('\n'.join(test_text))
        project_curves = from_text.curves
        assert Section.match_omit(project_curves.get_text(), '\n'.join(test_text), " -;\t\n")

        assert len(project_curves.value) == 1
        this_curve = project_curves.value[0]
        assert this_curve.curve_id == '1'
        assert this_curve.description == "Pump Curve for Pump 9"
        assert this_curve.curve_type == curves.CurveType.PUMP
        assert this_curve.curve_xy == [("1500", "250")]

if __name__ == '__main__':
    my_test = SimpleCurveTest()
    my_test.setUp()
    my_test.test_curve()
    my_test.test_curves()
