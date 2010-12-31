#!/bin/sh
#
# Ajouter la section suivante dans .hg/hgrc
#
#[hooks]
#commit = ./tag_frame.sh
hg tip --template="{rev}\t{node|short}\t{date|isodate}\t{author}\n" > client/tag.file
