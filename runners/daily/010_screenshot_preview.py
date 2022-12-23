#!/usr/bin/env python

# It's a bit deceptive that this is done daily; rather, it's only really doing the majority of its work
# once a week to save time and commit history space.
# However, I'd like it to _respond_ within the first day, so if the screenshot doesn't
# exist yet it will still create it.

import sys
import os
import glom
sys.path.append('./runners/lib')
import persist
from tinydb import TinyDB, Query
from selenium import webdriver
import base64
import datetime
from urllib.parse import urlparse

Pst = persist.Persist("screenshot_preview")

# Open in read-only mode and find all frontmatter data that has an offline_cache value set to True
frontmatter_db_file = "./runners/data/read_page_frontmatter.json"
fmdb = TinyDB(frontmatter_db_file, access_mode='r')

# Am I really getting any value out of TinyDB here? I'm just getting the last record's data field...
last_run_data = fmdb.all()[-1]['data']
# Find all frontmatter with a matching cache field
def front_matter_filter(page):
    # Check for recursive existence and value matching.
    # This returns false for not existing in that path and
    # for value not matching.

    try:
        offline_cache = glom.glom(page, 'front_matter_data.screenshot')
    except glom.core.PathAccessError as e:
        return False
    return offline_cache

def do_update(page_path):
    # Returns true if no file exists or it's a sunday.
    if (not os.path.exists(page_path)):
        print("Updating because it does not exist yet.")
        return True
    if (datetime.datetime.now().weekday() == 6): # Sunday
        print("Updating because it's Sunday.")
        return True
    print("Not updating.")
    return False


matching_front_matter_pages = filter(front_matter_filter, last_run_data)

screenshot_run_data = []

firefox_options = webdriver.FirefoxOptions()
firefox_options.headless = True
browser = webdriver.Firefox(options=firefox_options)
for page in matching_front_matter_pages:
    page_screenshot_data = {}
    redirect_page = glom.glom(page, 'front_matter_data.redirect')
    print(redirect_page)
    page_screenshot_data['page'] = redirect_page
    url = urlparse(redirect_page)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    fs_safe_path = base64.b64encode(url.path.encode('utf-8')).decode('utf-8', 'strict')
    screenshot_path = f"page_cache/{url.netloc}{fs_safe_path}.png"
    if do_update(screenshot_path):
        browser.get(redirect_page)
        page_screenshot_data['image'] = screenshot_path
        browser.save_screenshot(screenshot_path)
    else:
        page_screenshot_data['pass_until_routine_refresh'] = True
    screenshot_run_data.append(page_screenshot_data)

browser.close()
Pst.add_db_run(screenshot_run_data)
Pst.truncate_db_runs()
