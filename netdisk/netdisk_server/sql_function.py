import mysql.connector
import base64, os

class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None

    def create_user_table(self):
        try:
            cursor = self.conn.cursor()
            create_table_sql = '''
            CREATE TABLE IF NOT EXISTS user_storage (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                phone_num VARCHAR(255) NOT NULL,
                public_key TEXT
            )
            '''
            cursor.execute(create_table_sql)
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close(self):
        if self.conn:
            self.conn.close()

class User:
    def __init__(self, conn, username=None, password=None, phone_num=None, public_key=None, verify_num=None):
        self.conn = conn
        self.username = username
        self.password = password
        self.phone_num = phone_num
        self.public_key = public_key
        self.verify_num = verify_num

    def register_user(self):
        if not self.user_exists():
            try:
                cursor = self.conn.cursor()
                insert_user_sql = '''
                INSERT INTO user_storage (username, password, phone_num, public_key)
                VALUES (%s, %s, %s, %s)
                '''
                cursor.execute(insert_user_sql, (self.username, self.password, self.phone_num, self.public_key))
                self.conn.commit()
                cursor.close()
                # self.create_user_files_table()
                print("User registered successfully.")
            except mysql.connector.Error as err:
                print(f"Error: {err}")
        else:
            print("User already exists.")

    def user_exists(self):
        try:
            cursor = self.conn.cursor()
            query_user_sql = '''
            SELECT username FROM user_storage WHERE phone_num = %s
            '''
            cursor.execute(query_user_sql, (self.phone_num,))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def user_login_exists(self):
        try:
            cursor = self.conn.cursor()
            query_user_sql = '''
            SELECT username FROM user_storage WHERE username = %s and password = %s
            '''
            cursor.execute(query_user_sql, (self.username, self.password))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def create_user_files_table(self):
        try:
            cursor = self.conn.cursor()
            create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS user_files_{self.username} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL,
                file_data LONGBLOB,
                UNIQUE KEY (file_name)
            )
            '''
            cursor.execute(create_table_sql)
            self.conn.commit()
            cursor.close()
            print("create successful")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            
    def get_user_info_by_phone_num(self, phone_num):
        user_info = {}
        try:
            cursor = self.conn.cursor()
            # 查询用户表单中的相关信息
            query_user_info_sql = '''
            SELECT username, password, public_key
            FROM user_storage
            WHERE phone_num = %s
            '''
            cursor.execute(query_user_info_sql, (phone_num,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                user_info['username'] = result[0]
                user_info['password'] = result[1]
                user_info['public_key'] = result[2]
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        return user_info

    def store_user_file(self, file_name):
        try:

            with open(file_name, 'rb') as file:
                file_content = base64.b64encode(file.read()).decode('utf-8')

            file_name = os.path.basename(file_name)
            cursor = self.conn.cursor()
            insert_file_sql = f'''
            INSERT INTO user_files_{self.username} (file_name, file_data)
            VALUES (%s, %s)
            '''
            cursor.execute(insert_file_sql, (file_name, file_content))
            self.conn.commit()
            cursor.close()

            print("store successful")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_user_file(self, file_name):
        try:
            cursor = self.conn.cursor()
            query_file_sql = f'''
            SELECT file_data FROM user_files_{self.username} WHERE file_name = %s
            '''
            cursor.execute(query_file_sql, (file_name,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
            
    def get_user_file_names(self):
        try:
            cursor = self.conn.cursor()
            query_file_names_sql = f'''
            SELECT file_name FROM user_files_{self.username}
            '''
            cursor.execute(query_file_names_sql)
            result = cursor.fetchall()
            cursor.close()
            return [row[0] for row in result]
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return []
    def delete_user_file(self, file_name):
        try:
            cursor = self.conn.cursor()
            # 删除用户表单中的文件
            delete_file_sql = f'''
            DELETE FROM user_files_{self.username}
            WHERE file_name = %s
            '''
            cursor.execute(delete_file_sql, (file_name,))
            self.conn.commit()
            cursor.close()
            return 1
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 0
class Group:
    def __init__(self, conn=None, group_id=None, leader_username=None, leader_phone_num=None, leader_public_key=None):
        self.conn = conn
        self.group_id = group_id
        self.leader_username = leader_username
        self.leader_phone_num = leader_phone_num
        self.leader_public_key = leader_public_key

    def create_group_number_table(self):
        try:
            cursor = self.conn.cursor()
            create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS group_number_{self.group_id} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) NOT NULL UNIQUE,
                phone_num VARCHAR(255) NOT NULL,
                public_key TEXT
            )
            '''
            cursor.execute(create_table_sql)
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def create_group_files_table(self):
        try:
            cursor = self.conn.cursor()
            create_table_sql = f'''
            CREATE TABLE IF NOT EXISTS group_files_{self.group_id} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                file_name VARCHAR(255) NOT NULL UNIQUE,
                file_data LONGBLOB
            )
            '''
            cursor.execute(create_table_sql)
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def add_member(self, username, phone_num, public_key):
        try:
            cursor = self.conn.cursor()
            insert_member_sql = f'''
            INSERT INTO group_number_{self.group_id} (username, phone_num, public_key)
            VALUES (%s, %s, %s)
            '''
            cursor.execute(insert_member_sql, (username, phone_num, public_key))
            self.conn.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # 查询用户所在的所有用户组的ID
    def get_user_groups(self, phone_num):
        user_groups = []
        try:
            cursor = self.conn.cursor()
            # 获取所有用户组表单的名称
            cursor.execute("SHOW TABLES LIKE 'group_number_%'")
            group_tables = cursor.fetchall()

            for table in group_tables:
                group_table_name = table[0]
                # 查询表单中是否存在具有给定电话号码的用户
                query_user_sql = f'''
                SELECT username FROM {group_table_name} WHERE phone_num = %s
                '''
                cursor.execute(query_user_sql, (phone_num,))
                result = cursor.fetchone()
                if result:
                    group_id = group_table_name.split('_')[2]  # 从表单名称中提取组ID
                    # print(group_table_name.split('_')[1], group_table_name.split('_')[2])
                    user_groups.append(f'group_{group_id}')

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
        return user_groups


    # 查询用户组共享文件表单中的所有文件名
    def get_group_shared_file_names(self):
        shared_file_names = []
        try:
            cursor = self.conn.cursor()
            group_files_table_name = f'group_files_{self.group_id}'
            if self.table_exists(group_files_table_name):
                
                cursor.execute(f"SELECT file_name FROM {group_files_table_name}")
                result = cursor.fetchall()
                shared_file_names = [row[0] for row in result]

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        return shared_file_names

    def table_exists(self, table_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"SHOW TABLES LIKE %s", (table_name,))
            result = cursor.fetchone()
            cursor.close()
            return result is not None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
    
    
    def store_group_file(self, file_name):
        try:
            with open(file_name, 'rb') as file:
                file_content = base64.b64encode(file.read()).decode('utf-8')

            file_name = os.path.basename(file_name)
            cursor = self.conn.cursor()
            insert_file_sql = f'''
            INSERT INTO group_files_{self.group_id} (file_name, file_data)
            VALUES (%s, %s)
            '''
            cursor.execute(insert_file_sql, (file_name, file_content))
            self.conn.commit()
            cursor.close()
            
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_group_file(self, file_name):
        try:
            cursor = self.conn.cursor()
            query_file_sql = f'''
            SELECT file_data FROM group_files_{self.group_id} WHERE file_name = %s
            '''
            cursor.execute(query_file_sql, (file_name,))
            result = cursor.fetchone()
            cursor.close()
            if result:
                return result[0]
            else:
                return None
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None
        
    def delete_group_shared_file(self, group_id, file_name):
        try:
            cursor = self.conn.cursor()
            group_files_table_name = f'group_files_{group_id}'
            # 删除群组共享表单中的文件
            delete_file_sql = f'''
            DELETE FROM {group_files_table_name}
            WHERE file_name = %s
            '''
            cursor.execute(delete_file_sql, (file_name,))
            self.conn.commit()
            cursor.close()
            return 1
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 0
        
    def get_user_public_key_in_group(self, group_id, username):
        user_public_key = None
        try:
            cursor = self.conn.cursor()
            group_table_name = f'group_number_{group_id}'
            # 查询群组用户信息表单中的用户公钥
            query_user_public_key_sql = f'''
            SELECT public_key FROM {group_table_name}
            WHERE username = %s
            '''
            cursor.execute(query_user_public_key_sql, (username,))
            result = cursor.fetchone()
            cursor.close()

            if result:
                user_public_key = result[0]
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        return user_public_key
    
# 检查某用户是否存在:1表示存在
def check_user_exist(id):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm') 
    db_conn.connect()

    user = User(db_conn.conn, phone_num=id)
    return user.user_exists()

# 检查账号密码是否对应
def check_login_with_pw(id, pw):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')           
    db_conn.connect()                
    user = User(db_conn.conn, username=id, phone_num=id, password=pw, public_key="public_key")

    return user.user_login_exists()

# 将新用户添加到数据库中
def add_user(id, pw, public_key):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')      
    db_conn.connect()      
    
    user = User(db_conn.conn, username=id, phone_num=id, password=pw, public_key=str(public_key))
    user.register_user()
    user.create_user_files_table()

# 查询用户文件列表
def get_file(id):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')      
    db_conn.connect()      
    
    user = User(db_conn.conn, username=id, phone_num=id)
    data = user.get_user_file_names()
    return data

def download_from_db(username, filename):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')      
    db_conn.connect()      
    
    user = User(db_conn.conn, username=username, phone_num=username)
    retrieved_file_content = user.get_user_file(filename)

    path_ = f'C:/Users/ducz/Desktop/sql/netdisk_space/zf/{filename}'

    if retrieved_file_content:     
        with open(f'C:/Users/ducz/Desktop/sql/netdisk_space/zf/{filename}', 'wb') as file:         
            file.write(base64.b64decode(retrieved_file_content))
            
    return path_


def delete_file(filename,username):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')      
    db_conn.connect()      
    
    user = User(db_conn.conn, username=username, phone_num=username)
    res = user.delete_user_file(filename)
    return res



def check_group(id):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')           
    db_conn.connect()      

    group = Group(conn=db_conn.conn)
    if group.table_exists(f'group_number_{id}'):
        return 1
    else:
        return 0    
def store_sharekey(group_id,id,key):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')                
    db_conn.connect()            
    
    group = Group(conn=db_conn.conn, group_id=group_id)
    group.create_group_number_table()
    group.create_group_files_table()

    group.add_member(username=id, phone_num=id, public_key=key)

def search_pbkey(id):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')                
    db_conn.connect()     
    user = User(conn=db_conn.conn, phone_num=id)

    user_info = user.get_user_info_by_phone_num(id)
    return user_info['public_key']

def search_group(id):

    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')                     
    db_conn.connect()     
    user = Group(conn=db_conn.conn)
    ids = user.get_user_groups(id)
    return ids

def list_group_file(id):

    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')                     
    db_conn.connect()     
    id = id.split('_')[1]
    group = Group(conn=db_conn.conn, group_id=id)
    file_list = group.get_group_shared_file_names()
    return file_list

def delete_group_file(id,filename):

    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')                     
    db_conn.connect()     
    id = id.split('_')[1]
    group = Group(conn=db_conn.conn, group_id=id)
    res = group.delete_group_shared_file(id,filename)
    return res

def  search_sharekey(id, username):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')                     
    db_conn.connect()     
    id = id.split('_')[1]
    group = Group(conn=db_conn.conn, group_id=id)

    return group.get_user_public_key_in_group(id, username)

def group_download_from_db(id, filename):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')                     
    db_conn.connect()     
    id = id.split('_')[1]
    group = Group(conn=db_conn.conn, group_id=id)

    retrieved_file_content = group.get_group_file(filename)
    file_path = f'C:/Users/ducz/Desktop/sql/netdisk_space/zf/{filename}'
    if retrieved_file_content:     
        with open(f'C:/Users/ducz/Desktop/sql/netdisk_space/zf/{filename}', 'wb') as file:         
            file.write(base64.b64decode(retrieved_file_content))
    return file_path

def group_upload_to_db(id, dp):
    db_conn = DatabaseConnector('127.0.0.1', 'root', 'root', 'xm')                     
    db_conn.connect()     
    id = id.split('_')[1]
    group = Group(conn=db_conn.conn, group_id=id)

    group.store_group_file(dp)
    print("文件上传数据库成功")



if __name__ == '__main__':
    # print(check_login_with_pw("18810503803", "123"))
    # print(get_file("12345"))
    # download_from_db("12345", "1.png")
    # # ['1.png', '2.png']
    # print(check_group(1))
    # store_sharekey(5,"12345","123")
    # print(search_pbkey("12345"))
    # print(search_group("9876543210"))
    # print(list_group_file("group_test1"))
    # print(search_sharekey("group_test1","12345"))
    # print(group_download_from_db("group_test1","1.png"))
    # group_upload_to_db("group_test1","C:/Users/ducz/Desktop/sql/netdisk_space/zf/inf.png")
    pass