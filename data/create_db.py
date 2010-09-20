#-!- coding=utf-8 -!-

import sqlite3
import os

if __name__ == "__main__":
    os.system("touch main.db")
    os.system("rm main.db")
    conn = sqlite3.connect( "main.db" )
    cur = conn.cursor()
    conn_old = sqlite3.connect( "main.db.old" )
    cur_old = conn_old.cursor()
    
    MAX_CODE_LENGTH = 64
    MAX_CODE_ARREY_LENGTH = 65

    buffer = file.readlines()
    
    MAX_CODE_LENGTH = 64
    MAX_CODE_ARREY_LENGTH = 65

    sqls_update_tablet = ""
    for i in range( MAX_CODE_ARREY_LENGTH ):
        for j in range(10):
            table_name = "phrase_" + str(i) + "_" + str(j)
            sqls = "create table " + table_name + " ( key integer primary key, code char(" + str(i) + "), pinyin varchar(128), hanzi varchar(64), freq integer, length integer )"
            print sqls
            cur.execute( sqls )
    
    for b in buffer:
        record = b[:-1].split("|")
        #print strs
        i = len(record[0])
        if i < 65:
            table_name = "phrase_" + str(i) + "_" + record[0][0]
            length = record[2].count("'") + 1
            sqls = "insert into " + table_name + " ( key, code, pinyin, hanzi, freq, length ) values ( NULL, '" + record[0] + "', \"" + record[2] + "\", '" + record[3] + "', " + record[4] + ", " + str(length) + " )"
    for i in range( MAX_CODE_ARREY_LENGTH ):
        for j in range(10):

            p_name = "ci_" + str(i) + "_" + str(j)
            sqls = "create table " + p_name + " ( code char(" + str(i) + "), pinyin varchar(128), hanzi varchar(64), priority integer, update_count integer )"
            print sqls
            cur.execute( sqls )

            if i < 7 :
                p_name = "zi_" + str(i) + "_" + str(j)
                sqls = "create table " + p_name + " ( code char(" + str(i) + "), pinyin varchar(128), hanzi varchar(64), priority integer, update_count integer )"
                print sqls
                cur.execute( sqls )

    sqls = "create table update_count ( table_name varchar, update_count integer )"
    print sqls
    cur.execute( sqls )
    
    for i in range( MAX_CODE_ARREY_LENGTH ):
        sqls = "select * from pc_" + str(i) + " order by freq"
        rs = cur_old.execute( sqls )
        priority_zi = []
        priority_ci = []
        for j in range(10):
            priority_zi.append(0)
            priority_ci.append(0)
        for r in rs:
            if r[2].find("'") < 0:
                sqls = "insert into zi_" + str(i) + "_" + r[1][0] + " ( code, pinyin, hanzi, priority, update_count ) values ( '" + r[1] + "', \"" + r[2] + "\", '" + r[3] + "', " + str(priority_zi[int(r[1][0])]) + ", 0 )"
                priority_zi[int(r[1][0])] = priority_zi[int(r[1][0])] + 1
                print sqls
                cur.execute( sqls )
            else:
                sqls = "insert into ci_" + str(i) + "_" + r[1][0] + " ( code, pinyin, hanzi, priority, update_count ) values ( '" + r[1] + "', \"" + r[2] + "\", '" + r[3] + "', " + str(priority_ci[int(r[1][0])]) + ", 0 )"
                priority_ci[int(r[1][0])] = priority_ci[int(r[1][0])] + 1
                print sqls
                cur.execute( sqls )
    for i in range( MAX_CODE_ARREY_LENGTH ):
        for j in range(10):
            sqls = "insert into update_count ( table_name, update_count ) values ( 'ci_" + str(i) + "_" + str(j) + "', 0 )"
            print sqls
            cur.execute( sqls )
            if i < 7:
                sqls = "insert into update_count ( table_name, update_count ) values ( 'zi_" + str(i) + "_" + str(j) + "', 0 )"
                print sqls
                cur.execute( sqls )

    conn.commit()
