from core.swmm.hydrology.subcatchment import Subcatchment
import unittest


class SingleSubcatchmentTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def setUp(self):

        self.my_options = Subcatchment()

    def runTest(self):
        # Test one set of subcatchment parameters with spack
        test_subcatchment_all = r"""
SUB1               	RG1              	OT2               	5       	0       	140     0.05     	0           s1
        """
        # --Test set_text
        self.my_options.set_text(test_subcatchment_all)
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment_all)

        pass

        # Test one set of subcatchment parameters without spack
        # This should print fine
        test_subcatchment_wospack = r"""
SUB1               	RG1              	OT2               	5       	0       	140     	0.5     	0
        """
        # --Test set_text
        self.my_options.set_text(test_subcatchment_wospack)
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment_wospack)

        pass

        # Test one set of subcatchment parameters missing last two parameters Slope and Clength
        # This should report error
        test_subcatchment_partial = r"""
SUB1               	RG1              	OT2               	5       	0       	140
        """
        # --Test set_text
        self.my_options.set_text(test_subcatchment_partial)
        # --Test get_text through matches
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_subcatchment_partial)

        pass
