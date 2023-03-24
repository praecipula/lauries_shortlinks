#!/usr/bin/env python

import sys
sys.path.append('./runners/lib')

import yaml
import google_cloud_storage
from models import SqlLiteHandler, LPage, PageMetadata

import logging
import python_logging_base

from sqlalchemy import select

logger = logging.getLogger("scan_files")
logger.setLevel(logging.DEBUG)

SqlLiteHandler.idempotent_download()
SqlLiteHandler.idempotent_initialize()

query = select(LPage).where(LPage.trashed == False)
results = SqlLiteHandler.session().execute(query)

for (page,) in results:
    print(page)
    try:
        file_string = open(page.path).read()
        front_matter_string = file_string.split("---")[1]
        if len(front_matter_string) < 1:
            print(f"No front matter found for {file}")
            continue
        front_matter_data = yaml.safe_load(front_matter_string)
        PageMetadata.upsert_or_trash_all_by_page(page, front_matter_data)
    except Exception as e:
        print(f"Exception caught during frontmatter processing of {page.path}")
        raise

