import unittest
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match
from core.swmm.hydrology.snowpack import SnowPack
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from test.core.section_match import match, match_omit

class SimpleSnowPackTest(unittest.TestCase):

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
        test_snowpack_all = r"""
;;Name           Surface    Parameters
;;-------------- ---------- ----------
s                PLOWABLE   0.001      0.001      32.0       0.10       0.00       0.00       0.0
s                IMPERVIOUS 0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                PERVIOUS   0.001      0.001      32.0       0.10       0.00       0.00       0.00
s                REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0        w
        """
        self.my_options = SnowPack()
        self.my_options.set_text(test_snowpack_all)
        actual_text = self.my_options.get_text() # display purpose
        assert self.my_options.matches(test_snowpack_all)

    def test_one_type(self):
        """test only one type"""
        test_snowpack_removal = r"""
        ;;Name           Surface    Parameters
        ;;-------------- ---------- ----------
        s                REMOVAL    1.0        0.0        0.0        0.0        0.0        0.0        w
                """
        self.my_options = SnowPack()
        self.my_options.set_text(test_snowpack_removal)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_snowpack_removal)

    def test_snowpacks_section(self):
        """Test SNOWPACKS section"""
        test_text = r"""
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
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.snowpacks
        assert match_omit(project_section.get_text(), test_text, " \t-;\n")

def main():
    unittest.main()

if __name__ == "__main__":
    main()
