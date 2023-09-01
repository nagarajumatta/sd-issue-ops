"""
This script provides a functionality to search for multiple regex patterns in a given file and replace them with
specified replacement text.
The script is designed to be used with a programming language like Python.

Usage:
./replace_regex_strings.py pattern_name file_path

Parameters:
    pattern_name (str): pattern name for which the different regex variations
                        and replace text are already defined in the script.
    file_path (str): The path to the input file to be processed.


Warning:
    - Always test the script on a backup of your file to avoid accidental data loss.
    - Complex regex patterns can be powerful but also error-prone. Exercise caution when crafting them.

Note:
- Ensure the file is accessible and has the required permissions.
- If the file is extremely large, consider optimizing the script for memory usage.

Author: Sukumar P
Date: 28-07-2023
"""

import re
import sys


def replace_contents(file_name, pattern, replace):
    with open(file_name, 'r') as f:
        content = f.read()
        matches = re.findall(pattern, content, re.DOTALL)
        if matches:
            new_content = re.sub(pattern, replace, content, count=1, flags=re.DOTALL)
        else:
            sys.exit()
    if content != new_content and new_content is not None:
        with open(file_name, 'w') as f:
            print(f"Regex updating file: {file_name}")
            f.write(new_content)
            f.close()


name1_pattern1 = r""
name1_pattern2 = r""
name1_pattern3 = r""
name1_replace = """Something to replace"""

name2_pattern1 = r""
name2_pattern2 = r""
name2_replace = """Something to replace"""

name3_pattern1 = r""
name3_pattern2 = r""
name3_pattern3 = r""
name3_replace = """Something to replace"""

if sys.argv[1] == "name1":
    patterns = (name1_pattern1, name1_pattern2, name1_pattern3)
    replace = name1_replace
elif sys.argv[1] == "name2":
    patterns = (name2_pattern1, name2_pattern2)
    replace = name2_replace
elif sys.argv[1] == "name3":
    patterns = (name3_pattern1, name3_pattern2, name3_pattern3)
    replace = name3_replace
else:
    print("Pattern search should be for one of (name1, name2, name3)")
    sys.exit()

for pattern in patterns:
    replace_contents(f'{sys.argv[2]}', pattern, replace)
