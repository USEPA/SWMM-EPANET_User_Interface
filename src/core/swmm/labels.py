import core.coordinates
from core.project_base import Section
# from core.metadata import Metadata
from traitlets import Unicode, Float, Bool


class Label(Section):
    """Assigns coordinates to map labels"""

    field_format = "{:16}\t{:10}\t{:10}\t{:10}"
#
# #    attribute,         input_name, label,         default, english, metric, hint
#     metadata = Metadata((
#         ("label_text",          '', "Text",            '',       '', '',  "Text of the label"),
#         ('',                    '', "X-Coordinate",    '',       '', '',  "X coordinate of upper left corner of the label on the map"),
#         ('',                    '', "Y-Coordinate",    '',       '', '',  "Y coordinate of upper left corner of the label on the map"),
#         ("anchor_id",           '', "Anchor Node",     "",       '', '',  "Name of a node or subcatchment to which the label is anchored when map is zoomed (optional)"),
#         ("font",                '', "Font",            "",       '', '',  "The label's font"),
#         ("size",                '', "Size",            "10.0",   '', '',  "The label's font size"),
#         ("bold",                '', "Bold",            "False",  '', '',  "Set to True if the label is to be bold"),
#         ("italics",             '', "Italics",         "False",  '', '',  "Set to True if the label is to be italicized"),
#     ))

    def __init__(self):
        self.label_text = Unicode("New Label", help="Text of the label").tag(label="Text", config=True)
        self.anchor_id = Unicode(
            "",
            help="Name of a node or subcatchment to which the label is anchored when map is zoomed (optional)").tag(
            label="Anchor Node", config=True)

        self.font = Unicode("", help="Name of the label's font").tag(label="Font", config=True)
        self.size = Float(10.0, help="Label font size (points)").tag(label="Font Size", config=True)
        self.bold = Bool(False, help="Set to True if the label is to be bold").tag(label="Bold", config=True)
        self.italic = Bool(False, help="Set to True if the label is to be italicized").tag(label="Italics", config=True)

