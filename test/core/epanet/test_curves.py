from core.inputfile import Section
from core.epanet import curves
from core.epanet.project import Project
import unittest


class SimpleCurveTest(unittest.TestCase):

    TEST_TEXT = ("[CURVES]",
                 ";ID\tX-Value\tY-Value",
                 ";--\t-------\t-------",
                 ";PUMP: Pump Curve for Pump 9",
                 " 1\t1500\t250\t")

    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_curve = curves.Curve()

    def setUp(self):
        self.my_curve = curves.Curve()
        self.my_curve.curve_id = "XXX"
        self.my_curve.description = "test curve"
        self.my_curve.curve_type = curves.CurveType.HEADLOSS
        self.my_curve.curve_xy = ((1500, 250), (1400, 200))

    def runTest(self):
        assert self.my_curve.curve_id == "XXX"
        assert self.my_curve.description == "test curve"
        assert self.my_curve.get_text().split() == [';HEADLOSS:', 'test', 'curve',
                                                    'XXX', '1500', '250', 'XXX', '1400', '200'], "incorrect pattern block"

        # Create new Project with this section populated from TEST_TEXT
        from_text = Project()
        from_text.set_text('\n'.join(self.TEST_TEXT))
        project_curves = from_text.curves
        assert Section.match_omit(project_curves.get_text(), '\n'.join(self.TEST_TEXT), " -;\t\n")

        assert len(project_curves.value) == 1
        this_curve = project_curves.value[0]
        assert this_curve.curve_id == '1'
        assert this_curve.description == "Pump Curve for Pump 9"
        assert this_curve.curve_type == curves.CurveType.PUMP
        assert this_curve.curve_xy == [("1500", "250")]

if __name__ == '__main__':
    my_test = SimpleCurveTest()
    my_test.setUp()
    my_test.runTest()
