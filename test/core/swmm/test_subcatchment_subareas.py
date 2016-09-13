import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match


class SubAreasTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)

    def runTest(self):

        # Test aquifer parameters in Example 5
        test_subarea = r"""
[SUBAREAS]
;;Subcatchment  	N-Imperv  	N-Perv    	S-Imperv  	S-Perv    	PctZero   	RouteTo   	PctRouted
;;--------------	----------	----------	----------	----------	----------	----------	----------
1               	0.01      	0.1       	0.05      	0.05      	25        	OUTLET
"""
        # --Test set_text
        self.my_options = SubareasReader.read(test_subarea)
        # --Test get_text through matches
        actual_text = SubareaWriter.as_text(self.my_options) # display purpose
        assert match(actual_text, test_subarea)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
