from core.project_base import Section


class Title(Section):
    """SWMM descriptive title"""

    SECTION_NAME = "[TITLE]"

    def __init__(self):
        Section.__init__(self)
        self.title = "SWMM Project"
        """str: Descriptive title"""

