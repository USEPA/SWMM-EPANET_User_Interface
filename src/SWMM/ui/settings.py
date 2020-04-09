from PyQt5.QtCore import QTranslator
from PyQt5.QtWidgets import QInputDialog
from ui.translations_rc import *


class internationalization:
    def __init__(self):
        self.ui_languages = ("English", "French", "Chinese")
        self.ui_language = "English"
        self.ui_gTranslator = QTranslator()
        self.ui_mTranslator = QTranslator()

    def set_language(self):
        lang = "English"  # QInputDialog.getItem(None, "Select Language", "Language", self.ui_languages)
        self.ui_language = lang[0]
        if self.ui_language == "French":
            self.ui_mTranslator.load(":/french.qm")
            self.ui_gTranslator.load(':/qt_fr.qm')
        elif self.ui_language == "Chinese":
            self.ui_mTranslator.load(":/chinese.qm")
            self.ui_gTranslator.load(':/qt_zh_CN.qm')
