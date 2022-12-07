## Naming conventions

The files in this directory are named sort of like old-timey Linux boot files in that they are sorted and loaded/run alphabetically; therefore, if there is a dependency (script B needs to run after script A writes to a DB) then that should be encoded in the filename to ensure the scripts run correctly.

Not the most sophisticated way to implement this, but it works for now.
