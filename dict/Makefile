
all : dict.0

clean :
	rm -rf cache

cache/stamp :
	mkdir cache
	touch cache/stamp

cache/utf8raw : cache/stamp
	#echo "step 00 : convert raw_dict_file to utf-8"
	iconv -f utf-16 -t utf-8 data/rawdict_utf16_65105_freq.txt > cache/utf8raw


cache/sqlite : cache/utf8raw step_001.py
	#echo "step 01 : phrase utf-8 raw_dict_file to sqlite import format"
	python step_001.py >> cache/log

cache/db : cache/sqlite step_002.sh
	#echo "step 02 : import formated file to sqlite db"
	sh step_002.sh >> cache/log

dict.0 : cache/db step_003.py
	#echo "step 03 : dump raw date to marshal code_map"
	python step_003.py >> cache/log

