from datetime import datetime
import re
import pandas as pd
## -------------------------------------- Classes' definition -------------------------------------- ##

class User:
    def __init__(self,user_data):
        #Constructor
        if len(user_data)==0:
            self._username = None
            self._name = None
            self._last_name = None
            self._role = None
            self._password_change_date = None
            self._last_login = None
            self._email = None
            self._avatar_path = None
            self._password_reset = None
        else:
            self._username = str(user_data.iloc[0]['username'])
            self._name = str(user_data.iloc[0]['name'])
            self._last_name = str(user_data.iloc[0]['last_name'])
            self._role = str(user_data.iloc[0]['role'])
            self._password_change_date = str(user_data.iloc[0]['passwordChangeDate'])
            self._last_login = str(user_data.iloc[0]['lastLogin'])   
            self._email = str(user_data.iloc[0]['email']) 
            self._avatar_path = str(user_data.iloc[0]['avatarPath'])
            self._password_reset = str(user_data.iloc[0]['passwordReset'])

    #Getters     
    def get_username(self):
        return self._username  
    def get_name(self):
        return self._name  
    def get_last_name(self):
        return self._last_name
    def get_role(self):
        return self._role 
    def get_password_change_date(self):
        return self._password_change_date  
    def get_last_login(self):
        return self._last_login
    def get_email(self):
        return self._email
    def get_avatar_path(self):
        return self._avatar_path
    def get_password_reset(self):
        return self._password_reset
    #Setters
    def set_username(self,username):
        self._username = username  
    def set_name(self,name):
        self._name = name
    def set_last_name(self,last_name):
        self._last_name = last_name
    def set_role(self,role):
        self._role = role
    def set_password_change_date(self,change_date):
        self._password_change_date = change_date
    def set_last_login(self,last_login):
        self._last_login = last_login
    def set_email(self,email):
        self._email = email
    def set_avatar_path(self,avatar_path):
        self._avatar_path = avatar_path
    def set_password_reset(self,password_reset):
        self._password_reset = password_reset
    #Dropper
    def drop(self):
        self._username = None
        self._name = None
        self._last_name = None
        self._role = None
        self._password_change_date = None
        self._last_login = None
        self._email = None
        self._avatar_path = None
        self._password_reset = None


class Session:
    #Constructor
    def __init__(self,session_state,session_start):
        self._session_state = session_state
        self._session_start = session_start
    #Getter
    def get_state(self):
        return self._session_state
    def get_start_time(self):
        return self._session_start
    #dropper
    def drop(self):
        self._session_state = 0
        self._session_start = 0
## ------------------------------------------------------------------------------------------------- ##
## -------------------------------------- Functions' definition ------------------------------------ ##


    