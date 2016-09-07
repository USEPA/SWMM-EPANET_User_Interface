import unittest
from core.swmm.swmm_project import SwmmProject
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from core.swmm.inp_reader_sections import GeneralReader
from core.swmm.inp_writer_sections import GeneralWriter
from test.core.section_match import match, match_omit
from core.swmm.options.files import Files


class SimpleFilesTest(unittest.TestCase):
    """Test FILES section"""

    def test_default(self):
        """Test default"""
        #20160407xw: if default, all nones, therefore no text
        my_options = Files()
        name = my_options.SECTION_NAME
        assert name == "[FILES]"
        actual_text = GeneralWriter.as_text(my_options)
        assert actual_text == ""

    def test_space_delimited(self):
        """normal space delimited keyword and parameter"""
        test_text = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "USE RAINFALL use_rainfall.txt"
        my_options = GeneralReader.read(test_text)
        actual_text = GeneralWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

        assert self.my_options.use_rainfall == "use_rainfall.txt"
        assert self.my_options.save_rainfall is None
        assert self.my_options.save_outflows is None

    def test_more_space(self):
        """Test more spaces beyond [:19]"""
        test_text = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "SAVE OUTFLOWS                   save_outflows.txt"
        my_options = GeneralReader.read(test_text)
        actual_text = GeneralWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)
        assert self.my_options.use_rainfall is None
        assert self.my_options.save_outflows == "save_outflows.txt"
        assert self.my_options.matches(test_text)

    def test_space_in_filename(self):
        """Test space in file name """
        test_text = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "SAVE OUTFLOWS                   save outflows.txt"
        my_options = GeneralReader.read(test_text)
        actual_text = GeneralWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

        assert self.my_options.use_rainfall is None
        assert self.my_options.save_outflows == "save outflows.txt"  # ---Space in file name

    def test_filename_with_path(self):
        """Test filename with path"""
        test_text = "[FILES]\n"\
                    ";;Interfacing Files\n"\
                    "SAVE OUTFLOWS   .\My Documents\save_outflows.txt"
        my_options = GeneralReader.read(test_text)
        actual_text = GeneralWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

        assert self.my_options.use_rainfall is None
        assert self.my_options.save_outflows == ".\My Documents\save_outflows.txt"


    def test_all_options(self):
        """Test all options of FILE section"""
        my_options = Files()
        test_text = """
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
        my_options = GeneralReader.read(test_text)
        actual_text = GeneralWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

        assert my_options.use_rainfall == "rainfall_u.txt"
        assert my_options.save_rainfall is None
        assert my_options.use_runoff == "runoff_u.txt"
        assert my_options.save_runoff is None
        assert my_options.use_hotstart == "hotstart_u.txt"
        assert my_options.save_hotstart == "hotstart_s.txt"
        assert my_options.use_rdii == "rdii_u.txt"
        assert my_options.save_rdii is None
        assert my_options.use_inflows == "inflows_u.txt"
        assert my_options.save_outflows == "outflows_s.txt"

    def test_interface_files(self):
        """Test FILES options using the Section class"""
        my_options = Files()
        name = my_options.SECTION_NAME
        assert name == "[FILES]"
        actual_text = GeneralWriter.as_text(my_options)

        # Expect blank section when there are no contents for the section
        assert actual_text == ''

        my_options.save_outflows = "save_outflows.txt"
        expected_text = my_options.SECTION_NAME + '\n' + my_options.comment
        expected_text += "\nSAVE OUTFLOWS \tsave_outflows.txt"

        my_options = GeneralReader.read(expected_text)
        actual_text = GeneralWriter.as_text(my_options)
        msg = '\nSet:'+expected_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, expected_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()