import unittest
from core.inputfile import Section
from core.swmm.options.files import Files


class SimpleFilesTest(unittest.TestCase):
    """Test FILES section"""

    def test_default(self):
        """Test default"""
        #20160407xw: if default, all nones, therefore no text
        self.my_options = Files()
        name = self.my_options.SECTION_NAME
        assert name == "[FILES]"
        actual_text = self.my_options.get_text()
        assert actual_text == ""

    def test_space_delimited(self):
        """normal space delimited keyword and parameter"""
        self.my_options = Files()
        TEST_TEXT = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "USE RAINFALL use_rainfall.txt"
        self.my_options.set_text(TEST_TEXT)
        assert self.my_options.use_rainfall == "use_rainfall.txt"
        assert self.my_options.save_rainfall is None
        assert self.my_options.save_outflows is None
        assert self.my_options.matches(TEST_TEXT)

    def test_more_space(self):
        """Test more spaces beyond [:19]"""
        self.my_options = Files()
        TEST_TEXT = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "SAVE OUTFLOWS                   save_outflows.txt"
        self.my_options.set_text(TEST_TEXT)
        assert self.my_options.use_rainfall is None
        assert self.my_options.save_outflows == "save_outflows.txt"
        assert self.my_options.matches(TEST_TEXT)

    def test_space_in_filename(self):
        """Test space in file name """
        self.my_options = Files()
        TEST_TEXT = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "SAVE OUTFLOWS                   save outflows.txt"
        self.my_options.set_text(TEST_TEXT)
        assert self.my_options.use_rainfall is None
        assert self.my_options.save_outflows == "save outflows.txt"  # ---Space in file name
        assert self.my_options.matches(TEST_TEXT)

    def test_filename_with_path(self):
        """Test filename with path"""
        self.my_options = Files()
        TEST_TEXT = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "SAVE OUTFLOWS   .\My Documents\save_outflows.txt"
        self.my_options.set_text(TEST_TEXT)
        assert self.my_options.use_rainfall is None
        assert self.my_options.save_outflows == ".\My Documents\save_outflows.txt"
        assert self.my_options.matches(TEST_TEXT)

    def test_all_options(self):
        """Test all options of FILE section"""
        self.my_options = Files()
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
        assert self.my_options.save_rainfall is None
        assert self.my_options.use_runoff == "runoff_u.txt"
        assert self.my_options.save_runoff is None
        assert self.my_options.use_hotstart == "hotstart_u.txt"
        assert self.my_options.save_hotstart == "hotstart_s.txt"
        assert self.my_options.use_rdii == "rdii_u.txt"
        assert self.my_options.save_rdii is None
        assert self.my_options.use_inflows == "inflows_u.txt"
        assert self.my_options.save_outflows == "outflows_s.txt"

        assert self.my_options.matches(test_all_opts)
        actual_text = self.my_options.get_text()
        self.my_options.set_text(actual_text)
        assert self.my_options.matches(test_all_opts)

    def test_interface_files(self):
        """Test FILES options using the Section class"""
        self.my_options = Files()
        name = self.my_options.SECTION_NAME
        assert name == "[FILES]"

        actual_text = self.my_options.get_text()

        # Expect blank section when there are no contents for the section
        assert actual_text == ''

        self.my_options.save_outflows = "save_outflows.txt"

        expected_text = self.my_options.SECTION_NAME + '\n' + self.my_options.comment
        expected_text += "\nSAVE OUTFLOWS \tsave_outflows.txt"

        actual_text = self.my_options.get_text()
        assert Section.match_omit(actual_text, expected_text, " \t-")

