from datetime import datetime
import re
import pandas as pd


## ------------------------------------------------------------------------------------------------- ##
## -------------------------------------- Functions' definition ------------------------------------ ##

def modify_user(cursor,connection,username,action,description,performed_by):
    try:
        mod_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute("insert into UsersLog(username,action,actionDescription,performedBy,timeStamp) values('"+str(username)+"','"+str(action)+"','"+str(description)+"','"+str(performed_by)+"','"+mod_time+"');")
        connection.commit()
        return 'ok'
    except Exception as e:
        print(e)
        return 'failed'

def register_login(cursor,connection,username):
    try:
        time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute("insert into LoginLog(username,timeStamp) values('"+str(username)+"','"+time+"');")
        connection.commit()
        return
    except Exception as e:
        print(e)
        return e




