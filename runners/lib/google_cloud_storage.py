#!/usr/bin/env python

import logging
import os


from google.oauth2 import service_account
from google.cloud import storage
from google.api_core.exceptions import NotFound
import json


BUCKETNAME="matt_dot_directory_storage"
CREDENTIAL_JSON=json.loads(os.environ['CREDENTIALS'])

# Common module variables
credentials = service_account.Credentials.from_service_account_info(CREDENTIAL_JSON)
client = storage.Client(project=CREDENTIAL_JSON["project_id"], credentials=credentials)
bucket = client.bucket(BUCKETNAME)

def upload(blobname, filepath):
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filepath)
    print(f"Uploaded file to {blob.public_url}")

def download(blobname, destination_filepath):
    blob = bucket.blob(blobname)
    blob.download_to_filename(destination_filepath)
    filestat = os.stat(destination_filepath)
    print(f"Downloaded {filestat.st_size} bytes to {destination_filepath}")

def list_blobs():
    return client.list_blobs(BUCKETNAME)

