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

def match_keyword_lines(test_text, actual_text,
                        keywords_=None, skipped_keywords=None, ignore_trailing_0=False):
    """Test whether section and other have the same contents ignoring case, whitespace, order of lines.
    Args:
        section_text (str): String representation of a section.
        other_section_text (str): String representation of another section to compare with section_text
        keywords_: optional (default None) list of keywords where the lines with these keywords_ will be compared
        skipped_keywords: optional (default ";") list of keywords where the lines with keywords will be ignored in comparison
        ignore_trailing_0: optional (default False) ignore the trailing 0s in a line
    """
    if test_text and actual_text:  # Both are not empty
        test_lines = test_text.splitlines()
        actual_lines = actual_text.splitlines()
        # Skip lines with skipped keywords, default ";"
        new_tlines = []
        new_alines = []
        if skipped_keywords is None:
            skipped_keywords = ";"
        for line in test_lines:
            for skw in skipped_keywords:
                new_str = line.strip().upper()  # strip beginning and ending spaces
                if new_str.find(skw.upper()) != 0:  # did not find the skipped keywords at the beginning
                    new_tlines.append(new_str)
                else:
                    break
        for line in actual_lines:
            for skw in skipped_keywords:
                new_str = line.strip().upper()  # strip beginning and ending spaces
                if new_str.find(skw.upper()) != 0:  # did not find the skipped keywords at the beginning
                    new_alines.append(new_str)
                else:
                    break
        # Selected lines with keywords_
        if keywords_ is not None:
            for kw in keywords_:
                for tline in new_tlines:
                    new_str = tline.strip().upper()  # strip beginning and ending spaces
                    if new_str.find(kw.upper()) == 0:  # find keywords at the beginning
                        new_str = new_str.replace("\t", " ")
                        t_fields = new_str.strip(kw.upper()).split()
                        break
                for aline in new_alines:
                    new_str = aline.strip().upper()  # strip beginning and ending spaces
                    if new_str.find(kw.upper()) == 0:  # find keywords at the beginning
                        new_str = new_str.replace("\t", " ")
                        a_fields = new_str.strip(kw.upper()).split()
                        break
                rst = match_two_lists(t_fields, a_fields, ignore_trailing_0)
                if not rst:
                    return False
        else:
            new_tlines.sort()
            new_alines.sort()
            if len(new_tlines) != len(new_alines):
                return False
            else:
                for t, a in zip(new_tlines, new_alines):
                    t_fields = t.split()
                    a_fields = a.split()
                    rst = match_two_lists(t_fields, a_fields, ignore_trailing_0)
                    if not rst:
                        return False
    elif test_text or actual_text:
        return False  # Only one is empty, so they don't match
    return True

def match_two_lists(t_fields, a_fields, ignore_trailing_0):
    if ignore_trailing_0 or len(t_fields) == len(a_fields):
        for t, a in zip(t_fields, a_fields):
            try:
                t_value = float(t)
                a_value = float(a)
            except:
                t_value = t
                a_value = a
            if t_value != a_value:
                return False
        if len(t_fields) > len(a_fields):
            rest_fields = t_fields[len(a_fields):]
            for r in rest_fields:
                try:
                    if float(r) != 0.0:
                        return False  # not zero
                except:
                    return False  # not a number
        elif len(a_fields) > len(t_fields):
            rest_fields = a_fields[len(t_fields):]
            for r in rest_fields:
                try:
                    if float(r) != 0.0:
                        return False  # not zero
                except:
                    return False  # not a number
    else:
        return False
    return True

