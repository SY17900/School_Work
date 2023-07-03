import sql_function as sql

def online_state_system(request):
    username = request['username']
    if(request['type'] == 'online'):
        if(sql.update_state_online(username) == 1):
            response = {'success': True, 'message': ''}
    elif(request['type'] == 'offline'):
        if(sql.update_state_offline(username) == 1):
            sql.delete_login_inf(username)
            response = {'success': True, 'message': ''}
    
    return response