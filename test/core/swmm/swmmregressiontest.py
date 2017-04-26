from test.core.regression_base import RegressTestBase
from core.swmm.inp_reader_project import ProjectReader
from core.swmm.inp_writer_project import ProjectWriter
from core.swmm.swmm_project import SwmmProject


class SWMMRegressionTest(RegressTestBase):
    def __init__(self):
        super(SWMMRegressionTest, self).__init__()
        self.my_project = SwmmProject()
        self.new_project = SwmmProject()
        self.reader = ProjectReader
        self.writer = ProjectWriter
        self.model_type = "SWMM"

if __name__ == '__main__':
    my_test = SWMMRegressionTest()
    my_test.runTest()
