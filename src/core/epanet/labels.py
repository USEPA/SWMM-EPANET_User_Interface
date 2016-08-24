from enum import Enum

from core.project_base import Section
from core.metadata import Metadata


class MeterType(Enum):
    """Type of object being metered by the label"""
    NONE = 1
    NODE = 2
    LINK = 3


class Label(Section):
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
        ("italics",          '', "Italics",         "False",  '', '',  "Set to True if the label is to be italicized"),
    ))

    def __init__(self):
        Section.__init__(self)

        self.x = '0.0'
        """east/west label centroid coordinate"""

        self.y = '0.0'
        """north/south label centroid coordinate"""

        self.name = ''
        """Text of label in double quotes"""

        self.anchor_name = ''  # string
        """ID label of an anchor node (optional)"""

        self.meter_type = MeterType.NONE
        """type of object being metered by the label"""

        self.meter_name = ''
        """ID of the object (Node or Link) being metered"""

        self.font = ""
        """label font"""

        self.size = 10.0
        """label size"""

        self.bold = False
        """label bold"""

        self.italic = False
        """lable italics"""

