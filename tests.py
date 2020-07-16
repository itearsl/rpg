import pytest
import pymysql
import os
import configparser
import pymysql
path = "config.ini"
config = configparser.ConfigParser()
config.read(path) # Path
host_bd = config.get("Config", "host")
user_bd = config.get("Config", "user")
passwd_bd = config.get("Config", "passwd")
db_bd = config.get("Config", "db")
charset_bd = config.get("Config", "charset")
# ------------HOW TO USE------------
# Install pytest >> pip install pytest
# in terminal enter pytest tests.py


def test_check_settings():
    """ Check empty settings file """
    file_path = os.path.abspath(os.curdir) + '/settings.ini'
    assert os.path.exists(file_path) is True


def test_check_config():
    """ Check empty settings file """
    file_path = os.path.abspath(os.curdir) + '/config.ini'
    assert os.path.exists(file_path) is True


def test_check_bd():
    """ Check connect to basedata"""
    try:
        pymysql.connect(host=host_bd, user=user_bd, passwd=passwd_bd, db=db_bd, charset=charset_bd, port=3528)
        flag = True
    except:
        flag = False
    assert flag is True


