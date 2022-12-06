#!/usr/bin/env python

import sys
import datetime

sys.path.append('./runners/lib')
import persist

from tinydb import TinyDB, Query


Pst = persist.Persist("print_time")

print(datetime.date.today().strftime("%Y-%m-%d_%H:%M:%S"))

Pst.add_db_run()
Pst.truncate_db_runs()
