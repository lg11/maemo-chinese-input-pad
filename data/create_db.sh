#!/bin/sh

python convert.py pinyin_table.txt > code_full.txt
python convert.py phrase_pinyin_freq_sc_20090402.txt >> code_full.txt
#python create_db.py
#python create_idx.py
