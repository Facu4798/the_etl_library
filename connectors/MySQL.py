class MySQLConnector:
    def __init__(self,params):
        for k,v in params.items():
            setattr(self, k, v)

    def add_credential(self, key, value):
        setattr(self, key, value)

    def test_connection(self):
        import mysql.connector
        connection = None
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
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

    def get_data(self,query):
        import mysql.connector
        import pandas as pd
        connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return pd.DataFrame(result, columns=[i[0] for i in cursor.description])
