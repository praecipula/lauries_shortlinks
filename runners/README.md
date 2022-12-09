# Routine Github Actions runners

This directory contains runners, scripts that are called by Github Actions every so often and/or can be triggered manually.

The reason these are not directly implemented as Github Actions is that we can have more control over them when they are only triggered by GH Actions:

1. They enable us to put a minimum of logic in a location that's more difficult to test locally
1. They are more resilient to environment; i.e. they all run Python with a known pipenv, everywhere
1. They encourage good in-code hygiene

Next runners:

A runner that does a 3-load diff in Selenium to isolate static content (i.e. ads served are almost never interesting)
A runner that diffs static content from a previous run to find changes
  * Price changes / back in stock changes
  * Static snapshots / revision history
  * Offline caching and/or ad-less page loads from GH Pages? (Adless mirror generation)

