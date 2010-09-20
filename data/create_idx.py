#-!- coding=utf-8 -!-

import sqlite3

conn = sqlite3.connect( "main.db" )
cur = conn.cursor()

for i in range(65):
    for j in range(10):
        sqls = "create index idx_ci_code_" + str(i) + "_" + str(j) + " on ci_" + str(i) + "_" + str(j) + " (code)"
        print sqls
        cur.execute( sqls )
        #sqls = "create index idx_ci_pinyin_" + str(i) + "_" + str(j) + " on ci_" + str(i) + "_" + str(j) + " (pinyin)"
        #print sqls
        #cur.execute( sqls )
        sqls = "create index idx_ci_hanzi_" + str(i) + "_" + str(j) + " on ci_" + str(i) + "_" + str(j) + " (hanzi)"
        print sqls
        cur.execute( sqls )
        #sqls = "create index idx_ci_priority_" + str(i) + "_" + str(j) + " on ci_" + str(i) + "_" + str(j) + " (priority)"
        #print sqls
        #cur.execute( sqls )
        #sqls = "create index idx_ci_update_count_" + str(i) + "_" + str(j) + " on ci_" + str(i) + "_" + str(j) + " (update_count)"
        #print sqls
        #cur.execute( sqls )
        
        if i < 7 :
            sqls = "create index idx_zi_code_" + str(i) + "_" + str(j) + " on zi_" + str(i) + "_" + str(j) + " (code)"
            print sqls
            cur.execute( sqls )
            #sqls = "create index idx_zi_pinyin_" + str(i) + "_" + str(j) + " on zi_" + str(i) + "_" + str(j) + " (pinyin)"
            #print sqls
            #cur.execute( sqls )
            sqls = "create index idx_zi_hanzi_" + str(i) + "_" + str(j) + " on zi_" + str(i) + "_" + str(j) + " (hanzi)"
            print sqls
            cur.execute( sqls )
            #sqls = "create index idx_zi_priority_" + str(i) + "_" + str(j) + " on zi_" + str(i) + "_" + str(j) + " (priority)"
            #print sqls
            #cur.execute( sqls )
            #sqls = "create index idx_zi_update_count_" + str(i) + "_" + str(j) + " on zi_" + str(i) + "_" + str(j) + " (update_count)"
            #print sqls
            #cur.execute( sqls )
conn.commit()
