import http.server
import sql_function as sql

def userinf_system(request):
    chatname = request['chatname']
    ans = sql.select_user_inf(chatname)
    if(ans == ()):
        response = {'success': True,'message': "no result"}
    else:
        ip = ans[0][0]
        response = {'success': True,'message': ip}
    
    return response