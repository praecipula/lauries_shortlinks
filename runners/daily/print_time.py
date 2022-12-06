#!/usr/bin/env python

import sys
import datetime

sys.path.append('./runners/lib')
import persist

from tinydb import TinyDB, Query


Pst = persist.Persist("print_time")

print(datetime.datetime.now(datetime.timezone.utc).isoformat())

Pst.add_db_run()
Pst.truncate_db_runs()
