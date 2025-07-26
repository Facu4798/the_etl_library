class MySQLConnector:
    def __init__(self,params):
        for k,v in params.items():
            setattr(self, k, v)
    def add_credential(self, key, value):
        setattr(self, key, value)
    def test_connection(self):
        import mysql.connector
        connection = None
        required_params = ['host', 'user', 'password', 'database', 'port']
        for p in required_params:
            if not hasattr(self, p):
                print(f"Missing required parameter: {p}")
                return ""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if connection.is_connected():
                print("Connection successful")
                return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            if connection and connection.is_connected():
                connection.close()
    def connect(self):
        import mysql.connector
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )
        self.cursor = self.connection.cursor()
        return self
    def get_data(self,query):
        import mysql.connector
        import pandas as pd
        try:
            self.cursor.execute(query)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return pd.DataFrame()
        result = self.cursor.fetchall()
        return pd.DataFrame(result, columns=[i[0] for i in self.cursor.description])
    def check_existance(self, type,name):
        pass
