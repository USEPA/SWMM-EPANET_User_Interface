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
                new_str = line.strip().upper() # strip beginning and ending spaces
                if new_str.replace("\n", "").replace("\t","").replace(" ","") != "":
                    if new_str.find(skw.upper()) != 0:  # did not find the skipped keywords at the beginning
                        new_tlines.append(new_str)
                    else:
                        break
        for line in actual_lines:
            for skw in skipped_keywords:
                new_str = line.strip().upper()  # strip beginning and ending spaces
                if new_str.replace("\n", "").replace("\t","").replace(" ","") != "":
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
                    if float(r) != 0.0 and float(r) != 1.0:
                        return False  # not zero and not one (typical defaults)
                except:
                    return False  # not a number
    else:
        return False
    return True


def get_immediate_subdirectories(a_dir):
    import os
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


def readline_nowhite(f):
    """ Readline_nowhite
     Strip all carriage returns, tabs and spaces
     If it is empty line, read the next line
     Return the lines read, and the line without white
    """
    f_line = f.readline()
    line_no = 1
    f_line_nw = f_line.replace('\n', '').replace('\t', '').replace(' ', '')

    while f_line_nw == '' and f_line != '':
        f_line = f.readline()
        line_no += 1
        f_line_nw = f_line.replace('\n', '').replace('\t', '').replace(' ', '')
    f_line = f_line_nw
    return line_no, f_line


def compare_two_files(fname1, fname2, exempted_strings):
    """Reference: http://www.opentechguides.com/how-to/article/python/58/python-file-comparison.html
    Modified by xw 2016/05/12
    Strip all white spaces, empty lines and exempt the lines with exempted_strings
    Return a string message diff_msg. If identical, return empty string
    """

    diff_msg = ''
    # Open file for reading in text mode (default mode)
    f1 = open(fname1)
    f2 = open(fname2)

    # Initialize counter for line number
    line_no_f1 = 0
    line_no_f2 = 0

    # Readline_nowhite
    # Strip all carriage returns, tabs and spaces
    # If it is empty line, read the next line
    # File 1:
    line_read, f1_line = readline_nowhite(f1)
    line_no_f1 = line_no_f1 + line_read

    # File 2:
    line_read, f2_line = readline_nowhite(f2)
    line_no_f2 = line_no_f2 + line_read

    # Loop if either file1 or file2 has not reached EOF
    while f1_line != '' or f2_line != '':

        # Compare the lines from both file
        if f1_line != f2_line:

            is_diff = True
            # Loop through lines with keyword(s) indicating an exemption
            for exempted_string in exempted_strings:
                str_nw = exempted_string.replace(' ', '')
                if f1_line.find(str_nw) != -1 \
                        and f2_line.find(str_nw) != -1:
                    is_diff = False
                    # Break when the exempted_string hit
                    break

            if is_diff:
                diff_msg = '<br>[old]Line-' + str(line_no_f1) + ':' + f1_line + '<br>' + \
                           '[new]Line-' + str(line_no_f2) + ':' + f2_line + '<br>'
                # Break on the first difference
                break

        # File 1:
        line_read, f1_line = readline_nowhite(f1)
        line_no_f1 = line_no_f1 + line_read

        # File 2:
        line_read, f2_line = readline_nowhite(f2)
        line_no_f2 = line_no_f2 + line_read

    # Close the files
    f1.close()
    f2.close()
    return diff_msg


def compare_two_analysis_blocks(fname1, fname2, exempted_strings,
                                str_start="Analysis begun", str_end="Analysis ended"):
    """Modified from method compare_two_files by xw 3/27/2017
    Compare text between "Analysis begun" and "Analysis ended" of EPANET rpt files:
    Strip all white spaces, empty lines and exempt the lines with exempted_strings
    Return a string message diff_msg. If identical, return empty string
    """

    diff_msg = ''
    # Open file for reading in text mode (default mode)

    fnames = [fname1, fname2]
    new_lines = [[], []]
    try:
        for ifile, fname in enumerate(fnames):
            f = open(fname)
            lines = f.readlines()
            start_compare = False

            for id_line, line in enumerate(lines):
                if line.find(str_start) != -1:
                    start_compare = True
                elif line.find(str_end) != -1:
                    start_compare = False
                elif start_compare:
                    if line.replace(' ', '').replace('\t', '').replace('\n', '') != '':
                        is_exempted = False
                        for exempted_string in exempted_strings:
                            if line.find(exempted_string) == -1:
                                is_exempted = False
                            else:
                                is_exempted = True
                                break
                        if is_exempted is False:
                            new_lines[ifile].append([id_line, line])
                else:
                    pass
            f.close()
    except IOError as e:
        diff_msg = '<br>IO Error: {} <br>'.format(str(e))

    for f1_line, f2_line in zip(new_lines[0], new_lines[1]):
        if f1_line[1] != f2_line[1]:
            is_diff = True
            if is_diff:
                diff_msg = '<br>[old]Line-' + str(f1_line[0]) + ':' + f1_line[1] + '<br>' + \
                           '[new]Line-' + str(f1_line[0]) + ':' + f2_line[1] + '<br>'
                # Break on the first difference
                break
    return diff_msg

