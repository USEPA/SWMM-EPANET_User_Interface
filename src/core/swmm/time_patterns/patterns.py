from enum import Enum


class PatternType(Enum):
    """Pattern Type"""
    MONTHLY = 1
    DAILY = 2
    HOURLY = 3
    WEEKEND = 4


class Pattern:
    """Pattern multipliers define how some base quantity is adjusted for each time period"""
    def __init__(self):
        self.name = ""
        """Pattern name"""

        self.Type = PatternType.MONTHLY
        """Pattern type"""

        self.description = 0.0
        """Pattern description"""

        self.multipliers = 0.0
        """Array of multipliers for this pattern"""


