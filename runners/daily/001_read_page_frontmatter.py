#!/usr/bin/env python

import sys
sys.path.append('./runners/lib')
import persist
from tinydb import TinyDB, Query

import glob
import yaml

Pst = persist.Persist("read_page_frontmatter")

markdown_dir_to_search = ["_get", "_posts", "_short", "_themed_collection"]
markdown_files = []
for d in markdown_dir_to_search:
    markdown_files.extend(glob.glob(f"{d}/*.md", recursive=True))

file_data = []

for file in markdown_files:
    try:
        per_file_data = {}
        per_file_data["filename"] = file
        file_string = open(file).read()
        front_matter_string = file_string.split("---")[1]
        if len(front_matter_string) < 1:
            print(f"No front matter found for {file}")
            continue
        front_matter_data = yaml.safe_load(front_matter_string)
        per_file_data["front_matter_data"] = front_matter_data
        file_data.append(per_file_data)
    except Exception as e:
        print(f"Exception caught during processing of {file}")
        raise

Pst.add_db_run(file_data)
Pst.truncate_db_runs()
