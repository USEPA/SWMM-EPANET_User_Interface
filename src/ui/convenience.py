import PyQt5.QtGui as QtGui
import PyQt5.QtCore as QtCore
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


def all_list_items(list_widget):
    """Get all the items in a QListWidget as a list of strings"""
    return [str(list_widget.item(i).text()) for i in range(list_widget.count())]


def selected_list_items(list_widget):
    return [str(list_item.text()) for list_item in list_widget.selectedItems()]
