import pytest
import pymysql
import os

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
        pymysql.connect(host='localhost', user='root', passwd='qwe13245', db='rpg', charset="utf8", port=3528)
        flag = True
    except:
        flag = False
    assert flag == True


