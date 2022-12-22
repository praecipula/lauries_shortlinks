#!/usr/bin/env bash

# This exists because there are files (like screenshots, records of runs) in the upstream repo that get created as a part of nightly runs.
# This means we often find merge issues when pulling down (but why, if there aren't conflicts? Investigate.
#
# This is how we will merge in the remote and re-merge on top of it.
#
#https://stackoverflow.com/questions/4911794/git-command-for-making-one-branch-like-another/4912267#4912267
