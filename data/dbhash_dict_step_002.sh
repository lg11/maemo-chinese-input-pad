#!/bin/sh

touch temp_buffer_004
rm temp_buffer_004

echo create db
sqlite3 temp_buffer_004 "create table raw_dict_zi ( code int, pinyin char[], hanzi char[], freq float ) ;"
sqlite3 temp_buffer_004 "create table raw_dict_ci ( code int, pinyin char[], hanzi char[], freq float ) ;"

echo import file
sqlite3 temp_buffer_004 ".import temp_buffer_002 raw_dict_zi"
sqlite3 temp_buffer_004 ".import temp_buffer_003 raw_dict_ci"

echo create index
sqlite3 temp_buffer_004 "create index index_raw_dict_zi on raw_dict_zi ( code ) ;"
sqlite3 temp_buffer_004 "create index index_raw_dict_ci on raw_dict_ci ( code ) ;"

