

class Pattern:
    """
    Pattern multipliers define how a base quantity is adjusted for each time period.
    If another Pattern is defined with the same ID, it is a continuation of the same Pattern split across lines.
    """
    def __init__(self):
        self.name = ""
        """Pattern name"""

        self.description = ""
        """Pattern description"""

        self.multipliers = []
        """Array of multipliers for this pattern"""

