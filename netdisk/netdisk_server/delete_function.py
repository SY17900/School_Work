import sql_function as sql
import json

def delete_management(request, self):
    if(request["type"] == "private"):
        filename = request["file_name"]
        username = request["username"]
        result = sql.delete_file(filename,username)
        if(result == 1):
            reply = {
                "success": True
            }
        else:
            reply = {
                "success": False
            }
        self.request.send(json.dumps(reply).encode())
    elif(request["type"] == "group"):
        group_id = request["groupname"]
        filename = request["file_name"]
        result = sql.delete_group_file(group_id,filename)
        if(result == 1):
            reply = {
                "success": True
            }
        else:
            reply = {
                "success": False
            }
        self.request.send(json.dumps(reply).encode())
    return 1
