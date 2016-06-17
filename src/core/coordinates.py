class Coordinates:
    """An (x, y) coordinate pair representing a geographic location.
        Measurement units are not stored in or enforced by this class.
        Any units can be used such as lat/long degrees, feet, or meters."""

    def __init__(self):
        self.id = ''

        self.x = ''
        """X-Coordinate; East-West dimension"""

        self.y = ''
        """Y-Coordinate; North-South dimension"""

    def __str__(self):
        return self.get_text()

    def get_text(self):
        inp = ''
        if self.comment:
            inp = self.comment + '\n'
        inp += self.field_format.format(self.id, self.x, self.y)
        return inp

    def set_text(self, new_text):
        self.__init__()
        fields = new_text.split()
        if len(fields) > 2:
            self.id, self.x, self.y = fields[0:3]
