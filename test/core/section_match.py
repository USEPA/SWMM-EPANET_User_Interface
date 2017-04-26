# Methods for comparing expected and actual results while allowing some minor differences


def omit_these(original, omit_chars):
    """Return original with any characters in omit_chars removed.
        Args:
            original (str): Text to search
            omit_chars (str): Characters to remove from original
    """
    return ''.join(c for c in original if c not in omit_chars)


def match_omit(string_one, string_two, omit_chars):
    """Compare strings after removing omit_chars from both. True if they match.
        Args:
            string_one (str): One string to compare
            string_two (str): Other string to compare
            omit_chars (str): Characters to remove from both strings before comparing
    """
    return omit_these(string_one, omit_chars) == omit_these(string_two, omit_chars)


def match_omit_nocase(string_one, string_two, omit_chars):
    """Compare strings after converting to upper case and removing omit_chars. True if they match.
        Args:
            string_one (str): One string to compare
            string_two (str): Other string to compare
            omit_chars (str): Characters to remove from both strings before comparing
    """
    return match_omit(string_one.upper(), string_two.upper(), omit_chars.upper())


def match(section_text, other_section_text):
    """Test whether section and other have the same contents ignoring case, whitespace, order of lines.
    Args:
        section_text (str): String representation of a section.
        other_section_text (str): String representation of another section to compare with section_text
    """
    if section_text and other_section_text:  # Both are not empty
        # Split into lines, strip comments, and keep only lines that are not blank
        # this_sorted = [s for s in section_text.upper().splitlines() if (s.strip() and not s.startswith(';'))]
        # other_sorted = [s for s in other_section_text.upper().splitlines() if (s.strip() and not s.startswith(';'))]
        this_sorted = [s.split(';')[0].strip() for s in section_text.upper().splitlines() if s.split(';')[0].strip()]
        other_sorted = [s.split(';')[0].strip() for s in other_section_text.upper().splitlines() if s.split(';')[0].strip()]
        if len(this_sorted) != len(other_sorted):
            return False  # Different number of significant lines means they do not match.
        # sort lines because we don't care if the same options are in a different order
        this_sorted.sort()
        other_sorted.sort()
        for (this_line, other_line) in zip(this_sorted, other_sorted):
            # Compare each line by replacing any group of spaces and tabs with one space
            this_line_split = this_line.split()
            other_line_split = other_line.split()
            if len(this_line_split) != len(other_line_split):
                return False  # Different number of significant columns in a line means they do not match
            this_line_joined = ' '.join(this_line_split)
            other_line_joined = ' '.join(other_line_split)
            if this_line_joined != other_line_joined:
                # If whole line does not match, check for match of each field
                for (this_field, other_field) in zip(this_line_split, other_line_split):
                    if this_field != other_field:
                        try:  # Check for match when converted to floating point numbers
                            this_float = float(this_field)
                            other_float = float(other_field)
                            if this_float != other_float:
                                return False
                        except ValueError:
                            return False
    elif section_text or other_section_text:
        return False  # Only one is empty, so they don't match
    return True
