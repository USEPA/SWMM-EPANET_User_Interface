import PyQt4.QtGui as QtGui
import PyQt4.QtCore as QtCore
from enum import Enum


def set_combo_items(enum_type, cbo):
    for enum_item in enum_type:
        cbo.addItem(enum_item.name)


def set_combo(combo_box, value):
    try:
        if isinstance(value, Enum):
            value = value.name
        index = combo_box.findText(value, QtCore.Qt.MatchFixedString)
        if index >= 0:
            combo_box.setCurrentIndex(index)
    except Exception as e:
        print(str(e))
