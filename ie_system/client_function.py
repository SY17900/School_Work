import requests
import json
import messaging_client1 as client1

url = "http://10.122.247.180:11451"

def regis(username,password):
    data = {
        "port": 1,
        "type": "Registration",
        "username": username,
        "password": password
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    return response

def login(username,password):
    data = {
        "port": 1,
        "type": "Login",
        "username": username,
        "password": password
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    return response

def set_online(username):
    data = {
        "port": 4,
        "type": "online",
        "username": username
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    return response

def add_friends(username,addname):
    data = {
        "port": 2,
        "type": "add",
        "username": username,
        "addname": addname
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    return response

def delete_friends(username,deletename):
    data = {
        "port": 2,
        "type": "delete",
        "username": username,
        "deletename": deletename
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    return response

def show_friend_list(username):
    data = {
        "port": 2,
        "type": "list_friends",
        "username": username
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    return response

def show_online_friend_list(username):
    data = {
        "port": 2,
        "type": "list_online_friends",
        "username": username
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    return response

def send_message(username,chatname,message):
    get_ip = get_ip_inf(chatname)
    get_ip = json.loads(get_ip.text)
    ip = get_ip["message"]
    if(ip == "no result"):
        return 0
    else:
        client1.chat(username,ip,message)
    return 1
        
def get_ip_inf(chatname):
    data = {
        "port": 3,
        "chatname": chatname
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    return response

def set_offline(username):
    data = {
        "port": 4,
        "type": "offline",
        "username": username
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json_data)
    return response