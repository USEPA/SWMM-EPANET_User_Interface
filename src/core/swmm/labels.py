import core.coordinates


class Label:
    """Assigns coordinates to map labels"""
    def __init__(self):
        self.centroid = core.coordinates
        """X and Y coordinates of label centroid"""

        self.text = ""			    # string
        """Text of label in double quotes"""

        self.anchorID = ""			# string
        """ID label of an anchor node (optional)"""

        self.font = ""
        """label font"""

        self.size = 10.0
        """label size"""

        self.bold = false
        """label bold"""

        self.italic = false
        """lable italics"""

