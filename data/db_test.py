#-!- coding=utf-8 -!-

import sqlite3
import timeit

conn = sqlite3.connect("main.db")
cur = conn.cursor()
#sqls = "select * from pc_6 where code = 944326"
#sqls = "select ROWID,* from ci_6_9 where code = 944326 order by ROWID, id"
#sqls = "select ROWID,* from ci_6_9 where code = 944326 order by code, ROWID"
#sqls = "select ROWID,* from pc_6 where code = 944326 order by freq"
#sqls = "insert into ci_6_9 (code,pinyin,hanzi,priority,update_count) values ('944326',\"zhi'dao\",'纸叨',0,1)"
sqls = "select update_count from update_count where table_name = 'ci_6_9'"

def search( conn, cur ):
    #rl = []
    #sqls = "select * from pc_6 where code = 944326"
    rs = cur.execute( sqls )
    r = rs.fetchone()[0]
    print r
    
    #conn.commit()
    #for r in rs:
        #rl.append(r)

if __name__ == "__main__":
    repeat = 1
    timer = timeit.Timer("db_test.search(db_test.conn,db_test.cur)","import db_test")
    tl =  timer.repeat(repeat,1)
    avg = tl[0]
    for t in tl:
        avg = ( avg + t ) / 2
    print 'sql "' + sqls + '"' + " repeat " + str(repeat) + " time average use " + str(avg) + " second"

