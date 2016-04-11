from core.swmm.options.files import Files
from core.swmm.options import files
import unittest

class OptionsFilesTest(unittest.TestCase):

    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_options = Files()

    def setUp(self):

        self.my_options = files.Files()


    def runTest(self):

        name = self.my_options.SECTION_NAME
        assert name == "[FILES]"

        #20160407xw: if default, all nones, therefore no text
        actual_text = self.my_options.get_text()
        assert actual_text == ""

        # 20160408xw: Test set_text:
        # ---normal space delimited keyword and parameter
        TEST_TEXT = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "USE RAINFALL use_rainfall.txt"
        self.my_options.set_text(TEST_TEXT)
        assert self.my_options.use_rainfall == "use_rainfall.txt"
        assert self.my_options.save_rainfall is None
        assert self.my_options.save_outflows is None
        assert self.my_options.matches(TEST_TEXT)
        actual_text = self.my_options.get_text()

        # More spaces beyond [:19]
        TEST_TEXT = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "SAVE OUTFLOWS                   save_outflows.txt"
        self.my_options.set_text(TEST_TEXT)
        assert self.my_options.use_rainfall is None
        assert self.my_options.save_outflows == "save_outflows.txt"
        assert self.my_options.matches(TEST_TEXT)
        actual_text = self.my_options.get_text()

        # Space in file name
        TEST_TEXT = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "SAVE OUTFLOWS                   save outflows.txt"
        self.my_options.set_text(TEST_TEXT)
        assert self.my_options.use_rainfall is None
        assert self.my_options.save_outflows == "save outflows.txt"  # ---Space in file name
        assert self.my_options.matches(TEST_TEXT)
        actual_text = self.my_options.get_text()

        #---Filename with path
        TEST_TEXT = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "SAVE OUTFLOWS   .\My Documents\save_outflows.txt"
        self.my_options.set_text(TEST_TEXT)
        assert self.my_options.use_rainfall is None
        assert self.my_options.save_outflows == ".\My Documents\save_outflows.txt"
        assert self.my_options.matches(TEST_TEXT)
        actual_text = self.my_options.get_text()

        #---Test all options
        test_all_opts = """
[FILES]
;;Interfacing Files
USE RAINFALL rainfall_u.txt
USE RUNOFF runoff_u.txt
USE RDII rdii_u.txt
USE HOTSTART hotstart_u.txt
SAVE HOTSTART hotstart_s.txt
USE INFLOWS inflows_u.txt
SAVE OUTFLOWS outflows_s.txt
"""
        self.my_options.set_text(test_all_opts)
        assert self.my_options.use_rainfall == "rainfall_u.txt"
        assert self.my_options.save_rainfall == None
        assert self.my_options.use_runoff == "runoff_u.txt"
        assert self.my_options.save_runoff == None
        assert self.my_options.use_hotstart == "hotstart_u.txt"
        assert self.my_options.save_hotstart == "hotstart_s.txt"
        assert self.my_options.use_rdii == "rdii_u.txt"
        assert self.my_options.save_rdii == None
        assert self.my_options.use_inflows == "inflows_u.txt"
        assert self.my_options.save_outflows == "outflows_s.txt"

        assert self.my_options.matches(test_all_opts)
        actual_text = self.my_options.get_text()
        self.my_options.set_text(actual_text)
        assert self.my_options.matches(test_all_opts)

        # 20160407xw: if all assigned with a file name, text in [:19]\t format
        # with tab formatting
        expected_text = "[FILES]\n" + \
                        ";;Interfacing Files\n"\
                        " USE RAINFALL       \tuse_rainfall\n"\
                        " SAVE RAINFALL      \tsave_rainfall\n"\
                        " USE RUNOFF         \tuse_runoff\n"\
                        " SAVE RUNOFF        \tsave_runoff\n"\
                        " USE HOTSTART       \tuse_hotstart\n"\
                        " SAVE HOTSTART      \tsave_hotstart\n"\
                        " USE RDII           \tuse_rdii\n"\
                        " SAVE RDII	         \tsave_rdii\n"\
                        " USE INFLOWS        \tuse_inflows\n"\
                        " SAVE OUTFLOWS	     \tsave_outflows"

        self.my_options.set_text(expected_text)
        self.my_options.use_rainfall = "use_rainfall"
        self.my_options.save_rainfall = "save_rainfall"
        self.my_options.use_runoff = "use_runoff"
        self.my_options.save_runoff = "save_runoff"
        self.my_options.use_hotstart = "use_hotstart"
        self.my_options.save_hotstart = "save_hotstart"
        self.my_options.use_rdii = "use_rdii"
        self.my_options.save_rdii = "save_rdii"
        self.my_options.use_inflows = "use_inflows"
        self.my_options.save_outflows = "save_outflows"
        assert self.my_options.matches(expected_text)
        actual_text = self.my_options.get_text()
        self.my_options.set_text(actual_text)
        assert self.my_options.matches(expected_text)

        #--20160411 xw tests on get, set, defaults passed
        #-- However, 5.1 requires that Rainfall, Runoff, and RDII files can either be used or saved, not both
        #-- Not implemented in current code.



