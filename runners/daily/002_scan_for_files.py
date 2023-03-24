#!/usr/bin/env python
import sys
sys.path.append('./runners/lib') if './runners/lib' not in sys.path else sys.path
import glob
import google_cloud_storage
from models import SqlLiteHandler, LPage

import logging
import python_logging_base

from sqlalchemy import select

logger = logging.getLogger("scan_files")
logger.setLevel(logging.DEBUG)

# Do we need this every script if they are intended to be standalone-runnable, i.e. no code dependency, only
# state in the DB we hope is refreshed?
SqlLiteHandler.idempotent_download()
SqlLiteHandler.idempotent_initialize()


markdown_dir_to_search = ["_get", "_posts", "_short", "_themed_collection"]
markdown_files = []
for d in markdown_dir_to_search:
    markdown_files.extend(glob.glob(f"{d}/*.md", recursive=True))

for file in markdown_files:
    LPage.upsert(file)

# Now all the pages should be in the DB and we can work with that instead of FS scans.
