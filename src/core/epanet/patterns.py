from core.inputfile import Section


class Patterns(Section):
    """PATTERNS section of EPANET input"""

    SECTION_NAME = "[PATTERNS]"

    def __init__(self):
        Section.__init__(self)
        self.comment = ";ID              \tMultipliers"

    def set_text(self, new_text):
        self.__init__()
        self.set_list_comment_plus_ids(new_text, Pattern)


class Pattern:
    """
    Pattern multipliers define how a base quantity is adjusted for each time period.
    If another Pattern is defined with the same ID, it is a continuation of the same Pattern split across lines.
    """
    def __init__(self, new_text=None):
        self.pattern_id = ""
        """Pattern name"""

        self.description = ""
        """Pattern description"""

        self.multipliers = []
        """Array of multipliers for this pattern"""

        if new_text:
            self.set_text(new_text)

    def __str__(self):
        """Override default method to return string representation"""
        return self.get_text()

    def get_text(self):
        """format contents of this item for writing to file"""
        count = 6
        section_text = ""
        for line in self.description.splitlines(True):
            section_text += ';' + line
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
        self.__init__()
        for line in new_text.splitlines():
            comment_split = str.split(line, ';', 1)
            if len(comment_split) == 2:
                self.description += line[1:].strip()
                line = comment_split[0].strip()
            if line:
                fields = line.split()
                if len(fields) > 1:
                    self.pattern_id = fields[0]
                    self.multipliers.extend(fields[1:])
