import sys
import os
# sys.path.append(os.path.abspath('../../driver'))
# sys.path.append(os.path.abspath('../../config'))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from driver.py_mysql import PyMysqlConnector
from config._config import Config

# Select data from default table (specific table) with column name

class SelectCols:
    tableName = ''

    def __init__(self, tableName = Config().get_mysql()['default_table']):
        self.tableName = tableName
        print()

    def col_name(self, *colName):
        query = f"SELECT {', '.join(colName)} FROM {self.tableName}"
        result = PyMysqlConnector().exec(query)

        return result