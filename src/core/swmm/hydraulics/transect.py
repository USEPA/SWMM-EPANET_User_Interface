from enum import Enum


class Transect:
    """Describes the cross-section geometry of natural channels or conduits with irregular shapes
    following the HEC-2 data format"""
    def __init__(self, name):
        self.name = name
        """Transect Name"""

        self.description = None
        """Optional description of the Transect"""

        self.station_elevation_data_grid = None
        """Values of distance from the left side of the channel along with the corresponding elevation of the
        channel bottom as one moves across the channel from left to right, looking in the downstream direction"""

        self.roughness_left_bank = 0.0
        """Mannings roughness for the left overbank portion of the transect"""

        self.roughness_right_bank = 0.0
        """Mannings roughness for the right overbank portion of the transect"""

        self.roughness_channel = 0.0
        """Mannings roughness for the main channel portion of the transect"""

        self.bank_station_left = 0.0
        """Distance value appearing in the Station/Elevation grid that marks the end of the left overbank"""

        self.bank_station_right = 0.0
        """Distance value appearing in the Station/Elevation grid that marks the start of the right overbank"""

        self.stations_modifier = 0.0
        """Factor by which the distance between each station will be multiplied when the transect data is processed"""

        self.elevations_modifier = 0.0
        """Constant value that will be added to each elevation value"""

        self.meander_modifier = 0.0
        """Ratio of the length of a meandering main channel to the length of the overbank area that surrounds it."""
