#!/bin/sh
git describe --tags > client/tag.file 
git log -1 --format="%ai" >> client/tag.file
