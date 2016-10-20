import os
import unittest
import inspect
from core.swmm.swmm_project import SwmmProject
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from core.swmm.inp_reader_sections import *
from core.swmm.inp_writer_sections import *
from test.core.section_match import match, match_omit
from core.swmm.hydraulics.link import CrossSection, CrossSectionShape


class XsectionTest(unittest.TestCase):

    def setUp(self):
        """"""
        self.project_reader = ProjectReader()
        self.project_writer = ProjectWriter()

    def runTest(self):
        directory = os.path.dirname(os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename))
        inp_filename = directory + '\\' + "CrossSectionAllShapes.inp"
        with open(inp_filename,"r") as f:
            source_text = f.read()

        project_reader = ProjectReader()
        project_writer = ProjectWriter()
        my_project = SwmmProject()
        project_reader.read_file(my_project, os.path.join(directory, inp_filename))
        my_xsections = my_project.xsections

        assert len(my_xsections.value) == 26
        actual_text = project_writer.write_xsections.as_text(my_xsections)
        msg = '\nSet:\n' + source_text + '\nGet:\n' + actual_text
        self.assertTrue(match(actual_text, source_text), msg)

        # my_copy = project_reader.read_xsections(section_text)
        # copy_text = project_writer.write_xsections.as_text(my_copy)  # my_copy.set_text(my_xsections.get_text())
        # assert match(section_text, copy_text)

        for index in range(1, 25):  # Purposely not checking last line: second CUSTOM test
            assert my_xsections.value[index].link == str(index)
            assert my_xsections.value[index].shape == CrossSectionShape(index)

        cur_section = my_xsections.value[1]
        assert cur_section.geometry1 == "1.5"
        assert cur_section.geometry2 == "0"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "1"

        cur_section = my_xsections.value[2]
        assert cur_section.geometry1 == "11"
        assert cur_section.geometry2 == "12"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "6"

        cur_section = my_xsections.value[3]
        assert cur_section.geometry1 == "9"
        assert cur_section.geometry2 == "13"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "6"

        cur_section = my_xsections.value[4]
        assert cur_section.geometry1 == "14"
        assert cur_section.geometry2 == "15"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "5"

        cur_section = my_xsections.value[5]
        assert cur_section.geometry1 == "1"
        assert cur_section.geometry2 == "4"
        assert cur_section.geometry3 == "2"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "1"

        cur_section = my_xsections.value[6]
        assert cur_section.geometry1 == "3"
        assert cur_section.geometry2 == "4"
        assert cur_section.geometry3 == "5"
        assert cur_section.geometry4 == "6"
        assert cur_section.barrels == "2"

        cur_section = my_xsections.value[7]
        assert cur_section.geometry1 == "4"
        assert cur_section.geometry2 == "6"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "2"

        cur_section = my_xsections.value[8]
        assert cur_section.geometry1 == "1.167"
        assert cur_section.geometry2 == "1.917"
        assert cur_section.geometry3 == "1"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "9"

        cur_section = my_xsections.value[9]
        assert cur_section.geometry1 == "2.833"
        assert cur_section.geometry2 == "1.833"
        assert cur_section.geometry3 == "3"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "1"

        cur_section = my_xsections.value[10]
        assert cur_section.geometry1 == "1.250"
        assert cur_section.geometry2 == "1.750"
        assert cur_section.geometry3 == "19"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "10"

        cur_section = my_xsections.value[11]
        assert cur_section.geometry1 == "5"
        assert cur_section.geometry2 == "7"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "3"

        cur_section = my_xsections.value[12]
        assert cur_section.geometry1 == "13"
        assert cur_section.geometry2 == "15"
        assert cur_section.geometry3 == "17"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "2"

        cur_section = my_xsections.value[13]
        assert cur_section.geometry1 == "17"
        assert cur_section.geometry2 == "18"
        assert cur_section.geometry3 == "19"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "1"

        cur_section = my_xsections.value[14]
        assert cur_section.geometry1 == "19"
        assert cur_section.geometry2 == "20"
        assert cur_section.geometry3 == "21"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "13"

        cur_section = my_xsections.value[15]
        assert cur_section.geometry1 == "21"
        assert cur_section.geometry2 == "22"
        assert cur_section.geometry3 == "23"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "20"

        cur_section = my_xsections.value[16]
        assert cur_section.geometry1 == "24"
        assert cur_section.geometry2 == "0"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "23"

        cur_section = my_xsections.value[17]
        assert cur_section.geometry1 == "26"
        assert cur_section.geometry2 == "0"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "25"

        cur_section = my_xsections.value[18]
        assert int(float(cur_section.geometry1)) == 47
        assert cur_section.geometry2 == "0"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "1"

        cur_section = my_xsections.value[19]
        assert int(cur_section.geometry1) == 19
        assert cur_section.geometry2 == "0"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "6"

        cur_section = my_xsections.value[20]
        assert int(cur_section.geometry1) == 20
        assert cur_section.geometry2 == "0"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "6"

        cur_section = my_xsections.value[21]
        assert cur_section.geometry1 == "17"
        assert cur_section.geometry2 == "0"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "7"

        cur_section = my_xsections.value[22]
        assert cur_section.geometry1 == "1.222"
        assert cur_section.geometry2 == "0"
        assert cur_section.geometry3 == "0"
        assert cur_section.geometry4 == "0"
        assert cur_section.barrels == "11"

        cur_section = my_xsections.value[23]
        # assert cur_section.transect == "Tran1"
        assert cur_section.geometry1 == "Tran1"

        cur_section = my_xsections.value[24]
        assert cur_section.geometry1 == "2.833"
        assert cur_section.curve == "curve1"
        assert cur_section.barrels == "4"

        cur_section = my_xsections.value[25]
        assert cur_section.geometry1 == "2.933"
        assert cur_section.curve == "curve2"
        assert cur_section.barrels == "5"

def main():
    unittest.main()

if __name__ == "__main__":
    main()
