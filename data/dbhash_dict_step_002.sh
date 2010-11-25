#!/bin/sh

echo create db
sqlite3 temp_buffer_003 "create table raw_dict ( code char, pinyin varchar, hanzi varchar, freq float ) ;"

echo import file
sqlite3 temp_buffer_003 ".import temp_buffer_002 raw_dict"

echo create index
sqlite3 temp_buffer_003 "create index index_raw_dict on raw_dict ( code ) ;"

