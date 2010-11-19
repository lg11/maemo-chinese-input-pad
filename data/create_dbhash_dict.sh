#!/bin/sh

touch log

touch temp_buffer_001
touch temp_buffer_002
touch temp_buffer_003
rm temp_buffer_001
rm temp_buffer_002
rm temp_buffer_003

echo "step 00 : convert raw_dict_file to utf-8"
iconv -f utf-16 -t utf-8 rawdict_utf16_65105_freq.txt > temp_buffer_001
echo "step 01 : phrase utf-8 raw_dict_file to sqlite import format"
python dbhash_dict_step_001.py >> log
echo "step 02 : import formated file to sqlite db"
sh dbhash_dict_step_002.sh >> log
echo "step 03 : dump raw date to marshal data"
python dbhash_dict_step_003.py >> log

#python ./google_pinyin_dict_convert_step_002.py > log
