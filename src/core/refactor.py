import os
import sys
import errno
import re

only_method = "get_text"
class_prefix = "Read"
top_dir = "C:\\devNotMW\\SWMM-EPANET_User_Interface_dev_ui\\src\\"
start_dir = top_dir + "core\\epanet"

copy_into = os.path.join(start_dir, "inp_file_write.py")

imports = ["import traceback",
           "from enum import Enum",
           "from core.inputfile import Section"]


def un_camel(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

try:
    os.remove(copy_into)
except:
    print "didn't remove " + copy_into

with open(copy_into, 'wb') as collect_file:
    collect_file.write('\n'.join(imports) + '\n')
    for root, subdirs, files in os.walk(start_dir):
        print('--\nroot = ' + root)

        for filename in files:
            file_base, ext = os.path.splitext(filename)
            if ext == ".py":
                file_path = os.path.join(root, filename)
                with open(file_path, 'rb') as f:
                    file_contents = f.read()
                if only_method in file_contents:
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
                        class_header = []
                        in_class = False
                        in_only_method = False
                        in_other_method = False
                        new_class_name = "self"
                        class_var_name = "self"
                        for line in file_contents.splitlines():
                            fields = re.split(r'[\s,\(,\:]', line)
                            try:
                                class_index = fields.index("class")
                                if class_index == 0:
                                    orig_class_name = fields[class_index + 1]
                                    class_var_name = un_camel(orig_class_name)
                                    import_line = "from " + file_import_path + " import " + orig_class_name
                                    collect_file.write(import_line + '\n')
                                    in_only_method = False
                                    in_other_method = False
                                    class_header = []
                                    if "Enum" not in line:
                                        in_class = True
                                        new_class_name = class_prefix + orig_class_name
                                        line = line.replace(orig_class_name, new_class_name)
                            except Exception as ex:
                                if str(ex) != "'class' is not in list":
                                    print str(ex)
                                    print line

                            if " def " in line:
                                if only_method in line:
                                    in_only_method = True
                                    in_other_method = False
                                    # Now that we have found only_method, write the class header of this class.
                                    # Replace references to "self" with references to argument class_var_name.
                                    # Since we are moving field_format here, write it as new_class_name.field_format
                                    if class_header:
                                        header_str = '\n'.join(class_header) + '\n'
                                        collect_file.write(header_str)
                                        class_header = []
                                    line = "    @staticmethod\n" + line
                                else:
                                    in_only_method = False
                                    in_other_method = True

                            new_line = line.replace("self", class_var_name)\
                                           .replace(class_var_name + ".field_format", new_class_name + ".field_format")

                            if in_only_method:
                                collect_file.write(new_line + '\n')
                            elif in_class and not in_other_method:
                                # add this line to class_header, to be written when only_method is found in this class
                                class_header.append(new_line)
                            if not in_only_method and "field_format" not in line:
                                # write this line in new version of original file
                                # unless it is in method to be moved or is a field_format
                                rewrite_file.write(line + '\n')

                        collect_file.write(b'\n')
    # collect_file.write('\n'.join(imports))
