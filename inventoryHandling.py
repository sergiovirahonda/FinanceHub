from datetime import datetime
import re
import pandas as pd
import logsHandling
import numpy as np

def get_kardex(connection):
    try:
        kardex = pd.read_sql_query("SELECT * from InventoryKardex;", connection)
        kardex.fillna('-',inplace=True)
        kardex.sort_values(by=['operationDate','classID'],inplace=True)
        kardex.rename(columns={'productID':'ID operacion','classID':'ID producto','name':'Nombre','description':'Descripcion','operationType':'Tipo operacion','documentNumber':'Numero documento','operationDate':'Fecha operacion','inputQuantity':'Cantidad compra','inputUnitValue':'Valor unitario compra','inputTotalValue':'Valor total compra','outputQuantity':'Cantidad venta','outputUnitValue':'Valor unitario venta','outputTotalValue':'Valor total venta','TotalQuantity':'Cantidad total existente','TotalUnitValue':'Costo promedio','TotalValue':'Costo total promedio'},inplace=True)
        #kardex = kardex.style.set_properties(**{'font-size': '10pt',})
        return kardex
    except:
        kardex = None
        print('There was an issue querying the Kardex')
        return kardex

def get_articles(connection):
    try:
        articles = pd.read_sql_query("SELECT * from Articles;", connection)
        articles.fillna('-',inplace=True)
        articles.sort_values(by=['creationDate','productID'],inplace=True)
        articles.rename(columns={'ID':'ID control','productID':'ID producto','name':'Nombre','description':'Descripcion','unit':'Unidades','category':'Categoria','defaultPrice':'Costo predeterminado','creationDate':'Fecha creacion'},inplace=True)
        return articles
    except:
        articles = None
        print('There was an issue querying the articles')
        return articles

def create_article(article,user,cursor,connection):
    article_id = article[0].strip("'").strip('"')
    article_name = article[1].strip("'").strip('"')
    article_description = article[2].strip("'").strip('"')
    article_unit = article[3].strip("'").strip('"')
    article_category = article[4].strip("'").strip('"')
    article_default_price = article[5].strip("'").strip('"')
    try:
        article_default_price = float(article_default_price)
    except:
        return 'Ups! El precio ingresado no es valido.','#E87012'
    if len(article_id)<=20:
        regex = re.compile('[^A-Za-z0-9]')
        if(regex.search(article_id) == None):
            if len(pd.read_sql_query("SELECT productID from Articles where productID like '"+str(article_id)+"';", connection))==0:
                pass
            else:
                return 'Ups! El ID ingresado ya existe.','#E87012'
        else:
            return 'Ups! El ID ingresado es invalido.','#E87012'
    else:
        return 'Ups! El ID ingresado es invalido.','#E87012'
    if len(article_name)<=20:
        regex = re.compile('[^A-Za-z0-9\s]')
        print(regex.search(article_name))
        if(regex.search(article_name) == None):
            if len(pd.read_sql_query("SELECT name from Articles where name like '"+str(article_name)+"';", connection))==0:
                pass
            else:
                return 'Ups! El nombre del articulo ingresado ya existe.','#E87012'
        else:
            return 'Ups! El nombre del articulo ingresado es invalido.','#E87012'
    else:
        return 'Ups! El nombre del articulo ingresado es invalido.','#E87012'
    if len(article_description)<=100:
        pass
    else:
        return 'Ups! La descripcion del articulo ingresada es invalida.','#E87012'
    if len(article_unit)<=20:
        regex = re.compile('[^A-Za-z0-9\s]')
        if(regex.search(article_unit) == None):
            pass
        else:
            return 'Ups! La unidad del articulo ingresada es invalida.','#E87012'
    else:
        return 'Ups! La unidad del articulo ingresada es invalida.','#E87012'
    if len(article_category)<=20:
        regex = re.compile('[^A-Za-z0-9\s]')
        if(regex.search(article_category) == None):
            if len(pd.read_sql_query("SELECT categoryID from Categories where categoryID like '"+str(article_category)+"';", connection))!=0:
                pass
            else:
                return 'Ups! Parece que esa categoria no existe en la tabla de categorias.'
        else:
            return 'Ups! La categoria del articulo ingresada es invalida.','#E87012'
    else:
        return 'Ups! La categoria del articulo ingresada es invalida.','#E87012'
    if isinstance(article_default_price, float):
        pass
    else:
        return 'Ups! Parece que el precio ingresado es invalido.'
    try:
        creation_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute("insert into Articles(productID,name,description,unit,category,defaultPrice,creationDate) values('"+article_id+"','"+article_name+"','"+article_description+"','"+article_unit+"','"+article_description+"','"+article_category+"','"+str(article_default_price)+"');")
        connection.commit()
        return 'Excelente! El articulo se ha creado con exito.','#5CA343'
    except Exception as e:
        return 'Ups, algo salio mal! Intentalo de nuevo.','#E87012'

def get_categories(connection):
    try:
        categories = pd.read_sql_query("SELECT * from Categories;", connection)
        categories.fillna('-',inplace=True)
        categories.sort_values(by=['creationDate','categoryID'],inplace=True)
        categories['categoryID'] = '<a href="http://localhost:5000/modify_category?id='+categories['categoryID']+'">'+categories['categoryID']+'</a>'
        categories.rename(columns={'id':'ID control','categoryID':'ID categoria','name':'Nombre','description':'Descripcion','creationDate':'Fecha creacion'},inplace=True)
        return categories
    except:
        categories = None
        return categories

def get_all_categories(connection):
    try:
        categories = pd.read_sql_query("SELECT categoryID,name from Categories;", connection)
        categories.sort_values(by=['categoryID'],inplace=True)
        return categories
    except:
        categories = None
        return categories

def create_category(category,user,cursor,connection):
    category_id = category[0].strip("'").strip('"')
    category_name = category[1].strip("'").strip('"')
    category_description = category[2].strip("'").strip('"')
    if len(category_id)<=20:
        regex = re.compile('[^A-Za-z0-9]')
        if(regex.search(category_id) == None):
            if len(pd.read_sql_query("SELECT categoryID from Categories where categoryID like '"+str(category_id)+"';", connection))==0:
                pass
            else:
                return 'Ups! El ID ingresado ya existe.','#E87012'
        else:
            return 'Ups! El ID ingresado es invalido.','#E87012'
    else:
        return 'Ups! El ID ingresado es invalido.','#E87012'
    if len(category_name)<=20:
        regex = re.compile('[^A-Za-z0-9\s]')
        print(regex.search(category_name))
        if(regex.search(category_name) == None):
            if len(pd.read_sql_query("SELECT name from Categories where name like '"+str(category_name)+"';", connection))==0:
                pass
            else:
                return 'Ups! El nombre de categoria ingresado ya existe.','#E87012'
        else:
            return 'Ups! El nombre de categoria ingresado es invalido.','#E87012'
    else:
        return 'Ups! El nombre de categoria ingresado es invalido.','#E87012'
    if len(category_description)<=100:
        pass
    else:
        return 'Ups! La descripcion de categoria ingresada es invalida.','#E87012'
    try:
        creation_date = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        cursor.execute("insert into Categories(categoryID,name,description,creationDate) values('"+category_id+"','"+category_name+"','"+category_description+"','"+creation_date+"');")
        #logsHandling.modify_user(cursor,connection,str(username),'Alta','Registro: '+str(email)+'|'+str(name)+'|'+str(last_name)+'|'+str(role),str(user.get_username()))
        connection.commit()
        return 'Excelente! La categoria se ha creado con exito.','#5CA343'
    except Exception as e:
        return 'Ups, algo salio mal! Intentalo de nuevo.','#E87012'

def modify_category(username,category,cursor,connection):
    category_id = category[0].strip("'").strip('"')
    name = category[1].strip("'").strip('"')
    description = category[2].strip("'").strip('"')
    if name != '':
        if len(name)<=20:
            regex = re.compile('[^A-Za-z0-9\s]')
            if(regex.search(name) == None):
                if len(pd.read_sql_query("SELECT * from Categories where name like '"+str(name)+"';", connection))==0:
                    try:
                        cursor.execute("update Categories set name='"+str(name)+"' where categoryID='"+str(category_id)+"'")
                        connection.commit()
                    except Exception as e:
                        return 'Ups! Algo salio mal intentando modificar el nombre. Intentalo de nuevo.','#E87012'
                else:
                    return 'Ups! El nombre ingresado ya esta asociado a otra categoria.','#E87012'
            else:
                return 'Ups! El nombre ingresado es invalido.','#E87012'
        else:
            return 'Ups! El nombre ingresado es invalido.','#E87012'
    if description != '':
        if len(description)<=100:
            try:
                cursor.execute("update Categories set description='"+str(description)+"' where categoryID='"+str(category_id)+"'")
                connection.commit()
            except Exception as e:
                return 'Ups! Algo salio mal intentando modificar la descripcion. Intentalo de nuevo.','#E87012'
        else:
            return 'Ups! La descripcion de la categoria es invalida.','#E87012'
    return 'Excelente! Los cambios se han aplicado con exito.','#5CA343'
    
def delete_category(username,category_id,connection,cursor):
    try:
        cursor.execute("delete from Categories where categoryID='"+str(category_id)+"';")
        connection.commit()
        return True
    except Exception as e:
        return False