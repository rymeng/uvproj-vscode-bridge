import os
import re
import sys
import json

def modify_define_lines(content):
    items = []
    lines = content.splitlines()

    for line in lines:
        match_macro_with_value = re.match(r'^\s*#define\s+(\S+)\s*$', line)
        if match_macro_with_value:
            items.append(f"{match_macro_with_value.group(1)}")
            continue
        match_macro_without_value = re.match(r'^\s*#define\s+(\S+)\s+(.+)$', line)
        if match_macro_without_value:
            items.append(f"{match_macro_without_value.group(1)}={match_macro_without_value.group(2)}")

    return items

def main():
    source_files = []
    if len(sys.argv) > 1:
        source_files = sys.argv[1:]
    else:
        print("Error: No input file.")
        sys.exit(1)

    items = []

    for source_file in source_files:
        try:
            with open(source_file, 'r') as f:
                content = f.read()
                items = modify_define_lines(content)
                print(f"Processing {source_file} done. Finding macro number: {len(items)}.")
        except Exception as e:
            print(f"Error processing file {source_file}: {str(e)}")

        if items:
            json_file = source_file.rsplit('.', 1)[0] + '.json'
            with open(json_file, 'w', newline='\n') as f:
                json.dump(items, f, indent=2)
                print(f"Create {json_file} success.")
        else:
            print(f"There is no valid macro definition in file {source_file}.")

        items = []

if __name__ == "__main__":
    main()
