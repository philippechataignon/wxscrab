#!/bin/sh
hg tip --template="{rev}\t{node|short}\t{date|isodate}\t{author}\n" > client/tag.file
