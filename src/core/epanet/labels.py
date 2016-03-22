from core.epanet.vertex import Vertex


class Label:
    """Assigns coordinates to map labels"""
    def __init__(self):
        self.centroid = Vertex(0, 0, '')
        """X and Y coordinates of label centroid"""

        self.label_text = ''			    # string
        """Text of label in double quotes"""

        self.anchor_id = ''			# string
        """ID label of an anchor node (optional)"""
