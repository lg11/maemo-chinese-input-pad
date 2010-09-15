#-!- coding=utf-8 -!-

import sqlite3

conn = sqlite3.connect( "main.db" )
cur = conn.cursor()

for i in range(65):
    sqls = "create index idx_pc_" + str(i) + " on pc_" + str(i) + " (code,freq)"
    print sqls
    cur.execute( sqls )
conn.commit()
