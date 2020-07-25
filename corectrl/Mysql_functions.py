import pymysql

class ReportLocalDB():

    def __init__(self, db, user="root", password="123456", port=3306, host="localhost"):
        self.db = pymysql.connect(host=host, user=user, password=password, port=port, db=db)
        self.cursor=self.db.cursor()

    #增
    def add(self, db, table, insert_content):
        try:
            sql = "insert into `{0}`.`{1}`".format(db, table)
            sql = sql + insert_content
            self.cursor.execute(sql)
            self.db.commit()
            return True
        except:
            print("数据库添加失败\n")

    #删
    def delete(self):
        pass

    #改
    def updata(self):
        pass

    #查
    def findall(self, db, table):
        try:
            sql = "select * from `{0}`.`{1}`".format(db, table)
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            print("查找表所有数据失败")

    def find(self, db, table, condition):
        try:
            sql = "select * from `{0}`.`{1}`".format(db, table)
            sql = sql+condition
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except:
            print("查找单个数据失败\n")

import time
if __name__ == "__main__":
    rpt = ReportLocalDB("world", "root", "123456")
    sql = "(`id`, `name`, `title`) values(5, 'tf', 'jj')"
    rpt.add("world", "books", sql)
    rpt.db.commit()
