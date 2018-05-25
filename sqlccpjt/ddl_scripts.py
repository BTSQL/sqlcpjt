import pymysql



try :
    mariadb = pymysql.connect(host='127.0.0.1', port=3306, db='wingstone_db', user='wingstone_root',  passwd='dnldtmxhsfnxm')

    test_sql = """
               show global status
               """
    cursor = mariadb.cursor()
    col_list = []

    cursor.execute(test_sql)
    while True:
        data = cursor.fetchmany(100)
        if not data :
            break

        for col in data :
            col_list.append(col[0])


    for col in col_list :
        sql = "INSERT INTO mnt_columns_info VALUES ( '%s' ,'Y')"%(col)
        #print(sql)
        cursor.execute(sql)

    cursor.execute("commit")

    cursor.close()


except Exception as e:
    print (e)
    print('ddl error')


