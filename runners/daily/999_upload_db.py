#!/usr/bin/env python

import sys
sys.path.append('./runners/lib') if './runners/lib' not in sys.path else sys.path
import models

# If running standalone, so we can add the log.
models.SqlLiteHandler.idempotent_initialize()
# If it doesn't upload... we'll never see the message, since it's not synced to GCStorage
models.Log.info("infra", "Database uploaded successfully")
models.SqlLiteHandler.upload()
