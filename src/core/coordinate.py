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


