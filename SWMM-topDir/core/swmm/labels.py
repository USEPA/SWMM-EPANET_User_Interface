import core.coordinate
from core.project_base import Section
from core.metadata import Metadata
from core.coordinate import Coordinate


class Label(Section, Coordinate):
    """Assigns coordinates to map labels"""

    #    attribute,     input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("name",                '', "Text",            '',       '', '',  "Text of the label"),
        ('x',                   '', "X-Coordinate",    '',       '', '',  "X coordinate of upper left corner of the label on the map"),
        ('y',                   '', "Y-Coordinate",    '',       '', '',  "Y coordinate of upper left corner of the label on the map"),
        ("anchor_name",         '', "Anchor Node",     "",       '', '',  "Name of a node or subcatchment to which the label is anchored when map is zoomed (optional)"),
        ("font",                '', "Font",            "",       '', '',  "The label's font"),
        ("size",                '', "Size",            "10.0",   '', '',  "The label's font size"),
        ("bold",                '', "Bold",            "False",  '', '',  "Set to True if the label is to be bold"),
        ("italic",              '', "Italics",         "False",  '', '',  "Set to True if the label is to be italicized"),
    ))

    def __init__(self):
        Section.__init__(self)
        Coordinate.__init__(self)

        """Text of label is saved in name attribute defined in Coordinate base class."""

        ## ID label of an anchor node (optional)
        self.anchor_name = ""			# string

        ## label font
        self.font = ""

        ## label size
        self.size = 10.0

        ## label bold
        self.bold = False

        ## lable italics
        self.italic = False


