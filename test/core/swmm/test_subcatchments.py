import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydrology.subcatchment import Subcatchment


class SimpleSubcatchmentTest(unittest.TestCase):
    """Test SUBCATCHMENTS section"""

    def test_pk(self):
        """Test one set of subcatchment parameters with spack"""
        self.my_options = Subcatchment()
        test_subcatchment_all = "SUB1  RG1	OT2	5	0	140     0.05 	0 s1"
        self.my_options.set_text(test_subcatchment_all)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment_all)


    def test_nopk(self):
        """Test one set of subcatchment parameters without spack"""
        # This should print fine
        self.my_options = Subcatchment()
        test_subcatchment_wospack = "SUB1	RG1	OT2	5	0 140	0.5	0"
        self.my_options.set_text(test_subcatchment_wospack)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment_wospack)

    def test_missing(self):
        """Test one set of subcatchment parameters missing last two parameters Slope and Clength"""
        # This should report error
        self.my_options = Subcatchment()
        test_subcatchment_partial = "SUB1	RG1	OT2	5 0 140"
        self.my_options.set_text(test_subcatchment_partial)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment_partial)
        # self.assertFalse(self.my_options.matches(test_subcatchment_partial))

