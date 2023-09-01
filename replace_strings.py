"""
Search for a specific pattern in the given file and replace it with a replacement text.

Parameters:
    file_name (str): The path to the input file to be processed.
    search_pattern_search (str): The file path which contain search pattern to look for.
    search_pattern_replace (str): The file path which contain replacement text to be used if the search pattern is found.
    occurrences (int, optional): The maximum number of occurrences to replace. Default is None, which replaces all occurrences.

Note:
- This function modifies the content of the input file directly if the search pattern is found.
- If 'occurrences' is provided, only a maximum of that many occurrences will be replaced.

Example usage:
    $ python script_name.py input_file.txt pattern_to_search.txt replacement_text.txt
    $ python script_name.py input_file.txt pattern_to_search.txt replacement_text.txt 2

Author: Sukumar P
Date: 28-07-2023
"""


import sys

file_name = sys.argv[1]
search_pattern_search = open(f'{sys.argv[2]}').read()
search_pattern_replace = open(f'{sys.argv[3]}').read()
file_contents = open(file_name).read()
replace_specific_occurrences = (len(sys.argv) == 5)
if search_pattern_search in file_contents:
  if replace_specific_occurrences:
    occurrences = int(sys.argv[4])
    updated_file_contents = file_contents.replace(search_pattern_search, search_pattern_replace, occurrences)
  else:
    updated_file_contents = file_contents.replace(search_pattern_search, search_pattern_replace)
  if file_contents != updated_file_contents:
    file = open(file_name, 'w')
    file.write(updated_file_contents)
    file.close()
