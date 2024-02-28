import argparse
import csv
import re
import sys
from pathlib import Path

# ArgParse config
parser = argparse.ArgumentParser(description="Converts text")
parser.add_argument("in_rules", type=Path, help="path of the rules list")
parser.add_argument("in_text", type=Path, help="path of the input text file")
parser.add_argument("out_text", type=Path, help="path of the output dictionary")
args = parser.parse_args()

in_rules = args.in_rules
in_text = args.in_text
out_text = args.out_text


# Check if output file already exists
if out_text.exists():
    print(f"ERROR: {out_text.name} already exists!")
    sys.exit(1)


# Read rules
rules = []
with open(in_rules, encoding="UTF8") as f:
    csv_reader = csv.reader(f, delimiter=",")
    for row in csv_reader:
        if len(row) != 2:
            print("ERROR: Make sure the rules list only has 2 columns!")
            sys.exit(1)
        old = re.sub(r"\ufeff", r"", row[0])
        new = row[1]
        rules.append((rf"{old}", rf"{new}"))


# Read input text
out_list = []
with open(in_text, encoding="UTF8") as f:
    for line in f:
        new_line = line.strip()

        for old, new in rules:
            new_line = re.sub(old, new, new_line)

        out_list.append(new_line)


# Output text
with open(out_text, "w", encoding="UTF8") as f:
    for line in out_list:
        f.write(f"{line}\n")
