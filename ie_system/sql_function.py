import pymysql

myhost = "10.122.247.180"

# 将新用户添加到注册表中
def add_user_to_db(username,password):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    try:
        with conn.cursor() as cursor:
            value = f"'{username}','{password}'"
            sql = f"insert into user_inf values ({value})"
            cursor.execute(sql)
            conn.commit()
            print("新用户添加成功！")
    except Exception as e:
        conn.rollback()
        print("数据库操作异常：\n", e)
    finally:
        conn.close()
    
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    try:
        with conn.cursor() as cursor:
            sql = f"create table {username} (name varchar(255))"
            cursor.execute(sql)
            conn.commit()
            print("为新用户创建好友列表成功！")
    except Exception as e:
        conn.rollback()
        print("数据库操作异常：\n", e)
    finally:
        conn.close()

# 查找表注册表中是否有该用户名
def select_username(username):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    ret = 0
    try:
        with conn.cursor() as cursor:
            sql = f"select * from user_inf where username = '{username}'"
            cursor.execute(sql)
            datas = cursor.fetchall()
            if(datas):
                ret = 1
    except Exception as e:
        print("数据库操作异常：\n", e)
    finally:
        conn.close()
    return ret

# 检查用户名和密码是否正确
def select_login(username,password):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    ret = 0
    try:
        with conn.cursor() as cursor:
            sql = f"select * from user_inf where username = '{username}' and password = '{password}'"
            cursor.execute(sql)
            datas = cursor.fetchall()
            if(datas):
                ret = 1
    except Exception as e:
        print("数据库操作异常：\n", e)
    finally:
        conn.close()
    return ret

# 列出用户的所有好友
def select_friend_list(username): 
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    try:
        with conn.cursor() as cursor:
            sql = f"select * from {username}"
            cursor.execute(sql)
            datas = cursor.fetchall()
    except Exception as e:
        print("数据库操作异常：\n", e)
    finally:
        conn.close()
    return datas

# 列出用户的所有在线好友
def select_online_firend_list(username):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    try:
        with conn.cursor() as cursor:
            sql = f"select * from {username} where exists(select * from online_state \
                where {username}.name = online_state.username)"
            cursor.execute(sql)
            datas = cursor.fetchall()
    except Exception as e:
        print("数据库操作异常：\n", e)
    finally:
        conn.close()
    return datas

# 判断用户跟另一用户是否是好友   
def select_friends(username,addname):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    ret = 0
    try:
        with conn.cursor() as cursor:
            sql = f"select * from {username} where name = '{addname}'"
            cursor.execute(sql)
            datas = cursor.fetchall()
            if(datas):
                ret = 1
    except Exception as e:
        print("数据库操作异常：\n", e)
    finally:
        conn.close()
    return ret

# 添加好友
def add_friends_in_db(username,addname):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    try:
        with conn.cursor() as cursor:
            sql = f"insert into {username} values ('{addname}')"
            cursor.execute(sql)
            conn.commit()
            print("添加好友成功")
    except Exception as e:
        conn.rollback()
        print("数据库操作异常：\n", e)
    finally:
        conn.close()

# 删除好友    
def delete_friends_in_db(username,deletename):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    try:
        with conn.cursor() as cursor:
            sql = f"delete from {username} where name = '{deletename}'"
            cursor.execute(sql)
            conn.commit()
            print("删除好友成功")
    except Exception as e:
        conn.rollback()
        print("数据库操作异常：\n", e)
    finally:
        conn.close()

# 更新用户在线状态至在线
def update_state_online(username):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    ret = 0
    try:
        with conn.cursor() as cursor:
            value = f"'{username}',1"
            sql = f"insert into online_state values ({value});"
            cursor.execute(sql)
            conn.commit()
            ret = 1
    except Exception as e:
        conn.rollback()
        print("数据库操作异常：\n", e)
    finally:
        conn.close()
    return ret

# 更新用户在线状态至离线
def update_state_offline(username):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    ret = 0
    try:
        with conn.cursor() as cursor:
            sql = sql = f"delete from online_state where username = '{username}';"
            cursor.execute(sql)
            conn.commit()
            ret = 1
    except Exception as e:
        conn.rollback()
        print("数据库操作异常：\n", e)
    finally:
        conn.close()
    return ret

# 记录用户的ip地址
def rec_login_inf(username,ip):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    try:
        with conn.cursor() as cursor:
            value = f"'{username}','{ip}'"
            sql = f"insert into connect_inf values ({value});"
            cursor.execute(sql)
            conn.commit()
    except Exception as e:
        conn.rollback()
        print("数据库操作异常：\n", e)
    finally:
        conn.close()

# 查找用户的ip地址  
def select_user_inf(chatname):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    try:
        with conn.cursor() as cursor:
            sql = f"select ip from connect_inf where username = '{chatname}'"
            cursor.execute(sql)
            datas = cursor.fetchall()
    except Exception as e:
        print("数据库操作异常：\n", e)
    finally:
        conn.close()
    return datas

# 删除用户的ip地址    
def delete_login_inf(username):
    conn = pymysql.connect(
        host=myhost,
        port=3306,
        database="ie_system",
        charset="utf8",
        user="root",
        passwd="12345678"
    )
    try:
        with conn.cursor() as cursor:
            sql = sql = f"delete from connect_inf where username = '{username}'"
            cursor.execute(sql)
            conn.commit()
    except Exception as e:
        conn.rollback()
        print("数据库操作异常：\n", e)
    finally:
        conn.close()