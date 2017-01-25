class Coordinate:
    """An (x, y) coordinate pair representing a geographic location.
        Measurement units are not stored in or enforced by this class.
        Any units can be used such as lat/long degrees, feet, or meters."""

    def __init__(self):
        self.name = ''

        ## X-Coordinate; East-West dimension
        self.x = ''

        ## Y-Coordinate; North-South dimension
        self.y = ''


class Link:
    """A link between nodes in a model"""

    def __init__(self):

        ## Link Name/Identifier
        self.name = 'Unnamed'

        ## Optional description of the Link
        self.description = ''

        ## Optional label used to categorize or classify the Link
        self.tag = ''

        ## Name of node on the inlet end of the Link
        self.inlet_node = 'None'

        ## Name of node on the outlet end of the Link
        self.outlet_node = 'None'

        ## Intermediate vertices between inlet_node and outlet_node along the length of the link
        self.vertices = []


class Polygon:
    def __init__(self):
        ## Name/Identifier
        self.name = ''

        ## Coordinates of each vertex of this polygon
        self.vertices = []

