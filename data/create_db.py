#-!- coding=utf-8 -!-

import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect( "main.db" )
    cur = conn.cursor()
    file = open( "code_full.txt", "r" )

    buffer = file.readlines()

    phrase_list = []
    for i in range(65):
        p_name = "pc_" + str(i)
        phrase_list.append( p_name )
        sqls = "create table " + p_name + " ( code char(" + str(i) + "), pinyin varchar(128), hanzi varchar(64), freq int )"
        print sqls
        cur.execute( sqls )
    
    for b in buffer:
        strs = b[:-1].split("|")
        #print strs
        i = len(strs[0])
        if i < 65:
            p_name = "pc_" + str(i)
            sqls = "insert into " + p_name + " ( code, pinyin, hanzi, freq ) values ( '" + strs[0] + "', \"" + strs[2] + "\", '" + strs[3] + "', " + strs[4] + ")"
            print sqls
            cur.execute( sqls )
    conn.commit()

        

