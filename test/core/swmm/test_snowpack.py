import unittest
from core.swmm.inp_reader_sections import SnowPackReader
from core.swmm.inp_writer_sections import SnowPackWriter
from core.swmm.hydrology.snowpack import SnowPack
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit


class SimpleSnowPackTest(unittest.TestCase):
    """Test snowpack section"""
    TEST_TEXTS = [r"""
;;Name           Surface    Parameters
;;-------------- ---------- ----------
s                PLOWABLE   0.001      0.001      32.0       0.10       0.00       0.00       0.0
s                IMPERVIOUS 0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                PERVIOUS   0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0        w
        """]
    SOURCE_TEXTS =[r"""
[SNOWPACKS]
;;Name           Surface    Parameters
;;-------------- ---------- ----------
sno              PLOWABLE   0.001      0.001      32.0       0.10       0.00       0.00       0.0
sno              IMPERVIOUS 0.001      0.001      32.0       0.10       0.00       0.00       0.00
sno              PERVIOUS   0.001      0.001      32.0       0.10       0.00       0.00       0.00
sno              REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0
s                PLOWABLE   0.001      0.001      32.0       0.10       0.00       0.00       0.0
s                IMPERVIOUS 0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                PERVIOUS   0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0        w
        """]
    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def test_one_pack(self):
        """Test one snow pack
        snow parameters from Example 1h, examined according to SWMM 5.1 manual
        # Modified on test purposes
        # This test passed for an individual snowpack parameter set
        # Case 1: test all snowpack surface types"""
        for test_text in self.TEST_TEXTS:
            my_options = SnowPackReader.read(test_text)
            actual_text = SnowPackWriter.as_text(my_options)
            msg = '\nSet:'+test_text+'\nGet:'+actual_text
            self.assertTrue(match(actual_text, test_text), msg)

    def test_one_type(self):
        """test only one type"""
        test_snowpack_removal = r"""
        ;;Name           Surface    Parameters
        ;;-------------- ---------- ----------
        s                REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0        w
                """
        for test_text in [test_snowpack_removal]:
            my_options = SnowPackReader.read(test_text)
            actual_text = SnowPackWriter.as_text(my_options)
            msg = '\nSet:'+test_text+'\nGet:'+actual_text
            self.assertTrue(match(actual_text, test_text), msg)

    def test_snowpacks_section(self):
        """Test SNOWPACKS section"""
        for source_text in self.SOURCE_TEXTS:
            section_from_text = self.project_reader.read_snowpacks.read(source_text)
            actual_text = self.project_writer.write_snowpacks.as_text(section_from_text)
            msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
            self.assertTrue(match_omit(actual_text, source_text, " \t-;\n"), msg)


def main():
    unittest.main()

if __name__ == "__main__":
    main()
