from core.swmm import title
import unittest


class SimpleTitleTest(unittest.TestCase):
    def __init__(self):
        unittest.TestCase.__init__(self)
        self.my_title = title.Title()

    def setUp(self):
        self.my_title = title.Title()
        self.my_title.title = "test title"

    def runTest(self):

        name = self.my_title.SECTION_NAME
        assert self.my_title.title == "test title"
        assert self.my_title.get_text() == "[TITLE]\ntest title", 'incorrect title block'




