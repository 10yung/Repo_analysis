import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from driver.py_mysql import PyMysqlConnector
from config._config import Config


class CreateCols:
    table_name = ''

    def __init__(self, table_name=Config().get_mysql()['default_table']):
        self.table_name = table_name

    def create_cols(self, col_attribute):
        """
            @param col_attribute :

            {
                "colName" : "xxx",
                "type": "VARCHAR(255)"
            }
        """
        query = f"ALTER TABLE {self.table_name} ADD {col_attribute['colName']} {col_attribute['type']};"
        result = PyMysqlConnector().exec(query)

        return result
