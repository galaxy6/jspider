# -*- encoding:utf8 -*- 

import MySQLdb 
  
class db(object):

    def __init__(self):
        """
        初始化数据
        参数db_host：连接数据库主机
        参数db_port: 连接数据库端口
        参数db_user: 连接数据库用户
        参数db_password:  连接数据库密码
        参数db_name: 连接数据库名字
        """

        self.db_host = "localhost" 
        self.db_port = 3306
        self.db_user = "root" 
        self.db_password= "xxxxxx" 
        self.db_name = "xxxxxx"
        self.conn = self.getConnection() 
  
    def getConnection(self):
        """
        连接数据库函数
        """
        return MySQLdb.Connect( 
                           host=self.db_host,
                           port=self.db_port,
                           user=self.db_user,
                           passwd=self.db_password,
                           db=self.db_name,
                           charset='utf8'
                           ) 
  
    def query(self, sqlString):
        """
        查询数据库函数
        参数sqlString:查询的数据库sql语句
        """
        cursor=self.conn.cursor() 
        cursor.execute(sqlString) 
        returnData=cursor.fetchone() 
        cursor.close() 
        self.conn.close() 
        return returnData 
      
    def update(self, sqlString): 
        """
        数据库更新函数，可以继续数据插入
        参数sqlString: 操作的数据库sql语句
        """
        cursor=self.conn.cursor() 
        cursor.execute(sqlString)
        cursor.close() 
        self.conn.commit() 
       	self.conn.close()
