#!/bin/sh

python ./google_pinyin_dict_convert_step_001.py > buffer_001
cat buffer_001 | sort -rn > buffer_002
python ./google_pinyin_dict_convert_step_002.py > log
