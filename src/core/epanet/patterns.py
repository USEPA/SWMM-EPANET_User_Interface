

class Pattern:
    """Pattern multipliers define how some base quantity is adjusted for each time period"""
    def __init__(self):
        self.pattern_id = ""
        """Pattern name"""

        self.description = ""
        """Pattern description"""

        self.multipliers = []
        """Array of multipliers for this pattern"""

    def to_inp(self):
        """format contents of this item for writing to file"""
        return str(self.pattern_id) + '\t' + '\t'.join(self.multipliers)
        # TODO: format for remaining fields?       + str(self.head_curve)
        # TODO: What is the rule for creating columns? Will any amount of whitespace work?

    def set_from_text(self, text):
        fields = text.split()
        self.pattern_id = fields[0]
        self.multipliers = fields[1:]
