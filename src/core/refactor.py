import os
import sys
import errno
import re

reader_method = "get_text"
writer_method = "get_text"
reader_class_prefix = "Read"
writer_class_prefix = "Write"
top_dir = "C:\\devNotMW\\SWMM-EPANET_User_Interface_dev_ui\\src\\"
start_dir = top_dir + "core\\epanet"

reader_path = os.path.join(start_dir, "inp_file_reader.py")
writer_path = os.path.join(start_dir, "inp_file_writer.py")

imports = ["import traceback",
           "from enum import Enum",
           "from core.inputfile import Section"]


def un_camel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

try:
    os.remove(reader_path)
    os.remove(writer_path)
except:
    pass

with open(reader_path, 'wb') as reader_file:
    with open(writer_path, 'wb') as writer_file:
        reader_file.write('\n'.join(imports) + '\n')
        writer_file.write('\n'.join(imports) + '\n')
        for root, subdirs, files in os.walk(start_dir):
            print('--\nroot = ' + root)

            for filename in files:
                file_base, ext = os.path.splitext(filename)
                if ext == ".py":
                    file_path = os.path.join(root, filename)
                    with open(file_path, 'rb') as f:
                        file_contents = f.read()
                    if reader_method in file_contents or writer_method in file_contents:
                        rewrite_filename = os.path.join(root.replace("\\src\\", "\\src-new\\"), file_base) + ".py"
                        rewrite_dir = os.path.dirname(rewrite_filename)
                        try:
                            os.makedirs(rewrite_dir)
                        except OSError as exception:
                            if exception.errno != errno.EEXIST:
                                raise
                        with open(rewrite_filename, 'wb') as rewrite_file:
                            print('\t- file %s (full path: %s)' % (filename, file_path))
                            file_import_path = os.path.join(root, file_base)[len(top_dir):].replace('\\', '.')
                            # collect_file.write('\n' + import_line + '\n')
                            # imports.append(import_line)
                            reader_class_header = []
                            writer_class_header = []
                            in_class = False
                            in_read_method = False
                            in_write_method = False
                            in_other_method = False
                            for line in file_contents.splitlines():
                                fields = re.split(r'[\s,\(,\:]', line)
                                try:
                                    class_index = fields.index("class")
                                    if class_index == 0:
                                        orig_class_name = fields[class_index + 1]
                                        class_var_name = un_camel(orig_class_name)
                                        import_line = "from " + file_import_path + " import " + orig_class_name
                                        reader_file.write(import_line + '\n')
                                        writer_file.write(import_line + '\n')
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
                                            reader_class_header = [line.replace(orig_class_name, reader_class_name)]
                                            writer_class_header = [line.replace(orig_class_name, writer_class_name)]
                                        line = None
                                except Exception as ex:
                                    if str(ex) != "'class' is not in list":
                                        print str(ex)
                                        print line

                                if " def " in line:
                                    in_read_method = reader_method in line
                                    in_write_method = writer_method in line
                                    if in_read_method or in_write_method:
                                        in_other_method = False
                                        # Now that we have found reader or writer method, write the class header.
                                        if reader_class_header:
                                            header_str = '\n'.join(reader_class_header) + '\n'
                                            reader_file.write(header_str)
                                            reader_class_header = []
                                        if writer_class_header:
                                            header_str = '\n'.join(writer_class_header) + '\n'
                                            writer_file.write(header_str)
                                            writer_class_header = []
                                        line = "    @staticmethod\n" + line
                                    else:
                                        in_read_method = False
                                        in_write_method = False
                                        in_other_method = True
                                elif "field_format" in line:  # keep references to field_format only in writer
                                    new_line = line.replace("self.field_format", writer_class_name + ".field_format")
                                    if in_write_method:
                                        writer_file.write(new_line + '\n')
                                    else:
                                        writer_class_header.append(new_line)
                                    line = None  # discard this line before it is written to reader or rewrite

                                if line is not None:
                                    # Replace references to "self" with references to argument class_var_name.
                                    new_line = line.replace("self", class_var_name)

                                    if in_read_method:
                                        reader_file.write(new_line + '\n')
                                    elif in_write_method:
                                        writer_file.write(new_line + '\n')
                                    elif in_class and not in_other_method:
                                        # add this line to class headers, to be written if and when
                                        # reader or writer method is found in this class.
                                        reader_class_header.append(new_line)
                                        writer_class_header.append(new_line)
                                    if not in_read_method and not in_write_method:
                                        # write this line in new version of original file
                                        # unless it is in method to be moved or is a field_format
                                        rewrite_file.write(line + '\n')

                        reader_file.write(b'\n')
                        writer_file.write(b'\n')
        # collect_file.write('\n'.join(imports))
