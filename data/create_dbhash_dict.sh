#!/bin/sh

touch log

touch temp_buffer_001
touch temp_buffer_002
touch temp_buffer_003
touch temp_buffer_004
touch dict.0
touch dict.1
touch dict.2
touch dict.tar.gz
rm temp_buffer_001
rm temp_buffer_002
rm temp_buffer_003
rm temp_buffer_004
rm dict.0
rm dict.1
rm dict.2
rm dict.tar.gz

echo "step 00 : convert raw_dict_file to utf-8"
iconv -f utf-16 -t utf-8 rawdict_utf16_65105_freq.txt > temp_buffer_001
echo "step 01 : phrase utf-8 raw_dict_file to sqlite import format"
python dbhash_dict_step_001.py >> log
echo "step 02 : import formated file to sqlite db"
sh dbhash_dict_step_002.sh >> log
echo "step 03 : dump raw date to marshal code_map"
python dbhash_dict_step_003.py >> log
#echo "step 04 : gen incomplete code set"
#python dbhash_dict_step_004.py >> log

touch temp_buffer_001
touch temp_buffer_002
touch temp_buffer_003
touch temp_buffer_004
rm temp_buffer_001
rm temp_buffer_002
rm temp_buffer_003
rm temp_buffer_004
#tar -zcvf dict.tar.gz dict.0 dict.1 dict.2
