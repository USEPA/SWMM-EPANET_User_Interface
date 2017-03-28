from test.core.regression_base import RegressTestBase
from core.epanet.epanet_project import EpanetProject
from core.epanet.inp_reader_project import ProjectReader
from core.epanet.inp_writer_project import ProjectWriter


class EPANETRegressionTest(RegressTestBase):
    def __init__(self):
        super(EPANETRegressionTest, self).__init__()
        self.my_project = EpanetProject()
        self.new_project = EpanetProject()
        self.reader = ProjectReader
        self.writer = ProjectWriter
        self.model_type = "EPANET"

if __name__ == '__main__':
    my_test = EPANETRegressionTest()
    my_test.runTest()
