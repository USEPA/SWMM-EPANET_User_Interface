from enum import Enum


class PatternType(Enum):
    """Pattern Type"""
    MONTHLY = 1
    DAILY = 2
    HOURLY = 3
    WEEKEND = 4


class Pattern:
    """Pattern multipliers define how some base quantity is adjusted for each time period"""
    def __init__(self, new_text=None):
        self.name = ""
        """Pattern name"""

        self.pattern_type = PatternType.MONTHLY
        """Pattern type"""

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
        section_text = ''
        pattern_text = self.pattern_type.name
        for line in self.description.splitlines(True):
            section_text += ';' + line
        for multiplier in self.multipliers:
            if count == 6:        # add ID to first line and break lines before they get too long
                if section_text:  # If there are already values added, put next value on a new line
                    section_text += '\n'
                section_text += " {:16}{:10}".format(self.name, pattern_text)
                pattern_text = ''
                count = 0
            section_text += "\t{:5}".format(multiplier)
            count += 1
        return section_text

    def set_text(self, new_text):
        self.__init__()
        for line in new_text.splitlines():
            comment_split = str.split(line, ';', 1)
            if len(comment_split) > 1:
                self.description += line[1:].strip()
                line = comment_split[0].strip()
            if line:
                fields = line.split()
                if len(fields) > 1:
                    self.name = fields[0]
                    check_type = fields[1].upper()
                    try:
                        self.pattern_type = PatternType[check_type]
                        first_multiplier = 2
                    except:
                        first_multiplier = 1
                    self.multipliers.extend(fields[first_multiplier:])

