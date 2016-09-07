import unittest
# from core.inputfile import Section
from core.swmm.options import files
from core.swmm.inp_reader_sections import GeneralReader
from core.swmm.inp_writer_sections import GeneralWriter
from test.core.section_match import match


class OptionsInterfaceFilesTest(unittest.TestCase):
    """Test FILES options using the Section class"""

    def runTest(self):
        """Test files options"""
        my_options = files.Files()
        name = my_options.SECTION_NAME
        assert name == "[FILES]"

        actual_text = GeneralWriter.as_text(my_options)
        # Expect blank section when there are no contents for the section
        assert actual_text == ''

        my_options.save_outflows = "save_outflows.txt"

        expected_text = my_options.SECTION_NAME + '\n' + my_options.comment
        expected_text += "\nSAVE OUTFLOWS \tsave_outflows.txt"

        actual_text = GeneralWriter.as_text(expected_text)
        msg = '\nSet:' + expected_text + '\nGet:' + actual_text
        msg += "xw: FilesReader is commented out in inp_reader_project"
        self.assertTrue(match(actual_text, expected_text), msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()

# if __name__ == '__main__':
#     my_test = OptionsInterfaceFilesTest()
#     my_test.setUp()
#     my_test.runTest()
