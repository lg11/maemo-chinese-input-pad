#!/bin/sh

echo create db
sqlite3 cache/db "create table raw_dict ( code char, pinyin varchar, hanzi varchar, freq float ) ;"

echo import file
sqlite3 cache/db ".import cache/sqlite raw_dict"

echo create index
sqlite3 cache/db "create index index_raw_dict on raw_dict ( code ) ;"

