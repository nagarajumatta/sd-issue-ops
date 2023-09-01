patterns_file="./current-repo/replace_config.txt"
directory_path=$1
# Iterate over each line in the patterns file
# Simple search and replace
while IFS= read -r line
do
  IFS=, read -r search_string replace_string <<< "$line"
  find "$directory_path" -type f -exec sed -i "s|$search_string|${replace_string//&/\\&}|g" {} +
done < "$patterns_file"

# Defining variables to be used to create report which determines how many manual updates are avoided.
# These variables will be used in github actions workflows.
counter1=0
counter2=0

echo "COUNTER1=$counter1" >> $GITHUB_ENV
echo "COUNTER2=$counter2" >> $GITHUB_ENV


echo "Text replace...."
grep -ril "text_search_pattern" ${directory_path%/} | while IFS= read -r file; do
  counter1=$((counter1 + 1))
  echo "COUNTER1=$counter1" >> $GITHUB_ENV
  echo "Processing npm file: $file"
  python ./current-repo/replace_strings.py $(realpath "$file") $(realpath ./current-repo/search_and_replace/search.txt) $(realpath ./current-repo/search_and_replace/replace.txt)
done

echo "Regex replace...."
grep -rl "regex_search_pattern" ${directory_path%/} | while IFS= read -r file; do
  counter2=$((counter2 + 1))
  echo "COUNTER2=$counter2" >> $GITHUB_ENV
  echo "Processing regex replace file: $file"
  python ./current-repo/replace_regex_strings.py pattern_name $(realpath "$file")
done
