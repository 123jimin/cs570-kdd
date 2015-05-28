#!/usr/bin/env bash

pg_restore -Fc -U postgres -n public -d kdd2013authorpaperidentification data/raw/dataRev2.postgres
