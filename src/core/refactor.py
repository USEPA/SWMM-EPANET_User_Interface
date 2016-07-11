import os
import sys
import errno
import re

reader_method = "set_text"
writer_method = "get_text"
reader_class_prefix = "Read"
writer_class_prefix = "Write"
top_dir = "C:\\devNotMW\\SWMM-EPANET_User_Interface_dev_ui\\src\\"
start_dir = top_dir + "core\\swmm"

original_subpath = "\\src\\"
refactor_subpath = "\\src-refactor\\"

imports = ["import traceback",
           "from enum import Enum",
           "from core.inputfile import Section",
           "from core.metadata import Metadata"]


def un_camel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

reader_path = os.path.join(start_dir, "inp_file_reader.py").replace(original_subpath, refactor_subpath)
writer_path = os.path.join(start_dir, "inp_file_writer.py").replace(original_subpath, refactor_subpath)
try:
    os.remove(reader_path)
    os.remove(writer_path)
except:
    pass

count_edits = 0
reader_contents = []
writer_contents = []
for root, subdirs, files in os.walk(start_dir):
    print('--\nroot = ' + root)

    for filename in files:
        file_base, ext = os.path.splitext(filename)
        if ext == ".py":
            file_path = os.path.join(root, filename)
            with open(file_path, 'rb') as f:
                file_contents = f.read()
            if reader_method in file_contents or writer_method in file_contents:
                rewrite_filename = os.path.join(root.replace(original_subpath, refactor_subpath), file_base) + ".py"
                rewrite_dir = os.path.dirname(rewrite_filename)
                try:
                    os.makedirs(rewrite_dir)
                except OSError as exception:
                    if exception.errno != errno.EEXIST:
                        raise
                with open(rewrite_filename, 'wb') as rewrite_file:
                    print('\t- file %s (full path: %s)' % (filename, file_path))
                    file_import_path = os.path.join(root, file_base)[len(top_dir):].replace('\\', '.')
                    reader_class_header = []
                    writer_class_header = []
                    in_class = False
                    in_read_method = False
                    in_write_method = False
                    in_other_method = False
                    class_var_name = "self"
                    for line in file_contents.splitlines():
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
                                rewrite_file.write(line + '\n')
                                if "Enum" in line:
                                    reader_class_header = []
                                    writer_class_header = []
                                else:
                                    in_class = True
                                    reader_class_name = reader_class_prefix + orig_class_name
                                    writer_class_name = writer_class_prefix + orig_class_name
                                    reader_class_header = ["\n", line.replace(orig_class_name, reader_class_name)]
                                    writer_class_header = ["\n", line.replace(orig_class_name, writer_class_name)]
                                line = None
                        except Exception as ex:
                            if str(ex) != "'class' is not in list":
                                print str(ex)
                                print line

                        if line is not None:
                            if " def " in line:
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
                                    count_edits += 1
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
                                count_edits += 1

                            if line is not None:
                                # Replace references to "self" with references to argument class_var_name.
                                new_line = line.replace("self", class_var_name)
                                if new_line != line:
                                    count_edits += 1

                                if in_read_method:
                                    reader_contents.append(new_line)
                                elif in_write_method:
                                    writer_contents.append(new_line)
                                elif in_class and not in_other_method:
                                    # add this line to class headers, to be written if and when
                                    # a reader or writer method is found in this class.
                                    reader_class_header.append(new_line)
                                    writer_class_header.append(new_line)
                                if not in_read_method and not in_write_method:
                                    # write this line in new version of original file
                                    # unless it is in method to be moved.
                                    # remove Section as parent class
                                    if "Section.__init__(self)" not in line and\
                                       "from core.inputfile import " not in line:
                                        rewrite_line = line.replace("(Section)", '') + '\n'
                                        if ("Section" in rewrite_line and not "CrossSection" in rewrite_line
                                             and not "XSECTION" in rewrite_line) or\
                                            "InputFile" in rewrite_line:
                                            print rewrite_line
                                        rewrite_file.write(rewrite_line)
                                        if rewrite_line != line:
                                            count_edits += 1

if writer_contents:
    with open(writer_path, 'wb') as writer_file:
        writer_file.write('\n'.join(imports) + '\n\n')
        writer_file.write('\n'.join(writer_contents) + '\n\n')

if reader_contents:
    with open(reader_path, 'wb') as reader_file:
        reader_file.write('\n'.join(imports) + '\n\n')
        reader_file.write('\n'.join(reader_contents) + '\n\n')

print "Counted edits: " + str(count_edits) + " written to " + start_dir.replace(original_subpath, refactor_subpath)