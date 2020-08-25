from datetime import datetime
import re
import pandas as pd
import logsHandling



## ------------------------------------------------------------------------------------------------- ##
## -------------------------------------- Functions' definition ------------------------------------ ##

def modify_profile(profile,user,cursor,connection):
    username = profile[0].strip("'").strip('"')
    email = profile[1].strip("'").strip('"')
    name = profile[2].strip("'").strip('"')
    last_name = profile[3].strip("'").strip('"')
    password = profile[4].strip("'").strip('"')
    if email != '':
        if len(pd.read_sql_query("SELECT * from Users where email like '"+str(email)+"';", connection))==0:
            try:
                cursor.execute("update Users set email='"+str(email)+"' where username='"+str(username)+"'")
                logsHandling.modify_user(cursor,connection,str(username),'Modificacion','Modificar email a '+str(email),str(username))
                connection.commit()
                user.set_email(str(email))
            except Exception as e:
                return 'Ups! Algo salio mal intentando modificar el email. Intentalo de nuevo.','#E87012'
        else:
            return 'Ups! El email ingresado ya esta asociado a otro usuario.','#E87012'
    if name != '':
        if len(name)<=20:
            regex = re.compile('[123456789@_!#$%^&*()<".,-_+>?/\|}{~:]')
            if(regex.search(name) == None):
                try:
                    cursor.execute("update Users set name='"+str(name)+"' where username='"+str(username)+"'")
                    logsHandling.modify_user(cursor,connection,str(username),'Modificacion','Modificar nombre a '+str(name),str(username))
                    connection.commit()
                    user.set_name(str(name))
                except Exception as e:
                    return 'Ups! Algo salio mal intentando modificar el nombre. Intentalo de nuevo.','#E87012'
            else:
                return 'Ups! El nombre es invalido.','#E87012'
        else:
            return 'Ups! El nombre es invalido.','#E87012'
    if last_name != '':
        if len(last_name)<=20:
            regex = re.compile('[123456789@_!#$%^&*()<".,-_+>?/\|}{~:]')
            if(regex.search(last_name) == None):
                try:
                    cursor.execute("update Users set last_name='"+str(last_name)+"' where username='"+str(username)+"'")
                    logsHandling.modify_user(cursor,connection,str(username),'Modificacion','Modificar apellido a '+str(last_name),str(username))
                    connection.commit()
                    user.set_last_name(str(last_name))
                except Exception as e:
                    return 'Ups! Algo salio mal intentando modificar el apellido. Intentalo de nuevo.','#E87012'
            else:
                return 'Ups! El apellido invalido.','#E87012'
        else:
            return 'Ups! El apellido invalido.','#E87012'
    if password != '':
        regex = re.compile('[123456789@_!#$%^&*()<".,-_+>?/\|}{~:]')
        if ((len(password)>=8) and (regex.search(password)!=None) and (len(password)<=50)):
            try:
                change_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                cursor.execute("update Users set password='"+str(password)+"' where username='"+str(username)+"'")
                cursor.execute("update Users set passwordChangeDate='"+change_date+"' where username='"+str(username)+"'")
                logsHandling.modify_user(cursor,connection,str(username),'Modificacion','Modificar contrasena',str(username))
                connection.commit()
            except Exception as e:
                return 'Ups! Algo salio mal intentando modificar la contrasena. Intentalo de nuevo.','#E87012'
        else:
            return 'Ups! El tipo de contrasena es invalida.','#E87012'
    return 'Excelente! Los cambios se han aplicado con exito.','#5CA343'

def create_user(profile,user,cursor,connection):
    username = profile[0].strip("'").strip('"')
    email = profile[1].strip("'").strip('"')
    name = profile[2].strip("'").strip('"')
    last_name = profile[3].strip("'").strip('"')
    role = profile[4].strip("'").strip('"')
    password = profile[5].strip("'").strip('"')
    if ((len(username)>=6) & (len(username)<=20)):
        regex = re.compile('[@_!#$%^&*()<",+>?/\|}{~:]')
        if(regex.search(username) == None):
            if len(pd.read_sql_query("SELECT username from Users where username like '"+str(username)+"';", connection))==0:
                pass
            else:
                return 'Ups! El nombre de usuario ya existe.','#E87012'
        else:
            return 'Ups! El nombre de usuario es invalido.','#E87012'
    else:
        return 'Ups! El nombre de usuario es invalido.','#E87012'
    if len(name)<=20:
        #regex = re.compile('[123456789@_!#$%^&*()<.,-_+>?/\|}{~:]')
        regex = re.compile('[^A-Za-z]')
        if(regex.search(name) == None):
            pass
        else:
            return 'Ups! El nombre del empleado es invalido.','#E87012'
    else:
        return 'Ups! El nombre del empleado es invalido.','#E87012'
    if len(pd.read_sql_query("SELECT * from Users where email like '"+str(email)+"';", connection))==0:
        pass
    else:
        return 'Ups! El email ingresado ya esta asociado a otro usuario.','#E87012'
    if len(last_name)<=20:
        regex = re.compile('[^A-Za-z]')
        if(regex.search(last_name) == None):
            pass
        else:
            return 'Ups! El apellido del empleado es invalido.','#E87012'
    else:
        return 'Ups! El apellido del empleado es invalido.','#E87012'
    if (len(password)>=8 & len(password)<=50):
        pass
    else:
        return 'Ups! El tipo de contrasena es invalida.','#E87012'
    try:
        creation_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute("insert into Users(username,email,name,last_name,role,password,creationDate,avatarPath) values('"+username+"','"+email+"','"+name+"','"+last_name+"','"+role+"','"+password+"','"+creation_date+"','"+'static/img/avatars/avatar.jpeg'+"');")
        logsHandling.modify_user(cursor,connection,str(username),'Alta','Registro: '+str(email)+'|'+str(name)+'|'+str(last_name)+'|'+str(role),str(user.get_username()))
        connection.commit()
        return 'Excelente! El usuario se ha creado con exito.','#5CA343'
    except Exception as e:
        return 'Ups, algo salio mal! Intentalo de nuevo.','#E87012'


def modify_user(user,profile,cursor,connection):
    username = profile[0].strip("'").strip('"')
    email = profile[1].strip("'").strip('"')
    name = profile[2].strip("'").strip('"')
    last_name = profile[3].strip("'").strip('"')
    role = profile[4].strip("'").strip('"')
    password = profile[5].strip("'").strip('"')
    if email != '':
        if len(pd.read_sql_query("SELECT * from Users where email like '"+str(email)+"';", connection))==0:
            try:
                cursor.execute("update Users set email='"+str(email)+"' where username='"+str(username)+"'")
                logsHandling.modify_user(cursor,connection,str(username),'Modificacion','Email: '+str(email),str(user))
                connection.commit()
            except Exception as e:
                return 'Ups! Algo salio mal intentando modificar el email. Intentalo de nuevo.','#E87012'
        else:
            return 'Ups! El email ingresado ya esta asociado a otro usuario.','#E87012'
    if name != '':
        if len(name)<=20:
            regex = re.compile('[^A-Za-z]')
            if(regex.search(name) == None):
                try:
                    cursor.execute("update Users set name='"+str(name)+"' where username='"+str(username)+"'")
                    logsHandling.modify_user(cursor,connection,str(username),'Modificacion','Nombre: '+str(name),str(user))
                    connection.commit()
                except Exception as e:
                    return 'Ups! Algo salio mal intentando modificar el nombre. Intentalo de nuevo.','#E87012'
            else:
                return 'Ups! El nombre del empleado es invalido.','#E87012'
        else:
            return 'Ups! El nombre del empleado es invalido.','#E87012'
    if last_name != '':
        if len(last_name)<=20:
            regex = re.compile('[^A-Za-z]')
            if(regex.search(last_name) == None):
                try:
                    cursor.execute("update Users set last_name='"+str(last_name)+"' where username='"+str(username)+"'")
                    logsHandling.modify_user(cursor,connection,str(username),'Modificacion','Apellido: '+str(last_name),str(user))
                    connection.commit()
                except Exception as e:
                    return 'Ups! Algo salio mal intentando modificar el apellido. Intentalo de nuevo.','#E87012'
            else:
                return 'Ups! El apellido del empleado es invalido.','#E87012'
        else:
            return 'Ups! El apellido del empleado es invalido.','#E87012'
    if password != '':
        regex = re.compile('[123456789@_!#$%^&*()<".,-_+>?/\|}{~:]')
        if ((len(password)>=8) and (regex.search(password)!=None) and (len(password)<=50)):
            try:
                change_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                cursor.execute("update Users set password='"+str(password)+"' where username='"+str(username)+"'")
                cursor.execute("update Users set passwordChangeDate='"+change_date+"' where username='"+str(username)+"'")
                cursor.execute("update Users set passwordReset=1 where username='"+str(username)+"'")
                logsHandling.modify_user(cursor,connection,str(username),'Modificacion','Contrasena',str(user))
                connection.commit()
            except Exception as e:
                return 'Ups! Algo salio mal intentando modificar la contrasena. Intentalo de nuevo.','#E87012'
        else:
            return 'Ups! El tipo de contrasena es invalida.','#E87012'
    if role != '':
        pass
    return 'Excelente! Los cambios se han aplicado con exito.','#5CA343'


def get_users(connection):
    users = pd.read_sql_query("SELECT username,name,last_name,role,lastLogin,passwordChangeDate from Users;", connection)
    users.fillna('No disponible',inplace=True)
    users.sort_values(by='username',inplace=True)
    users['username'] = '<a href="http://localhost:5000/modify_user?username='+users['username']+'">'+users['username']+'</a>'
    users.rename(columns={'username':'Nombre de usuario','name':'Nombre','last_name':'Apellido','role':'Rol','lastLogin':'Ultima sesion','passwordChangeDate':'Ultimo cambio de contrasena'},inplace=True)  
    return users

def delete_user(user,username,connection,cursor):
    try:
        cursor.execute("delete from Users where username='"+str(username)+"';")
        logsHandling.modify_user(cursor,connection,str(username),'Baja','-',str(user))
        connection.commit()
        return True
    except Exception as e:
        return False

def set_password(cursor,connection,username,password):
    try:
        change_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        current_password = pd.read_sql_query("select password from Users where username like '"+str(username)+"';", connection)
        current_password = current_password.iloc[0]['password']
        if password == current_password:
            return 1
        else:
            regex = re.compile('[123456789@_!#$%^&*()<".,-_+>?/\|}{~:]')
            if ((len(password)>=8) and (regex.search(password)!=None) and (len(password)<=50)):
                cursor.execute("update Users set password='"+str(password)+"' where username='"+str(username)+"';")
                cursor.execute("update Users set passwordChangeDate='"+change_date+"' where username='"+str(username)+"'")
                cursor.execute("update Users set passwordReset=0 where username='"+str(username)+"'")
                connection.commit()
                return 0
            else:
                return 2
    except Exception as e:
        return 3
