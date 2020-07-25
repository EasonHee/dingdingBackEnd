import pymysql

class ReportLocalDB():

    def __init__(self, db, user="root", password="123456", port=3306, host="localhost"):
        self.db = pymysql.connect(host=host, user=user, password=password, port=port, db=db)
        self.cursor=self.db.cursor()

    #增
    def add(self, db, table, insert_content):
        sql = "insert into `{0}`.`{1}`".format(db, table)
        sql = sql + insert_content
        self.cursor.execute(sql)
        self.db.commit()
        return True

    #删
    def delete(self):
        pass

    #改
    def updata(self):
        pass

    #查
    def findall(self, db, table):
        sql = "select * from `{0}`.`{1}`".format(db, table)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def find(self, db, table, condition):
        sql = "select * from `{0}`.`{1}`".format(db, table)
        sql = sql+condition
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

import time
if __name__ == "__main__":
    db = ReportLocalDB("sh", "root", "123456")
    condition = "where date = {0}".format(1595065225.62821)
    result = db.find("sh", "sh_annual", condition=condition)
    print(result)