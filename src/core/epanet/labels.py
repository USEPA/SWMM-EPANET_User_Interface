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

    field_format = '{:16}\t{:16}\t"{}"\t{:16}'

#    attribute,         input_name, label,         default, english, metric, hint
    metadata = Metadata((
        ("label",           '', "Text",            '',    '',   '', "Text of label"),
        ('x',               '', "X-Coordinate",    '',    '',   '', "X coordinate of label on study area map"),
        ('y',               '', "Y-Coordinate",    '',    '',   '', "Y coordinate of label on study area map"),
        ('anchor_node_id',  '', "Anchor Node",     '',    '',   '', "ID label of an anchor node (optional)"),
        ('meter_type',      '', "Meter Type",      '',    '',   '', "Type of object being metered by the label"),
        ('meter_id',        '', "Meter ID",        '',    '',   '', "ID of the object (Node or Link) being metered"),
        ("font",            '', "Font",            "",       '', '',  "The label's font"),
        ("size",            '', "Size",            "10.0",   '', '',  "The label's font size"),
        ("bold",            '', "Bold",            "False",  '', '',  "Set to True if the label is to be bold"),
        ("italics",         '', "Italics",         "False",  '', '',  "Set to True if the label is to be italicized"),
    ))

    def __init__(self, new_text=None):
        if new_text:
            self.set_text(new_text)
        else:
            Section.__init__(self)

            self.x = '0.0'
            """east/west label centroid coordinate"""

            self.y = '0.0'
            """north/south label centroid coordinate"""

            self.label = ''
            """Text of label in double quotes"""

            self.anchor_node_id = ''  # string
            """ID label of an anchor node (optional)"""

            self.meter_type = MeterType.NONE
            """type of object being metered by the label"""

            self.meter_id = ''
            """ID of the object (Node or Link) being metered"""

            self.font = ""
            """label font"""

            self.size = 10.0
            """label size"""

            self.bold = False
            """label bold"""

            self.italic = False
            """lable italics"""

    def get_text(self):
        """format contents of this item for writing to file"""
        return self.field_format.format(self.x, self.y, self.label, self.anchor_node_id)

    def set_text(self, new_text):
        self.__init__()
        new_text = self.set_comment_check_section(new_text)
        fields = new_text.split(None, 2)  # Only use split for first two splits, do last one manually below
        if len(fields) > 1:
            (self.x, self.y) = fields[0:2]
            if len(fields) > 2:
                self.label = fields[2]
                if self.label[0] == '"':  # split above would not work with quotes, so find end of label ourselves
                    endquote = self.label.rindex('"')
                    if endquote + 1 < len(self.label):  # If there is more after the label, it is the anchor_node_id
                        self.anchor_node_id = self.label[endquote + 1:].strip()
                        self.label = self.label[0:endquote + 1]
                self.label = self.label.replace('"', '')  # label is quoted in the file, but not while in memory
