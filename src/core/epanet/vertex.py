from core.coordinates import Coordinates


class Vertex(Coordinates):
    """Assigns interior vertex points to network links"""
    def __init__(self, x, y, link):
        Coordinates.__init__(self, x, y)
        self.link = link
