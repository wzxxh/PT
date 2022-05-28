"""
文件名：本地Sqilte.py
用途：存储数据到本地sqlite3 数据库，并提供查询功能

"""
import sqlite3

class Nativedb:
    def __init__(self):
        self.dbname = "./data/database.db"
        self.error_log_file = './log/'
        self.error_log_file_name = 'error_store_data_to_sqlilte3.log'
        self.__check_dbfile()


    def __check_dbfile(self):
        sqls = [
                """create table if not exists 签到记录
                   (ID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    网站名        TEXT     NULL,
                    时间     DATETIME    NULL,
                    用户等级     TEXT    NULL,
                    用户名     TEXT      NULL,
                    魔力值   TEXT        NULL,
                    分享率  TEXT        NULL,
                    上传量   TEXT        NULL,
                    下载量   TEXT        NULL,
                    当前做种   TEXT        NULL,
                    当前下载   TEXT        NULL,
                    是否可连接  TEXT        NULL,
                    连接数      TEXT        NULL,
                    是否已签到   TEXT        NULL,
                    签到是否成功   INTEGER    NULL,
                    日志          TEXT       NULL);""",
                """create table if not exists 网站列表
                   (ID  INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    网站名        TEXT UNIQUE    NOT NULL);"""           
                ]
        for sql in sqls:
            self.store(sql)
        return

    def store(self,SQL,param=None):
        flag = False
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        try:
            if param:
                cur.execute(SQL,param)
            else:
                cur.execute(SQL)
            con.commit()
        except:
            print('sqlite更新数据失败,SQL为：',SQL)
        else:
            flag = True
        finally:
            con.close()
        return flag
           
            
    def select(self,SQL,param = None):
        con = sqlite3.connect(self.dbname)
        cur = con.cursor()
        try:
            cur.execute(SQL,param)
            data = cur.fetchall()
        finally:
            con.close()
        return data if data != [] else None

    def 保存数据(self,data):
        sql1 = 'insert or ignore into 网站列表 (网站名) values (?) '
        param1 = (data['网站名'],)

        sql2 = 'insert into 签到记录 (网站名,时间,用户等级,用户名,魔力值,分享率,上传量,下载量,当前做种,当前下载,是否可连接,连接数,是否已签到,签到是否成功,日志) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
        param2 = ( data['网站名'],data['时间'],data['用户等级'],data['用户名'],data['魔力值'],data['分享率'],data['上传量'],data['下载量'],data['当前做种'],
                    data['当前下载'],data['是否可连接'],data['连接数'],data['是否已签到'],data['签到是否成功'],data['日志'] )
        try:
            self.store(sql1,param1)
            self.store(sql2,param2)
        except:
            error_file_path = self.error_log_file + str(data['时间']) + ' ' + self.error_log_file_name
            with open(error_file_path,'w') as file:
                file.write( str( data ) )
        
