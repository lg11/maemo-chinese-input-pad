#-!- coding=utf-8 -!-

import string
from marshal import dumps, loads
import dbhash

file = open("buffer_002", "r")
lines = file.readlines()

zi_db = dbhash.open("db_zi", "c")
ci_db = dbhash.open("db_ci", "c")

print "readed"

ci_dict = {}
zi_dict = {}

i = 0
for line in lines:
    #if i < 10:
    i = i + 1
    line = line[:-1]
    line = line.split()
    code = line[1]
    pinyin = line[2]
    hanzi = line[3]
    print i, "/", len(lines), ":", pinyin, hanzi
    if len( hanzi.decode("utf-8") ) == 1 :
        if code in zi_dict.keys():
            pass
        else:
            zi_dict[code] = []
        node = [ pinyin, hanzi ]
        zi_dict[code].append( node )
        print "zi"
    elif len( hanzi.decode("utf-8") ) > 1 :
        if code in ci_dict.keys():
            pass
        else:
            ci_dict[code] = []
        #if len(ci_dict[code]) > 32:
        if len( hanzi.decode("utf-8") ) > 5 :
            print "droped ci"
        else:
            node = [ pinyin, hanzi ]
            ci_dict[code].append( node )
            print "ci"
    else:
        print "error"

print "dict created"

i = 0
for code in zi_dict.keys():
    print i, "/", len(zi_dict.keys()), ":", code
    i = i + 1
    zi_db[code] = dumps( zi_dict[code] )

zi_db.close()


i = 0
for code in ci_dict.keys():
    print i, "/", len(ci_dict.keys()), ":", code
    i = i + 1
    ci_db[code] = dumps( ci_dict[code] )

ci_db.close()
