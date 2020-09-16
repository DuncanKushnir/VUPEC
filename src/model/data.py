"""
Utilities for handling I/O
"""

import pandas as pd
from collections import defaultdict

import model.drive_cycles
from util.io import process_subdir_files
from util import locations
import model.parsers as parsers

DATA_FILEEXTS = [".dat", ".vdc"]

raw_parses = process_subdir_files(
    locations.DATA_DIR, parsers.read_file, ext_whitelist=DATA_FILEEXTS
)

# Parse all viable files in subdirectories of /data/
data = defaultdict(dict)
fail = defaultdict(dict)
for dirname, file_results in raw_parses.items():
    for fname, parser in file_results.items():
        for item in parser.result:
            if hasattr(item, "name"):
                if item.name in data[dirname]:
                    print(f"Name Conflict > {dirname}:{item.name} already exists")
                else:
                    data[dirname][item.name] = item
            else:
                fail[dirname][fname] = item

# Resolve symbolic cross links in input data
count = 0
for dirname, results in data.items():
    for key, obj in results.items():
        obj.resolve(data[dirname])

# Resolve subobject cross links in input data
for dirname, results in data.items():
    for key, obj in results.items():
        if hasattr(obj, "_sub_objects"):
            for (target, args) in obj._sub_objects:
                lookup_key = args[0]
                if lookup_key not in data[target]:
                    raise KeyError(
                        f"Can not find {lookup_key} in {target} for "
                        f"inclusion in {dirname}:{key}"
                    )
                setattr(obj, target, data[target][lookup_key])
            del obj["_sub_objects"]


# Report
load_count = sum([1 for dirname, results in data.items() for item in results.values()])
fail_count = sum([1 for dirname, results in fail.items() for item in results.values()])
print(f"----\n{load_count} data items loaded. \n{fail_count} data failures.")
for item, val in data["defaults"].items():
    print(item, val)
"""
print(raw_parses)
print(data)


print(data["drive_cycles"]["edc-15"].duration)
print(data["drive_cycles"]["edc-15"].total_distance)
print(data["drive_cycles"]["eudc"].duration)
print(data["drive_cycles"]["eudc"].total_distance)
print(data["drive_cycles"]["nedc"].duration)
print(data["drive_cycles"]["nedc"].total_distance)
print(data["drive_cycles"]["edc-15"].to_df().head())
print(data["drive_cycles"]["edc-15"].to_df()['delta_d'].sum())
"""
