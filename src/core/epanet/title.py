from core.project_base import Section


class Title(Section):
    """EPANET descriptive title"""

    SECTION_NAME = "[TITLE]"

    def __init__(self):
        Section.__init__(self)
        self.title = ""
        self.notes = ""
        """str: Descriptive title"""

