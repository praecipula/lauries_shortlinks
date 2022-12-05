#!/usr/bin/env python

import datetime

from tinydb import TinyDB, Query


global DB
DB = TinyDB("./runners/data/dailies.json", sort_keys=True, indent=2)

global KEEP_RUNS
KEEP_RUNS=3
def truncate_db_runs():
    global DB
    global KEEP_RUNS
    query = Query()
    script_run_data = DB.search(query.script == 'print_time')    
    if len(script_run_data) > KEEP_RUNS:
        script_run_data.sort(key=lambda d: d['time'])
        print(script_run_data)
        overruns = list(map(lambda d:d.doc_id, script_run_data[:-KEEP_RUNS]))
        print(f"Truncating {overruns}")
        DB.remove(doc_ids=overruns)
        
    DB.close()

def add_db_run():
    global DB
    run_data = {'script':'print_time', 'time':datetime.datetime.today().isoformat()}
    DB.insert(run_data)


print(datetime.date.today().strftime("%Y-%m-%d_%H:%M:%S"))

add_db_run()
truncate_db_runs()
