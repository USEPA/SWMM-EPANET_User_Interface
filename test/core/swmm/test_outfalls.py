import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydraulics.node import Outfall


class SimpleOutfallTest(unittest.TestCase):
    """Test OUTFALLS section"""

    def test_one_outfall(self):
        """Test one outfall will all parameters"""
        test_outfall = r""" 18      975    FREE      NO       xxx"""
        self.my_options = Outfall()
        self.my_options.set_text(test_outfall)
        # --Test get_text through matches
        actual_text = self.my_options.get_text()  # display purpose
        assert self.my_options.matches(test_outfall)

    def test_outfall_section(self):
        """Test OUTFALLS section"""
        test_text = r"""
[OUTFALLS]
;;Name           Elevation  Type       Stage Data       Gated    Route To
;;-------------- ---------- ---------- ---------------- -------- ----------------
18               975        FREE                        NO
18               975        FREE                        NO       xxx
        """
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.outfalls
        assert Section.match_omit(project_section.get_text(), test_text, " \t-;\n")