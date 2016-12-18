class Coordinate:
    """An (x, y) coordinate pair representing a geographic location.
        Measurement units are not stored in or enforced by this class.
        Any units can be used such as lat/long degrees, feet, or meters."""

    def __init__(self):
        self.name = ''

        self.x = ''
        """X-Coordinate; East-West dimension"""

        self.y = ''
        """Y-Coordinate; North-South dimension"""


class Link:
    """A link between nodes in a model"""

    def __init__(self):
        self.name = 'Unnamed'
        """Link Name/Identifier"""

        self.description = ''
        """Optional description of the Link"""

        self.tag = ''
        """Optional label used to categorize or classify the Link"""

        self.inlet_node = 'None'
        """Name of node on the inlet end of the Link"""

        self.outlet_node = 'None'
        """Name of node on the outlet end of the Link"""

        self.vertices = []
        """Intermediate vertices between inlet_node and outlet_node along the length of the link"""


class Polygon:
    def __init__(self):
        self.name = ''
        """Name/Identifier"""

        self.vertices = []
        """Coordinates of each vertex of this polygon"""
