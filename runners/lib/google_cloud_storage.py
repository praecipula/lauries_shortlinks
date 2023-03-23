#!/usr/bin/env python

import logging

BUCKETNAME="matt_dot_directory_storage"

from google.cloud import storage

client = storage.Client().from_service_account_json("/Users/matt/Downloads/future-medley-249022-ec5906f38fd6.json")

bucket = client.bucket(BUCKETNAME)

testfilename = "testfile.md"
testfilepath = "./" + testfilename


with open(testfilepath, 'rb') as stream:
    blob = bucket.blob(testfilename)
    blob.upload_from_string(stream.read(), testfilename)
    blob.make_public()
    print(blob.public_url)
