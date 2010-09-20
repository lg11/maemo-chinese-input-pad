#-!- coding=utf-8 -!-

import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect( "main.db" )
    cur = conn.cursor()
    #file = open( "code_full.txt", "r" )

    #buffer = file.readlines()
    
    MAX_CODE_LENGTH = 64
    MAX_CODE_ARREY_LENGTH = 65

    sqls_update_tablet = ""
    for i in range( MAX_CODE_ARREY_LENGTH ):
        for j in range(10):
            p_name = "ci_" + str(i) + "_" + str(j)
            sqls = "create table " + p_name + " ( key integer primary key, code int, pinyin varchar(128), hanzi varchar(64), priority int, update int )"
            print sqls
            #cur.execute( sqls )
            sqls_update_tablet = sqls_update_tablet + "c_" + str(i) + "_" + str(j) + 
    
    #for b in buffer:
        #strs = b[:-1].split("|")
        #print strs
        #i = len(strs[0])
        #if i < 65:
            #p_name = "pc_" + str(i)
            #sqls = "insert into " + p_name + " ( id, code, pinyin, hanzi, freq ) values ( NULL, '" + strs[0] + "', \"" + strs[2] + "\", '" + strs[3] + "', " + strs[4] + ")"
            #print sqls
            #cur.execute( sqls )
    conn.commit()

        

