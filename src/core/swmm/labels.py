import core.coordinates


class Label:
    """Assigns coordinates to map labels"""
    def __init__(self):
        self.centroid = core.coordinates
        """X and Y coordinates of label centroid"""

        self.label_text = ""			    # string
        """Text of label in double quotes"""

        self.anchor_id = ""			# string
        """ID label of an anchor node (optional)"""

        self.font = ""
        """label font"""

        self.size = 10.0
        """label size"""

        self.bold = False
        """label bold"""

        self.italic = False
        """lable italics"""

