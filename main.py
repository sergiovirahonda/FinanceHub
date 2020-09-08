#  Activate the environment
# Windows:
# .\app-env\Scripts\activate
# MacOS/Linux:
#source app-env/bin/activate

## ----------------------------------------------- Imports ----------------------------------------------- ##
import pyodbc 
from flask import Flask, render_template, flash, request,redirect,url_for,send_file,send_from_directory,abort
import pandas as pd
import numpy as np
from datetime import datetime
import appHandling, usersHandling, logsHandling,inventoryHandling
import re
import os

## ----------------------------------------------- Starting app ------------------------------------------ ##

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
session = appHandling.Session(0,0)
user = appHandling.User([])
temp = ''

## ----------------------------------------------- DB innitializing -------------------------------------- ##

server = 'serge-machine'
database = 'ApplicationDB' 
username = 'SA' 
password = 'SudoRights!' 
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = connection.cursor()

## --------------------------------------------- Web Functions ------------------------------------------- ##

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')

@app.route('/', methods=['POST','GET'])
def index():
    if session.get_state() == 1:
        #logsHandling.register_login(cursor,connection,str(user_login.iloc[0]['username']))
        return render_template('index.html',name=str(user_login.iloc[0]['name']),last_name=str(user_login.iloc[0]['last_name']),avatar_path=user_login.iloc[0]['avatarPath'])
    else:
        return redirect('/login')

@app.route('/login', methods=['POST','GET'])
def login():
    global user_login 
    global session
    global user
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = str(request.form['password'])
        user_login = pd.read_sql_query("SELECT * from Users where username like '"+str(username)+"';", connection)
        if len(user_login)==0:
            error = 'Credenciales invalidas.'
            return render_template('login.html', error=error)
        else:
            if str(user_login.iloc[0]['password']) != password:
                error = 'Credenciales invalidas.'
            else:
                if str(user_login.iloc[0]['passwordReset']) =='1':
                    session = appHandling.Session(1,str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    user = appHandling.User(user_login)
                    return redirect('/password_reset')
                else:
                    session = appHandling.Session(1,str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    user = appHandling.User(user_login)
                    cursor.execute("update Users set lastLogin='"+session.get_start_time()+"' where username='"+user.get_username()+"'")
                    connection.commit()
                    return redirect('/')
            return render_template('login.html', error=error)
    else:
        return render_template('login.html', error=error)

@app.route('/password_reset',methods=['GET','POST'])
def password_reset():
    if session.get_state() == 1:
        if request.method == 'POST':
            password1 = request.form['password1']
            password2 = request.form['password2']
            if password1 == password2:
                result = usersHandling.set_password(cursor,connection,user.get_username(),password1)
                if result == 0:
                    return redirect('/')
                if result == 1:
                    return render_template('password_reset.html',message='Ups! La contrasena que ingresaste coincide con la anterior.')
                if result == 2:
                    return render_template('password_reset.html',message='Ups! La contrasena no cumple con los requisitos. Intenta con otra.')
                if result == 3:
                    return render_template('password_reset.html',message='Ups! Algo salio mal intentando cambiar tu contrasena. Intenta de nuevo.')
            else:
                return render_template('password_reset.html',message='Las contrasenas no coinciden. Intentalo de nuevo.')
        else:
            return render_template('password_reset.html',message='')
    else:
        return redirect('/exit')

@app.route('/inventory',methods=['GET','POST'])
def inventory():
    if session.get_state() == 1:
        kardex = inventoryHandling.get_kardex(connection)
        print(kardex)
        return render_template('inventory.html',data=kardex,titles=kardex.columns.values,name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/categories',methods=['GET','POST'])
def categories():
    if session.get_state() == 1:
        categories = inventoryHandling.get_categories(connection)
        print(categories)
        return render_template('categories.html',data=categories,titles=categories.columns.values,name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/add_category', methods=['POST','GET'])
def add_category():
    if session.get_state() == 1:
        if request.method=='POST':
            category = [request.form['id'],request.form['name'],request.form['description']]
            print(category)
            message,color = inventoryHandling.create_category(category,user,cursor,connection)
            return render_template('add_category.html',name=user.get_name(),last_name=user.get_last_name(),message=message,color=color,avatar_path=user.get_avatar_path())
        else:
            return render_template('add_category.html',name=user.get_name(),last_name=user.get_last_name(),message='',color='',avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/modify_category',methods=['POST','GET'])
def modify_category():
    global temp
    if session.get_state() == 1:
        if request.method=='GET':
            temp = request.args.get('id')
            return render_template('modify_category.html',category_id=temp,message='',color='',name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
        if request.method=='POST':
            category = [temp,request.form['name'],request.form['description']]
            message,color = inventoryHandling.modify_category(user.get_username(),category,cursor,connection)
            return render_template('modify_category.html',category_id=temp,message=message,color=color,name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/delete_category/<category_id>/<confirmation>',methods=['GET','POST'])
def delete_category(category_id,confirmation):
    if session.get_state() == 1:
        if confirmation == 'ok':
            if inventoryHandling.delete_category(user.get_username(),category_id,connection,cursor) == True:
                return redirect('/cat_deletion_ok')
            else:
                return redirect('/cat_deletion_fail')
        else:
            return abort(404)
    else:
        return redirect('/exit')

@app.route('/cat_confirmation',methods=['GET','POST'])
def cat_confirmation():
    if session.get_state() == 1:
        if request.method == 'GET':
            category_id = request.args.get('id')
            return render_template('cat_confirm.html',category_id=category_id,name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
        else:
            return redirect('/exit')
    else:
        return redirect('/exit')

@app.route('/cat_deletion_ok',methods=['GET','POST'])
def cat_deletion_ok():
    if session.get_state() == 1:
        return render_template('deletion_result.html',message='Se ha borrado la categoria exitosamente.',top='Excelente!',icon='<i class="fas fa-clipboard-check text-dark mb-4"></i>',return_to='categories',name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/cat_deletion_fail',methods=['GET','POST'])
def cat_deletion_fail():
    if session.get_state() == 1:
        return render_template('deletion_result.html',message='Parece que algo no salio bien. Intentalo de nuevo.',top='Oh no!',icon='<i class="fas fa-frown text-dark mb-4"></i>',return_to='categories',name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/articles',methods=['GET','POST'])
def articles():
    if session.get_state() == 1:
        articles = inventoryHandling.get_articles(connection)
        print(articles)
        return render_template('articles.html',data=articles,titles=articles.columns.values,name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/add_article', methods=['POST','GET'])
def add_article():
    if session.get_state() == 1:
        category_options = inventoryHandling.get_all_categories(connection)
        print(category_options)
        if request.method=='POST':
            article = [request.form['id'],request.form['name'],request.form['description'],request.form['category'],request.form['unit'],request.form['defaultPrice']]
            category = category_options[category_options['name']==article[3]]
            if len(category)>0:
                article[3] = category['categoryID'].values[0]
            else:
                return render_template('add_article.html',data=category_options['name'],name=user.get_name(),last_name=user.get_last_name(),message='Ups! Hubo un problema con esa categoria.',color='#E87012',avatar_path=user.get_avatar_path())
            print(article)
            message,color = inventoryHandling.create_article(article,user,cursor,connection)
            return render_template('add_article.html',data=category_options['name'],name=user.get_name(),last_name=user.get_last_name(),message=message,color=color,avatar_path=user.get_avatar_path())
        else:
            return render_template('add_article.html',data=category_options['name'],name=user.get_name(),last_name=user.get_last_name(),message='',color='',avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/modify_article',methods=['POST','GET'])
def modify_article():
    global temp
    if session.get_state() == 1:
        category_options = inventoryHandling.get_all_categories(connection)
        if request.method=='GET':
            temp = request.args.get('id')
            return render_template('modify_article.html',data=category_options['name'],article_id=temp,message='',color='',name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
        if request.method=='POST':
            article = [temp,request.form['name'],request.form['description'],request.form['category'],request.form['unit'],request.form['defaultPrice']]
            if article[3] != '-':
                category = category_options[category_options['name']==article[3]]
                if len(category)>0:
                    article[3] = category['categoryID'].values[0]
                else:
                    return render_template('modify_article.html',data=category_options['name'],article_id=temp,name=user.get_name(),last_name=user.get_last_name(),message='Ups! Hubo un problema con esa categoria.',color='#E87012',avatar_path=user.get_avatar_path())
            else:
                article[3] = ''
            message,color = inventoryHandling.modify_article(user.get_username(),article,cursor,connection)
            return render_template('modify_article.html',data=category_options['name'],article_id=temp,message=message,color=color,name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route("/exit")
def exit():
    global temp
    temp = ''
    session.drop()
    user.drop()
    user_login = np.nan
    return redirect("/login")

@app.route("/profile", methods=['POST','GET'])
def profile(): 
    global user
    if session.get_state() == 1:
        if request.method=='POST':
            profile = [user.get_username(),request.form['email'],request.form['name'],request.form['lastname'],request.form['password']]
            message,color = usersHandling.modify_profile(profile,user,cursor,connection)
            return render_template('profile.html',username=user.get_username(),name=user.get_name(),last_name=user.get_last_name(),role=user.get_role(),email=user.get_email(),passwordChangeDate=user.get_password_change_date(),change=message,color=color,avatar_path=user.get_avatar_path())
        else:
            return render_template('profile.html', username=user.get_username(),name=user.get_name(),last_name=user.get_last_name(),role=user.get_role(),email=user.get_email(),passwordChangeDate=user.get_password_change_date(),change='',color='',avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/users', methods=['POST','GET'])
def users():
    if session.get_state() == 1: 
        if user.get_role()=='admin':
            users = usersHandling.get_users(connection)
            return render_template('users.html',data=users,titles=users.columns.values,name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
        else:
            return redirect('/exit')
    else:
        return redirect('/exit')

@app.route('/add_user', methods=['POST','GET'])
def add_user():
    if session.get_state() == 1:
        if request.method=='POST':
            profile = [request.form['username'],request.form['email'],request.form['name'],request.form['lastname'],request.form['role'],request.form['password']]
            print(profile)
            message,color = usersHandling.create_user(profile,user,cursor,connection)
            return render_template('add_user.html',name=user.get_name(),last_name=user.get_last_name(),message=message,color=color,avatar_path=user.get_avatar_path())
        else:
            return render_template('add_user.html',name=user.get_name(),last_name=user.get_last_name(),message='',color='',avatar_path=user.get_avatar_path())
    else:
        return redirect('/exit')

@app.route('/modify_user',methods=['GET','POST'])
def modify_user():
    global temp
    if session.get_state() == 1:
        if user.get_role()=='admin':
            if request.method=='GET':
                temp = request.args.get('username')
                return render_template('modify_user.html',username=temp,message='',color='',name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
            if request.method=='POST':
                profile = [temp,request.form['email'],request.form['name'],request.form['lastname'],request.form['role'],request.form['password']]
                print(profile)
                message,color = usersHandling.modify_user(user.get_username(),profile,cursor,connection)
                return render_template('modify_user.html',username=temp,message=message,color=color,name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
        else:
            return redirect('/exit')
    else:
        return redirect('/exit')

@app.route('/delete_user/<username>/<confirmation>',methods=['GET','POST'])
def delete_user(username,confirmation):
    if session.get_state() == 1:
        if user.get_role() == 'admin':
            if confirmation == 'ok':
                if usersHandling.delete_user(user.get_username(),username,connection,cursor) == True:
                    return redirect('/deletion_ok')
                else:
                    return redirect('/deletion_fail')
            else:
                return abort(404)
        else:
            return redirect('/exit')
    else:
        return redirect('/exit')

@app.route('/confirmation',methods=['GET','POST'])
def confirmation():
    if session.get_state() == 1:
        if user.get_role() == 'admin':
            if request.method == 'GET':
                username = request.args.get('username')
                return render_template('confirm.html',username=username,name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
                #Add here the rest of the options
            else:
                return redirect('/exit')
        else:
            return redirect('/exit')
    else:
        return redirect('/exit')

@app.route('/deletion_ok',methods=['GET','POST'])
def deletion_ok():
    if session.get_state() == 1:
        if user.get_role() == 'admin':
            return render_template('deletion_result.html',message='El usuario ha sido dado de baja con exito.',top='Excelente!',icon='<i class="fas fa-clipboard-check text-dark mb-4"></i>',return_to='users',name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
        else:
            return redirect('/exit')
    else:
        return redirect('/exit')

@app.route('/deletion_fail',methods=['GET','POST'])
def deletion_fail():
    if session.get_state() == 1:
        if user.get_role() == 'admin':
            return render_template('deletion_result.html',message='Parece que algo no salio bien. Intentalo de nuevo.',top='Oh no!',icon='<i class="fas fa-frown text-dark mb-4"></i>',return_to='users',name=user.get_name(),last_name=user.get_last_name(),avatar_path=user.get_avatar_path())
        else:
            return redirect('/exit')
    else:
        return redirect('/exit')

if __name__ == '__main__':
    app.run(debug=True)