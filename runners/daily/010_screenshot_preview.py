#!/usr/bin/env python

import sys
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
    browser.get(redirect_page)
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    fs_safe_path = base64.b64encode(url.path.encode('utf-8')).decode('utf-8', 'strict')
    screenshot_path = f"page_cache/{url.netloc}{fs_safe_path}.png"
    page_screenshot_data['image'] = screenshot_path
    screenshot_run_data.append(page_screenshot_data)
    browser.save_screenshot(screenshot_path)

browser.close()
Pst.add_db_run(screenshot_run_data)
Pst.truncate_db_runs()
