import os
import sys
import errno
import re

"""
Refactor existing code that contains class definitions with reader and writer methods
by moving reader methods all into a new file "inp_file_reader.py"
and moving writer methods all into a new file "inp_file_writer.py"

This version does not handle re-writing code that accesses the reader and writer methods.
"""

reader_method = "set_text"
writer_method = "get_text"
reader_class_prefix = "Read"
writer_class_prefix = "Write"
top_dir = "C:\\devNotMW\\GitHub\\SWMM-EPANET_User_Interface_master\\src\\"
start_dir = top_dir + "core\\swmm"
# start_dir = top_dir + "core\\epanet"

original_subpath = "\\src\\"
refactor_subpath = "\\src-refactor\\"

imports = ["import traceback",
           "from enum import Enum",
           "from core.inputfile import Section",
           "from core.metadata import Metadata"]


def un_camel(name):
    """ Take ClassNameLikeThis and return class_name_like_this, for converting a class name into a variable name. """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

inp_prefix = "inp_"

reader_path = os.path.join(start_dir, inp_prefix + "reader_sections.py").replace(original_subpath, refactor_subpath)
writer_path = os.path.join(start_dir, inp_prefix + "writer_sections.py").replace(original_subpath, refactor_subpath)
try:
    os.remove(reader_path)
    os.remove(writer_path)
except:
    pass

folders_read = 0
files_read = 0
files_edited = 0
lines_read = 0
edits_made = 0
class_header_edits_made = 0
reader_contents = []
writer_contents = []
for root, subdirs, files in os.walk(start_dir):
    print('reading folder ' + root)
    folders_read += 1

    for filename in files:
        file_base, ext = os.path.splitext(filename)
        # Only scan Python files and do not scan new files that are already part of this refactor
        if ext == ".py" and not file_base.startswith(inp_prefix):
            file_path = os.path.join(root, filename)
            with open(file_path, 'rb') as f:
                file_contents = f.read()
                files_read += 1
            if reader_method in file_contents or writer_method in file_contents:
                files_edited += 1
                rewrite_filename = os.path.join(root.replace(original_subpath, refactor_subpath), file_base) + ".py"
                rewrite_dir = os.path.dirname(rewrite_filename)
                try:
                    os.makedirs(rewrite_dir)
                except OSError as exception:
                    if exception.errno != errno.EEXIST:
                        raise
                with open(rewrite_filename, 'wb') as rewrite_file:
                    # print('\t- file %s (full path: %s)' % (filename, file_path))
                    file_import_path = os.path.join(root, file_base)[len(top_dir):].replace('\\', '.')
                    reader_class_header = []
                    writer_class_header = []
                    class_header_edits_made = 0
                    in_class = False
                    in_read_method = False
                    in_write_method = False
                    in_other_method = False
                    class_var_name = "self"
                    orig_class_name = None
                    for line in file_contents.splitlines():
                        lines_read += 1
                        fields = re.split(r'[\s,\(,\:]', line)
                        try:
                            class_index = fields.index("class")
                            if class_index == 0:
                                orig_class_name = fields[class_index + 1]
                                class_var_name = un_camel(orig_class_name)
                                import_line = "from " + file_import_path + " import " + orig_class_name
                                imports.append(import_line)
                                # reader_file.write(import_line + '\n')
                                # writer_file.write(import_line + '\n')
                                in_read_method = False
                                in_write_method = False
                                in_other_method = False

                                rewrite_line = line.replace("(Section)", '') + '\n'
                                if ("Section" in rewrite_line and not "CrossSection" in rewrite_line
                                     and not "XSECTION" in rewrite_line) or\
                                    "InputFile" in rewrite_line:
                                    print(rewrite_line)
                                rewrite_file.write(rewrite_line)
                                if rewrite_line != line:
                                    edits_made += 1

                                if "Enum" in line:
                                    in_class = False
                                    reader_class_header = []
                                    writer_class_header = []
                                    class_header_edits_made = 0
                                    class_var_name = "self"
                                    orig_class_name = None
                                else:
                                    in_class = True
                                    reader_class_name = reader_class_prefix + orig_class_name
                                    writer_class_name = writer_class_prefix + orig_class_name
                                    reader_class_header = ["\n", line.replace(orig_class_name, reader_class_name)]
                                    writer_class_header = ["\n", line.replace(orig_class_name, writer_class_name)]
                                    class_header_edits_made = 1
                                line = None
                        except Exception as ex:
                            if str(ex) != "'class' is not in list":
                                print(str(ex))
                                print(line)

                        if line is not None:
                            if " def " in line:
                                if in_read_method:
                                    reader_contents.append("\n        return " + class_var_name + '\n\n')
                                in_read_method = reader_method in line
                                in_write_method = writer_method in line
                                if in_read_method or in_write_method:
                                    in_other_method = False
                                    # Now that we have found reader or writer method, write the class header.
                                    if reader_class_header:
                                        reader_contents.extend(reader_class_header)
                                        reader_class_header = []
                                    if writer_class_header:
                                        writer_contents.extend(writer_class_header)
                                        writer_class_header = []
                                    line = "    @staticmethod\n" + line
                                    edits_made += 1 + class_header_edits_made
                                    class_header_edits_made = 0
                                    if in_read_method:
                                        line = line.replace("self, ", '')  # remove self argument
                                else:
                                    in_read_method = False
                                    in_write_method = False
                                    in_other_method = True
                            elif "field_format" in line:  # keep references to field_format only in writer
                                new_line = line.replace("self.field_format", writer_class_name + ".field_format")
                                new_line = new_line.replace("self", class_var_name)
                                if in_write_method:
                                    writer_contents.append(new_line)
                                else:
                                    writer_class_header.append(new_line)
                                line = None  # discard this line before it is written to reader or rewrite
                                # edits_made += 1

                            if line is not None:
                                # Replace references to "self" with references to argument class_var_name.
                                if orig_class_name:
                                    new_line = line.replace("self.__init__()",
                                                            class_var_name + " = " + orig_class_name + "()")
                                new_line = line.replace("self", class_var_name)

                                if in_read_method:
                                    reader_contents.append(new_line)
                                    if new_line != line:
                                        edits_made += 1
                                elif in_write_method:
                                    writer_contents.append(new_line)
                                    if new_line != line:
                                        edits_made += 1
                                elif in_class and not in_other_method:
                                    # add this line to class headers, to be written if and when
                                    # a reader or writer method is found in this class.
                                    reader_class_header.append(new_line)
                                    writer_class_header.append(new_line)
                                    if new_line != line:
                                        class_header_edits_made += 1
                                if not in_read_method and not in_write_method:
                                    # write this line in new version of original file
                                    # unless it is in method to be moved.
                                    # remove Section as parent class
                                    if "Section.__init__(self)" not in line and\
                                       "SECTION_NAME =" not in line and\
                                       "from core.inputfile import " not in line:
                                        rewrite_line = line.replace("(Section)", '')
                                        if ("Section" in rewrite_line and not "CrossSection" in rewrite_line
                                             and not "XSECTION" in rewrite_line) or\
                                            "InputFile" in rewrite_line or \
                                            "SECTION_NAME" in rewrite_line:
                                            print("Questionable line rewritten from " + file_base + ':\n' + line\
                                                  + "\nto:" + rewrite_filename + ':\n' + rewrite_line)
                                        rewrite_file.write(rewrite_line + '\n')
                                        if rewrite_line != line:
                                            edits_made += 1
                    if in_read_method:
                        reader_contents.append("        return " + class_var_name)
                        in_read_method = False

if writer_contents:
    with open(writer_path, 'wb') as writer_file:
        writer_file.write('\n'.join(imports) + '\n\n')
        writer_file.write('\n'.join(writer_contents) + '\n\n')

if reader_contents:
    with open(reader_path, 'wb') as reader_file:
        reader_file.write('\n'.join(imports) + '\n\n')
        reader_file.write('\n'.join(reader_contents) + '\n\n')

print("\nFolders read: " + str(folders_read))
print("Files read: " + str(files_read))
print("Files edited: " + str(files_edited))
print("Lines in edited files: " + str(lines_read))
print("Edits made: " + str(edits_made))
print("Refactored classes written to " + start_dir.replace(original_subpath, refactor_subpath))
