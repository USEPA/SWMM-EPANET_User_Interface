from core.epanet import curves
import unittest


class SimpleCurveTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_curve = curves.Curve

    def setUp(self):
        self.my_curve = curves.Curve()
        self.my_curve.curve_id = "XXX"
        self.my_curve.description = "test curve"
        self.my_curve.curve_type = curves.CurveType.HEAD_LOSS
        self.my_curve.curve_xy = ((1500, 250), (1400, 200))

    def runTest(self):
        assert self.my_curve.curve_id == "XXX"
        assert self.my_curve.description == "test curve"
        assert self.my_curve.get_text() == 'XXX	1.0	1.1	1.2	1.3', 'incorrect pattern block'
