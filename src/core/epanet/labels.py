from enum import Enum

from core.project_base import Section
from core.metadata import Metadata
from core.coordinate import Coordinate


class MeterType(Enum):
    """Type of object being metered by the label"""
    NONE = 1
    NODE = 2
    LINK = 3


class Label(Section, Coordinate):
    """A label on the map with location, text, and optional anchor node ID"""


#    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",             '', "Text",            '',    '',   '', "Text of label"),
        ('x',                '', "X-Coordinate",    '',    '',   '', "X coordinate of label on study area map"),
        ('y',                '', "Y-Coordinate",    '',    '',   '', "Y coordinate of label on study area map"),
        ('anchor_name',      '', "Anchor Node",     '',    '',   '', "ID label of an anchor node (optional)"),
        ('meter_type',       '', "Meter Type",      '',    '',   '', "Type of object being metered by the label"),
        ('meter_name',       '', "Meter ID",        '',    '',   '', "ID of the object (Node or Link) being metered"),
        ("font",             '', "Font",            "",       '', '',  "The label's font"),
        ("size",             '', "Size",            "10.0",   '', '',  "The label's font size"),
        ("bold",             '', "Bold",            "False",  '', '',  "Set to True if the label is to be bold"),
        ("italic",           '', "Italics",         "False",  '', '',  "Set to True if the label is to be italicized"),
    ))

    def __init__(self):
        Section.__init__(self)
        Coordinate.__init__(self)

        """Text of label is saved in name attribute defined in Coordinate base class."""

        ## ID label of an anchor node (optional)
        self.anchor_name = ''  # string

        ## type of object being metered by the label
        self.meter_type = MeterType.NONE

        ## ID of the object (Node or Link) being metered
        self.meter_name = ''

        ## label font
        self.font = ""

        ## label size
        self.size = 10.0

        ## True to use bold
        self.bold = False

        ## True to use italics
        self.italic = False

