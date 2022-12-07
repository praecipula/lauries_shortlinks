#!/usr/bin/env python

import sys
sys.path.append('./runners/lib')
import glom
import persist
from tinydb import TinyDB, Query


Pst = persist.Persist("offline_page_cache")

# Open in read-only mode and find all frontmatter data that has an offline_cache value set to True
frontmatter_db_file = "./runners/data/read_page_frontmatter.json"
fmdb = TinyDB(frontmatter_db_file, access_mode='r')

# Am I really getting any value out of TinyDB here? I'm just getting the last record's data field...
last_run_data = fmdb.all()[-1]['data']
# Find all frontmatter with a matching cache field
def front_matter_filter(page):
    print(page)
    # Check for recursive existence and value matching.
    # This returns false for not existing in that path and
    # for value not matching.

    try:
        offline_cache = glom.glom(page, 'front_matter_data.offline_cache')
    except glom.core.PathAccessError as e:
        return False
    return offline_cache


matching_front_matter_pages = filter(front_matter_filter, last_run_data)
print(list(matching_front_matter_pages))

# TODO: get the page with Selenium

#Pst.add_db_run(file_data)
#Pst.truncate_db_runs()
