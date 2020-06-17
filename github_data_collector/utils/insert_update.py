import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from config._config import Config
from driver.py_mysql import PyMysqlConnector


class InsertUpdate:
    tableName = ''
    colName = ''

    def __init__(self, colName, tableName = Config().get_mysql()['default_table']):
        self.tableName = tableName
        self.colName = colName

    def update_val(self, fullName, value):
        query = f"""UPDATE {self.tableName} SET {self.colName} = "%s" WHERE full_name = '{fullName}'"""
        result = PyMysqlConnector().exec(query, value)

        return result
