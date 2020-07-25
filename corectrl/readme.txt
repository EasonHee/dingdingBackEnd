V1.0
1、
完成es_funcitons中的ReportRemoteEs类，
是连接远程elasticsearch的类，暂时完成的是查找功能，
    def search(self, index, title_code="", content="",content_max_length=300, link="",
               start='', size='10', highlight=True, raw = False):
               raw=True返回es返回的数据， raw=False返回处理后的数据

               需要调整的地方：try, exception

2、完成Mysql的添加和查找，
    def findall(self, db, table): //返回表中所有内容
    def find(self, db, table, condition):   //condition为sql语言 where给出条件
    def add(self, db, table, insert_content):   //添加的内容 还没有测试
    add测试成功
3、def an_rpt_updata(cir_bg_time):   //cir_bg_time为每次循环的开始时间，用于判断是否有新数据加入数据库
    成功测试将数据加入到远程es的test索引
