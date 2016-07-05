import os
import sys
import errno
import re

only_method = "get_text"
top_dir = "C:\\devNotMW\\GitHub\\SWMM-EPANET_User_Interface_master\\src\\"
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
                        import_line = "import " + os.path.join(root, file_base)[len(top_dir):].replace('\\', '.')
                        collect_file.write('\n' + import_line + '\n')
                        imports.append(import_line)
                        class_header = []
                        in_class = False
                        in_only_method = False
                        in_other_method = False
                        for line in file_contents.splitlines():
                            fields = re.split(r'[\s,\(,\:]', line)
                            try:
                                class_index = fields.index("class")
                                if class_index == 0:
                                    class_name = fields[class_index + 1]
                                    class_var_name = un_camel(class_name)
                                    in_class = True  # not ("(Enum)" in line)  # "Section" in line
                                    class_header = []
                            except Exception as ex:
                                if str(ex) != "'class' is not in list":
                                    print str(ex)
                                    print line

                            if " def " in line:
                                if only_method in line:
                                    in_only_method = True
                                    in_other_method = False
                                    if class_header:
                                        collect_file.write('\n'.join(class_header) + '\n')
                                        class_header = []
                                    line = "    @staticmethod\n" + line
                                else:
                                    in_only_method = False
                                    in_other_method = True
                            if in_class and not in_other_method:
                                class_header.append(line)

                                # replace references to "self" with references to argument class_var_name,
                                # except since we are moving field_format here, write as class_name.field_format
                                collect_file.write(line
                                                   .replace("self", class_var_name)
                                                   .replace(class_var_name + ".field_format",
                                                            class_name + ".field_format") +
                                                   '\n')
                            if not in_only_method and "field_format" not in line:
                                rewrite_file.write(line + '\n')

                        collect_file.write(b'\n')
    # collect_file.write('\n'.join(imports))
