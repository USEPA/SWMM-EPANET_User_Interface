from core.project_base import Section


class Pattern(Section):
    """
    Pattern multipliers define how a base quantity is adjusted for each time period.
    If another Pattern is defined with the same ID, it is a continuation of the same Pattern split across lines.
    """
    def __init__(self):
        Section.__init__(self)

        ## Pattern name
        self.name = ""

        ## Pattern description
        self.description = ""

        ## Array of multipliers for this pattern
        self.multipliers = []

