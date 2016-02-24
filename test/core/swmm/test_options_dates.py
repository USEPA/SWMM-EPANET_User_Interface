from core.swmm.options.dates import Dates
from core.swmm.options import dates
import unittest


class  OptionsDatesTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = Dates()

    def setUp(self):

        self.my_options = dates.Dates()


    def runTest(self):

        name = self.my_options.SECTION_NAME
        assert name == "[OPTIONS]"

        expected_text = "[OPTIONS]\n" + \
                        " END_TIME           	24:00\n" + \
                        " END_DATE           	1/1/2002\n" + \
                        " SWEEP_END          	12/31\n" + \
                        " START_TIME         	0:00\n" + \
                        " REPORT_START_TIME  	0:00\n" + \
                        " START_DATE         	1/1/2002\n" + \
                        " SWEEP_START        	1/1\n" + \
                        " REPORT_START_DATE  	1/1/2002"

        actual_text = self.my_options.get_text()
        assert actual_text == expected_text
