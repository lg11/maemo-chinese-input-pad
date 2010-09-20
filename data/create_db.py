#-!- coding=utf-8 -!-

import sqlite3
import os

if __name__ == "__main__":
    os.system("touch main.db")
    os.system("rm main.db")
    conn = sqlite3.connect( "main.db" )
    cur = conn.cursor()
    file = open( "code_full.txt", "r" )

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
            print sqls
            cur.execute( sqls )
    conn.commit()

        

