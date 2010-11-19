#!/bin/sh

touch dict.db
rm dict.db

sqlite3 dict.db "create table raw_dict_zi ( code int, pinyin char[], hanzi char[], freq float ) ;"
sqlite3 dict.db "create table raw_dict_ci ( code int, pinyin char[], hanzi char[], freq float ) ;"
sqlite3 dict.db ".import temp_buffer_002 raw_dict_zi"
sqlite3 dict.db ".import temp_buffer_003 raw_dict_ci"
sqlite3 dict.db "create index index_raw_dict_zi on raw_dict_zi ( code ) ;"
sqlite3 dict.db "create index index_raw_dict_ci on raw_dict_ci ( code ) ;"

