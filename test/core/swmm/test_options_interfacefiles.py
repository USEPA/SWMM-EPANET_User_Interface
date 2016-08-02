import unittest
from core.inputfile import Section
from core.swmm.options import files


class OptionsInterfaceFilesTest(unittest.TestCase):
    """Test FILES options using the Section class"""

    def runTest(self):
        """Test files options"""
        self.my_options = files.Files()
        name = self.my_options.SECTION_NAME
        assert name == "[FILES]"

        actual_text = self.my_options.get_text()

        # Expect blank section when there are no contents for the section
        assert actual_text == ''

        self.my_options.save_outflows = "save_outflows.txt"

        expected_text = self.my_options.SECTION_NAME + '\n' + self.my_options.comment
        expected_text += "\nSAVE OUTFLOWS \tsave_outflows.txt"

        actual_text = self.my_options.get_text()
        assert match_omit(actual_text, expected_text, " \t-")


if __name__ == '__main__':
    my_test = OptionsInterfaceFilesTest()
    my_test.setUp()
    my_test.runTest()
