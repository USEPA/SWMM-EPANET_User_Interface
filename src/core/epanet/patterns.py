

class Pattern:
    """
    Pattern multipliers define how a base quantity is adjusted for each time period.
    If another Pattern is defined with the same ID, it is a continuation of the same Pattern split across lines.
    """
    def __init__(self):
        self.pattern_id = ""
        """Pattern name"""

        self.description = ""
        """Pattern description"""

        self.multipliers = []
        """Array of multipliers for this pattern"""

    def __str__(self):
        """Override default method to return string representation"""
        return self.get_text()

    def get_text(self):
        """format contents of this item for writing to file"""
        count = 6
        section_text = ""
        for multiplier in self.multipliers:
            if count == 6:        # add ID to first line and break lines before they get too long
                if section_text:  # If there are already values added, put next value on a new line
                    section_text += '\n'
                section_text += " {:16}".format(self.pattern_id)
                count = 0
            section_text += "\t{:12}".format(multiplier)
            count += 1
        return section_text

    def set_text(self, new_text):
        fields = new_text.split()
        self.pattern_id = fields[0]
        self.multipliers = fields[1:]
