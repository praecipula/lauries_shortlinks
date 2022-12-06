#!/usr/bin/env python

import datetime
from tinydb import TinyDB, Query


class Persist:
    def __init__(self, dbname):
        self._dbname = dbname
        self._database = TinyDB("./runners/data/" + self._dbname + ".json", sort_keys=True, indent=2)
        self._keep_runs = 5

    def db(self):
        return self._database

    def truncate_db_runs(self):
        query = Query()
        script_run_data = self.db().search(query.script == self._dbname)
        if len(script_run_data) > self._keep_runs:
            script_run_data.sort(key=lambda d: d['time'])
            overruns = list(map(lambda d:d.doc_id, script_run_data[:-self._keep_runs]))
            print(f"Truncating runs with ids: {overruns}")
            self.db().remove(doc_ids=overruns)
        self.db().close()

    def add_db_run(self, data_to_store=None):
        run_data = {'script': self._dbname, 'time':datetime.datetime.now(datetime.timezone.utc).isoformat(), "data":data_to_store}
        self.db().insert(run_data)

