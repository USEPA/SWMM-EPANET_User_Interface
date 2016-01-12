from core.epanet.vertex import Vertex


class Label:
    """Assigns coordinates to map labels"""
    def __init__(self):
        self.Centroid = Vertex
        """X and Y coordinates of label centroid"""

        self.Text = ""			    # string
        """Text of label in double quotes"""

        self.AnchorID = ""			# string
        """ID label of an anchor node (optional)"""


