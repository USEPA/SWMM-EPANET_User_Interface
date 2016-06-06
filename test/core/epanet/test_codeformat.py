import os
import unittest
import pycodestyle
import inspect

class TestCodeFormat(unittest.TestCase):

    def runTest(self):
        """Test that we conform to PEP-8."""

        # Get Python code directory
        directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))
        source_root_path = os.path.split(os.path.split(os.path.split(directory)[0])[0])[0]
        pycode_path = os.path.join(source_root_path, "src", "core", "epanet", "options")

        # Check formats
        style = pycodestyle.StyleGuide(quiet=True)
        # style.input_dir(pycode_path)
        result = style.check_files([pycode_path])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

if __name__ == '__main__':
    pstyle = TestCodeFormat()
    pstyle.runTest()