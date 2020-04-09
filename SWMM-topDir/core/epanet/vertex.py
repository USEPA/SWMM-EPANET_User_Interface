from core.coordinate import Coordinate


class Vertex(Coordinate):
    """Assigns interior vertex points to network links"""
    def __init__(self, x, y, link):
        Coordinate.__init__(self, x, y)
        self.link = link
