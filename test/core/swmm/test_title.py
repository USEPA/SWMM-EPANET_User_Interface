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

        new_titles = ["test set_text title", "","test \n test","test \n\n test"]
        for new_title in new_titles:
            self.my_title.set_text(self.my_title.SECTION_NAME + '\n'+new_title)
            self.assertEqual(self.my_title.title,new_title, 'wrong title read by set_text{}'.format(new_title))

