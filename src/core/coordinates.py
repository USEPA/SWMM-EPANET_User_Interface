class Coordinates:
    """An (x, y) coordinate pair representing a geographic location.
        Measurement units are not stored in or enforced by this class.
        Any units can be used such as lat/long degrees, feet, or meters."""

    def __init__(self, x, y):
        self.x = x
        """X-Coordinate; East-West dimension"""

        self.y = y
        """Y-Coordinate; North-South dimension"""
