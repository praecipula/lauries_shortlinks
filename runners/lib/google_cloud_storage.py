#!/usr/bin/env python

import logging
import os

BUCKETNAME="matt_dot_directory_storage"

from google.oauth2 import service_account
from google.cloud import storage
import json


CREDENTIALS=json.loads(os.environ['CREDENTIALS'])
creds = service_account.Credentials.from_service_account_info(CREDENTIALS)
client = storage.Client(project=CREDENTIALS["project_id"], credentials=creds)

bucket = client.bucket(BUCKETNAME)

testfilename = "testfile.md"
testfilepath = "./" + testfilename


with open(testfilepath, 'rb') as stream:
    blob = bucket.blob(testfilename)
    blob.upload_from_string(stream.read(), testfilename)
    print(blob.public_url)
