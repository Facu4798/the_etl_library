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
                
        except mysql.connector.Error as err:
            print(f"Error: {err}")
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
    
    def check_existance(self, obj_type,name):
        self.cursor.execute(f"SHOW {obj_type} LIKE '{name}'")
        return self.cursor.fetchone() is not None

    def insert_data(self,data,table_name,pks= None):
        # check table existance
        if self.check_existance('TABLES', table_name):
            pass
        else:
            print(f"Table {table_name} does not exist.")
            return None
        
        # insert data
        import pandas as pd
        import numpy as np
        if isinstance(data, pd.DataFrame):
            columns = ', '.join(data.columns)
            placeholders = ', '.join(['%s'] * len(data.columns))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            if pks is not None:
                update_set = ', '.join([f"{col} = VALUES({col})" for col in data.columns if col not in pks])
                query += f" ON DUPLICATE KEY UPDATE {update_set}"
            values = [tuple(row) for row in data.values]
            values = [tuple(None if isinstance(x, float) and np.isnan(x) else x for x in row) for row in data.values]
            self.cursor.executemany(query, values)
            self.connection.commit()

    def create_table(self, query = None,data=None,table_name=None, pks=None, exceptions = None):
        if query != None:
            q = query
        
        if data is not None and table_name is not None:
            if self.check_existance('TABLES', table_name):
                print(f"Table {table_name} already exists.")
                return None
            dtype_mapper = DTypeMapper()
            dtypes = dtype_mapper.map(data,exceptions=exceptions)
            q = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {', '.join(f'{col} {dtype}' for col, dtype in dtypes.items())}
            )
            """
            if pks!=None:
                q = q.rstrip().rsplit(')', 1)[0]
                q += f", PRIMARY KEY ({', '.join(pks)}))"
        self.cursor.execute(q)
        self.connection.commit()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Connection closed")
        else:
            print("No active connection to close")
        return self


class DTypeMapper:
    def __init__(self):
        self.map_dict = {}

    def map(self,data,exceptions):
        import pandas as pd        
        dtypes = data.dtypes
        for col, dtype in dtypes.items():
            if pd.api.types.is_integer_dtype(dtype):
                self.map_dict[col] = 'INT'
            elif pd.api.types.is_float_dtype(dtype):
                self.map_dict[col] = 'FLOAT'
            elif pd.api.types.is_string_dtype(dtype):
                self.map_dict[col] = 'VARCHAR(255)'
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                self.map_dict[col] = 'DATETIME'
            elif data[col].dtype == 'boolean':
                self.map_dict[col] = 'BOOLEAN'
            else:
                self.map_dict[col] = 'TEXT'
        for col,dtype in exceptions.items():
            self.map_dict[col] = dtype
        return self.map_dict
    
    def __str__(self):
        s = "Data Type Mapping:\n"
        mk = max(len(k) for k in self.map_dict.keys())
        for col, dtype in self.map_dict.items():
            s += f"{col.ljust(mk)}: {dtype}\n"
        return s

            
