import unittest
from core.swmm.options.backdrop import BackdropOptions
from core.swmm.inp_reader_sections import BackdropOptionsReader
from core.swmm.inp_writer_sections import BackdropOptionsWriter
from test.core.section_match import match


class SimpleBackdropTest(unittest.TestCase):
    """Test BACKDROP section"""

    def test_bare(self):
        """Test bare section"""
        test_text = ""
        my_options = BackdropOptionsReader.read(test_text)
        actual_text = BackdropOptionsWriter.as_text(my_options)
        # msg = '\nSet:'+test_text+'\nGet:'+actual_text
        # self.assertTrue(match(actual_text, test_text), msg)
        assert my_options.SECTION_NAME == "[BACKDROP]"
        assert my_options.offset == None
        assert my_options.scaling == None
        assert my_options.dimensions == (0.0, 0.0, 0.0, 0.0)

    def test_backdrop(self):
        """Test backdrop parameters"""
        test_text = """[BACKDROP]
        DIMENSIONS    0.0	  0.0	0.0	 0.0
         """
        my_options = BackdropOptionsReader.read(test_text)
        actual_text = BackdropOptionsWriter.as_text(my_options)
        msg = '\nSet:'+test_text+'\nGet:'+actual_text
        self.assertTrue(match(actual_text, test_text), msg)

    def test_missing_value(self):
        """Test on missing value"""
        test_text = """[BACKDROP]
        DIMENSIONS     0.0     0.0     0.0
         """
        my_options = BackdropOptionsReader.read(test_text)
        try:
            actual_text = BackdropOptionsWriter.as_text(my_options)
            msg = '\nSet missing value with:' + test_text + '\nGet:' + str(e)
            find_missing_value = False
        except Exception as e:
            msg = '\nSet missing value with:'+test_text+'\nGet:'+str(e)
            find_missing_value = True
        self.assertTrue(find_missing_value, msg)

def main():
    unittest.main()

if __name__ == "__main__":
    main()
