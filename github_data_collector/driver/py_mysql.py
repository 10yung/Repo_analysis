import sys
import os
import mysql.connector

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from config._config import Config


# This Class follow singleton design pattern which allow only one instance be created in entire project
class PyMysqlConnector():
    _instance = None

    # __new__ should return a new, blank instance of a class. __init__ is then called to initialise that instance
    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            db_config = Config().get_mysql()
            try:
                print('connecting mySQL database...')
                connection = PyMysqlConnector._instance.connection = mysql.connector.connect(
                    host=db_config['host'],
                    user=db_config['user'],
                    passwd=db_config['password'],
                    database=db_config['database']
                )
                cursor = PyMysqlConnector._instance.cursor = connection.cursor()
                cursor.execute('SELECT VERSION()')
                db_version = cursor.fetchone()

            except Exception as error:
                print('Error: connection not established {}'.format(error))
                PyMysqlConnector._instance = None

            else:
                print('connection established\n{}'.format(db_version[0]))

        return cls._instance

    def __init__(self):
        """
            initialize with the return type node list or dictionary.
            @param: $mode optional or String 'dict'
            ( Virtually private constructor )
        """
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor

    def __del__(self):
        # TODO: Weak reference exception
        # self.cursor.close()
        self.connection.close()
        print('mysql connect close')

    def exec(self, query, value=None):
        # noinspection PyBroadException (supress to board exception)
        if value is None:
            try:
                self.cursor.execute(query)
                result = self.cursor.fetchall()
            except Exception as e:
                result = e
        else:
            try:
                self.cursor.execute(query, [value])
                self.connection.commit()
                result = 'Transaction completed!'
            except Exception as e:
                result = e

        return result
