import sys
sys.path.append('./runners/lib') if './runners/lib' not in sys.path
import models

# Do a real, forced download and initialize, not the idempotent versions.
# Remember, the version stored in GCStorage should be considered the authoritative version.
SqlLiteHandler.download()
SqlLiteHandler.initialize()
models.Log.info("infra", "Database downloaded and initialized successfully")
