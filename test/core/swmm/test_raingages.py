import unittest
from core.inputfile import Section
from core.swmm.project import Project
from core.swmm.hydrology.raingage import RainGage


class SimpleRainGageTest(unittest.TestCase):
    """Test RAINGAGES section"""

    def test_one_raingage(self):
        """Test one rain gage"""
        test_raingage = "RainGage         INTENSITY 0:05   1.0    TIMESERIES 2-yr "
        self.my_options = RainGage()
        self.my_options.set_text(test_raingage)
        assert self.my_options.matches(test_raingage)

    def test_raingage_section(self):
        """Test RAINGAGES section"""
        test_text = """[RAINGAGES]
;;               Rain      Time   Snow   Data
;;Name           Type      Intrvl Catch  Source
;;-------------- --------- ------ ------ ----------
RainGage         INTENSITY 0:05   1.0    TIMESERIES 2-yr"""
        from_text = Project()
        from_text.set_text(test_text)
        project_section = from_text.raingages
        assert Section.match_omit(project_section.get_text(), test_text, " \t-;\n")

