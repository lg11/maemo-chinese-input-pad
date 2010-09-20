#-!- coding=utf-8 -!-

import sqlite3

conn = sqlite3.connect( "main.db" )
cur = conn.cursor()

for i in range(65):
    for j in range(10):
        sqls = "create index idx_code_phrase_" + str(i) + "_" + str(j) + " on phrase_" + str(i) + "_" + str(j) + " (code)"
        print sqls
        cur.execute( sqls )
        #sqls = "create index idx_pinyin_phrase_" + str(i) + "_" + str(j) + " on phrase_" + str(i) + "_" + str(j) + " (pinyin)"
        #print sqls
        #cur.execute( sqls )
        #sqls = "create index idx_hanzi_phrase_" + str(i) + "_" + str(j) + " on phrase_" + str(i) + "_" + str(j) + " (hanzi)"
        #print sqls
        #cur.execute( sqls )
conn.commit()
