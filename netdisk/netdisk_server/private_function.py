import file_function as ff
import sql_function as sql
import json

# 上传文件
def private_upload(data, self):
    ff.upload_file(data, self)

# 下载文件    
def private_download(data, self):
    ff.download_file(data, self)

# 通过用户id查询其在私人空间中储存的文件(名称)
def private_list(data, self):
    username = data["username"]
    list = sql.get_file(username)
    self.request.send(json.dumps(list).encode())

def private_management(data, self):
    if(data["type"] == "upload"):
        private_upload(data, self)
    elif(data["type"] == "download"):
        private_download(data, self)
    elif(data["type"] == "list"):
        private_list(data, self)
