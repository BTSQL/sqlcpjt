"""
DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),

        ## BT 마리아 DB셋팅 ##
        ##
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'wingstone_db',
        'USER': 'wingstone_root',
        #'PASSWORD': '',
        'PASSWORD': 'dnldtmxhsfnxm',
        'HOST': '127.0.0.1',
        'PORT': '3306',

    }
}
"""

import pymysql, threading, datetime
from multiprocessing import Process
from threading import Thread

from django.db import models
from pjtmgmt import *


mariadb = pymysql.connect(host='127.0.0.1', port=3306, db='wingstone_db', user='wingstone_root',  passwd='dnldtmxhsfnxm')

# server 커서
server_cursor = mariadb.cursor()

global g_cnt
g_cnt = 0

def get_connection(mntdb_list):
    conn_list = []

    # 읽어온 DB 정보를 바탕으로 thread 호출
    for mntserver in mntdb_list:
        print(mntserver[1])
        print(mntserver[2])
        print(mntserver[3])
        print(mntserver[4])
        conn = pymysql.connect(host=mntserver[1], port=int(mntserver[2]), user=mntserver[3], passwd=mntserver[4])
        conn_list.append(conn)

    return conn_list


def set_collector(conn_list, mntdb_list) :
    procs = []


    # 읽어온 DB 정보를 바탕으로 thread 호출
    for i in range(len(mntdb_list)):
        proc = Process(target=collector, args=(mntdb_list[i][0]
                                               , conn_list[i]))

        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    global g_cnt
    g_cnt += 1


    threading.Timer(5.0, set_collector, [conn_list, mntdb_list]).start()


def collector(server_id, conn) :

    # 모니터링 커서
    mnt_cursor = conn.cursor()


    ## 1. Global Status 값 가져 오기

    global_status_sql = """ show global status """
    op_dtm = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
    #op_dtm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    cnt = 0

    mnt_cursor.execute(global_status_sql)

    insert_list = []

    while True:
        data = mnt_cursor.fetchmany(1024)
        if not data :
            break

        for result in data :
            #print(result[0])
            #print(result[1])
            insert = """ INSERT INTO mnt_status_log_%s values ('%s', %d , STR_TO_DATE('%s','%%Y%%m%%d%%H%%i%%S%%f'), '%s', '%s') """ % (server_id, server_id, g_cnt, op_dtm, result[0], str(result[1]))
            server_cursor.execute(insert)
            #print(insert)

    server_cursor.execute("commit")

    get_sql_for_last_time = """
    select IFNULL(MAX(date_format(oper_dtm,'%%Y%%m%%d%%H%%i%%S%%f')),'%s') as last_time
    from mnt_status_log_%s a
    where server_id ='%s'
    order by oper_dtm DESC LIMIT 1
    """ % (op_dtm, server_id, server_id)

    server_cursor.execute(get_sql_for_last_time)
    lasttime = server_cursor.fetchone()[0]

    print(lasttime)

    ## 2. SQL 리스트 가져오기
    slow_log_sql = """
    SELECT   date_format(SK.start_time,'%%Y%%m%%d%%H%%i%%S%%f') as time
						   ,SK.user_host as user_host
						   ,date_format(SK.query_time,'%%H%%i%%S%%f') as query_time
						   ,date_format(SK.lock_time,'%%H%%i%%S%%f') as lock_time
						   ,SK.rows_sent
						   ,SK.rows_examined
						   ,SK.db
						   ,SK.last_insert_id
						   ,SK.insert_id
						   ,SK.server_id
						   ,SK.sql_text
						   ,SK.thread_id
						   ,SK.rows_affected
						   ,SK.SHATEXT
					  FROM (  SELECT sql_text REGEXP 'SELECT?|UPDATE?|DELETE?|INSERT?|MERGE?' AS TTT
									 ,SHA(sql_text) AS SHATEXT
									 ,A.*
							  FROM mysql.slow_log  A
							  WHERE 1 = 1 
							  AND   1 = 1 
							  AND   date_format(start_time,'%%Y%%m%%d%%H%%i%%S%%f') > '%s'
							  ) SK
		 WHERE SK.TTT = 1;  
    """  % (lasttime)

    mnt_cursor.execute(slow_log_sql)

    while True:
        data = mnt_cursor.fetchmany(1024)
        if not data:
            break

        #print(data)

        for result in data:
            query_txt = result[10].replace("'" , "''")
            slow_sql = """ INSERT INTO mnt_slow_log_%s values ('%s',%d,STR_TO_DATE('%s','%%Y%%m%%d%%H%%i%%S%%f'),STR_TO_DATE('%s','%%Y%%m%%d%%H%%i%%S%%f'),'%s','%s','%s', %d, %d, '%s', %d, %d, %d, '%s',%d, %d,'%s' ) 
            """ %( server_id, server_id, g_cnt, op_dtm, result[0], result[1], result[2], result[3], result[4], result[5],
                   result[6], result[7], result[8], result[9], query_txt, result[11], result[12], result[13])

            server_cursor.execute(slow_sql)


    server_cursor.execute('commit')

    process_list_sql = " SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST; "

    mnt_cursor.execute(process_list_sql)

    print("--------------------processlist ------------------------")
    while True:
        data = mnt_cursor.fetchmany(1024)
        if not data:
            break

        #print(data)

        print(data)
        for result in data:

            process_sql = """ INSERT INTO mnt_processlist_%s values ('%s',%d,STR_TO_DATE('%s','%%Y%%m%%d%%H%%i%%S%%f'),%d,'%s','%s','%s',
            '%s',%d, '%s','%s', %d, %d, %d, %d, %d, %d, '%s', %d) 
            """ % (server_id, server_id, g_cnt, op_dtm, result[0], result[1], result[2], result[3], result[4], result[5],
                   result[6], result[7], result[8],result[9], result[10], result[11], result[12], result[13], result[14],
                   result[16], result[15])
            print(process_sql)

            server_cursor.execute(process_sql)

    server_cursor.execute('commit')

    print("--------------------processlist end ------------------------")

    reponse_time_sql = "SELECT time, count, total FROM INFORMATION_SCHEMA.QUERY_RESPONSE_TIME"
    mnt_cursor.execute(reponse_time_sql)

    print("--------------------reponse time ------------------------")
    while True:
        data = mnt_cursor.fetchmany(1024)
        if not data:
            break


        for result in data:
            process_sql = """ INSERT INTO mnt_response_time_%s values ('%s',%d,STR_TO_DATE('%s','%%Y%%m%%d%%H%%i%%S%%f'),'%s',%d,'%s') 
                """ % (server_id, server_id, g_cnt, op_dtm, result[0], result[1], result[2])

            server_cursor.execute(process_sql)

    server_cursor.execute('commit')

    print("--------------------reponse time end ------------------------")

    mnt_cursor.close()



    """
    performance 스키마는 수집이 필요  
    마리아DB 5.5 이상에서 사용가능 
    1. 모니터링 데이터를 수집하기 전에 performance_schema=on (my.cnf 파일) 을 해야 한다. * runtime execution is X
       mysqld --verbose --help | grep -A 1 'Default options'
       /etc/my.cnf /etc/mysql/my.cnf ~/.my.cnf 
       sudo service mysql restart
       
    2.  status  수집필요
    3.  sql 및 실행계획 수집 필요 
    """

try :



    test_sql = """
               select id as server_id
                     ,db_server_ip as ip
                     ,db_access_port as port
                     ,db_acnt_id as anct_id
                     ,db_acnt_pwd as pwd
               from pjtmgmt_mntserver
               where is_available = 1
               """
    mntdb_list = []

    server_cursor.execute(test_sql)
    while True:
        data = server_cursor.fetchmany(100)
        if not data :
            break

        for result in data :
            mntdb_list.append(result)

    for mntserver in mntdb_list:
        ddl_log_tbl_txt = """
        create table if not exists mnt_status_log_%s 
            ( mnt_server_id varchar(20) not null ,
            mnt_oper_cnt decimal not null,
            mnt_oper_dtm timestamp(6) not null,
            mnt_col_name varchar(100) not null,
            mnt_status varchar(50) not null
            )
            """ % (mntserver[0])

        ddl_log_index_txt = """
        create index if not exists mnt_status_index_%s on mnt_status_log_%s (mnt_server_id, mnt_oper_dtm , mnt_col_name, mnt_status)
            """ % (mntserver[0], mntserver[0])

        ddl_slow_log = """
        create table if not exists mnt_slow_log_%s
        ( mnt_server_id varchar(20) not null ,
          mnt_oper_cnt decimal not null,
          mnt_oper_dtm date not null,
          start_time timestamp(6) not null , 
          user_host mediumtext not null ,
          query_time time(6) not null, 
          lock_time time(6)  not null,            
          rows_sent int(11)  not null,            
          rows_examined int(11) not null,             
          db           varchar(512) not null,        
          last_insert_id int(11)   not null,           
          insert_id      int(11)   not null,           
          server_id      int(10) unsigned  not null,   
          sql_text       mediumtext not null,          
          thread_id      bigint(21) unsigned  not null, 
          rows_affected  int(11) not null,
          sha_text       mediumtext not null
         )
        """ % (mntserver[0])

        ddl_reponse_time = """
        create table if not exists mnt_response_time_%s
        ( 
          mnt_server_id varchar(20) not null ,
          mnt_oper_cnt decimal not null,
          mnt_oper_dtm date not null,
          time varchar(14) not null ,
          count int(11) unsigned not null,
          total varchar(14) not null 
        )
        """ % (mntserver[0])

        ddl_processlist = """
        create table if not exists mnt_processlist_%s
        ( 
            mnt_server_id varchar(20) not null ,
            mnt_oper_cnt decimal not null,
            mnt_oper_dtm date not null,
            ID	bigint(4)	not null,
            USER	varchar(128)	not null,
            HOST	varchar(64)	not null,
            DB	varchar(64)	null,
            COMMAND	varchar(16)	not null,
            TIME	int(7)	not null,
            STATE	varchar(64)	null,
            INFO	longtext	null,
            TIME_MS	decimal(22,3)	not null,
            STAGE	tinyint(2)	null,
            MAX_STAGE	tinyint(2)	not null,
            PROGRESS	decimal(7,3)	not null,
            MEMORY_USED	int(7)	null,
            EXAMINED_ROWS	int(7)	not null,
            QUERY_ID	bigint(4)	not null,
            INFO_BINARY	blob	null,
            TID	bigint(4)	not null 
        )
        """ % (mntserver[0])

        server_cursor.execute(ddl_log_tbl_txt)
        server_cursor.execute(ddl_log_index_txt)
        server_cursor.execute(ddl_slow_log)
        server_cursor.execute(ddl_reponse_time)
        server_cursor.execute(ddl_processlist)


    print("test1")

    conn_list = get_connection(mntdb_list)

    print("test2")

    set_collector(conn_list, mntdb_list)

    print("test3")

except Exception as e:
    print('collector error')
    print(e)





