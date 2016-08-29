import core.coordinate
from core.project_base import Section
from core.metadata import Metadata
from core.coordinate import Coordinate


class Label(Section, Coordinate):
    """Assigns coordinates to map labels"""

    #    attribute,     input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                '', "Text",            '',       '', '',  "Text of the label"),
        ('',                    '', "X-Coordinate",    '',       '', '',  "X coordinate of upper left corner of the label on the map"),
        ('',                    '', "Y-Coordinate",    '',       '', '',  "Y coordinate of upper left corner of the label on the map"),
        ("anchor_name",         '', "Anchor Node",     "",       '', '',  "Name of a node or subcatchment to which the label is anchored when map is zoomed (optional)"),
        ("font",                '', "Font",            "",       '', '',  "The label's font"),
        ("size",                '', "Size",            "10.0",   '', '',  "The label's font size"),
        ("bold",                '', "Bold",            "False",  '', '',  "Set to True if the label is to be bold"),
        ("italics",             '', "Italics",         "False",  '', '',  "Set to True if the label is to be italicized"),
    ))

    def __init__(self):
        Section.__init__(self)
        Coordinate.__init__(self)

        """Text of label is saved in name attribute defined in Coordinate base class."""

        self.anchor_name = ""			# string
        """ID label of an anchor node (optional)"""

        self.font = ""
        """label font"""

        self.size = 10.0
        """label size"""

        self.bold = False
        """label bold"""

        self.italic = False
        """lable italics"""

