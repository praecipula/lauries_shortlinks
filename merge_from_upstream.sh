#!/usr/bin/env bash
#

git checkout -b temp
git add -u
git commit -m "Committing WIP for upstream merge"
git checkout main
git pull
git merge -s ours temp
git branch -d temp
