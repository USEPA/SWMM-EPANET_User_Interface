from core.swmm.hydraulics.node import RDIInflow
import unittest


class SingleRDIITest(unittest.TestCase):

    def setUp(self):

        self.my_options = RDIInflow()

    def runTest(self):

        # Test example created based on SWMM 5.1 manual
        test_text = r"""NODE2  UHGROUP1 12.0 """
        # --Test set_text
        self.my_options.set_text(test_text)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_text)


        pass

class MultiRDIIsTest(unittest.TestCase):

    def setUp(self):

        self.my_options = RDIInflow()

    def runTest(self):

        test_text = r"""
[RDII]
;;Node             UHgroup          SewerArea
;;----------------------------------------------------------------------
  80408            FLOW             80408
  81009            FLOW             81009
  82309            FLOW             82309
        """
        # --Test set_text


        pass