class FileReader:
    def __init__(self,filepath,format,env=None,id=None,output_name=None):
        #attribute assignment
        self.env = env
        if id is None:
            self.id = len(self.env.items)
        else:
            self.id = id
        self.parent = None
        self.output = None
        if output_name == None:
            self.output_name = f"output_{self.id}"
        else:
            self.output_name = output_name
        
        # do add item if env is not None
        try:
            self.env._add_item(self,self.parent)
        except: pass
        self.filepath_ = filepath
        self.format_ = format

    def config(self,var,value):
        """
        update the configuration of the activity
        """
        setattr(self,var,value)
        return self

    def add_to_env(self,env):
        """
        add the activity to the environment
        
        **NOTE:** *this method should be called only once the activity is fully configured and its parents are set(if applicable)*
        """
        try:
            if self.env is not None:
                raise ValueError("Activity is already added to an environment.")
        except:
            pass
        self.env = env
        self.env._add_item(self,self.parent)
        return self
    
    def run(self):
        if self.function is None:
            return self.input
        def read_file(filepath, format):
            import polars as pl
            if format not in ['csv','parquet','json','ipc','ndjson','excel']:
                raise ValueError(f"""Unsupported format: {format}. 
                Supported formats are: csv, parquet, json, ipc, ndjson, excel.""")
            read_func = getattr(pl, f"scan_{format}")
            return read_func(filepath)

        self.output = read_file(self.filepath_, self.format_)

        if self.env.logger_obj is not None:
            self.env.logger_obj.log(f"File {self.filepath_} read.")
        return {self.output_name : self.output}

    def __str__(self):
        return f"File reader activity {self.id} in {self.env}"

class tableRegister:
    def __init__(self,data,table_name,env=None,id=None,output_name=None,parent=None):
        #attribute assignment
        self.env = env
        if id is None:
            self.id = len(self.env.items)
        else:
            self.id = id
        self.parent = parent
        self.input = data
        self.output = None
        if output_name == None:
            self.output_name = f"output_{self.id}"
        else:
            self.output_name = output_name
        self.table_name = table_name

        # do add item if env is not None
        try:
            self.env._add_item(self,self.parent)
        except: pass

    def config(self,var,value):
        """
        update the configuration of the activity
        """
        setattr(self,var,value)
        return self

    def add_to_env(self,env):
        """
        add the activity to the environment
        
        **NOTE:** *this method should be called only once the activity is fully configured and its parents are set(if applicable)*
        """
        try:
            if self.env is not None:
                raise ValueError("Activity is already added to an environment.")
        except:
            pass
        self.env = env
        self.env._add_item(self,self.parent)
        return self

    def run(self):
        try:
            ctx.register(self.table_name,self.input)
        except:
            raise ValueError("Input is not a polars DataFrame or LazyFrame.")
        self.output = None
        if self.env.logger_obj is not None:
            self.env.logger_obj.log(f"Table {self.table_name} registered.")
        return {self.output_name : self.output}


class sqlTransformer:
    def __init__(self,query,env=None,input=None,id=None,output_name=None,parent=None):
        #attribute assignment
        self.env = env
        if id is None:
            self.id = len(self.env.items)
        else:
            self.id = id
        self.parent = parent
        self.input = input
        self.output = None
        if output_name == None:
            self.output_name = f"output_{self.id}"
        else:
            self.output_name = output_name
        self.query = query

        # do add item if env is not None
        try:
            self.env._add_item(self,self.parent)
        except: pass
    
    def config(self,var,value):
        """
        update the configuration of the activity
        """
        setattr(self,var,value)
        return self
    
    def add_to_env(self,env):
        """
        add the activity to the environment
        
        **NOTE:** *this method should be called only once the activity is fully configured and its parents are set(if applicable)*
        """
        try:
            if self.env is not None:
                raise ValueError("Activity is already added to an environment.")
        except:
            pass
        self.env = env
        self.env._add_item(self,self.parent)
        return self
    
    def run(self):
        try:
            self.output = ctx.execute(self.query)
        except:
            self.output = None
            raise ValueError("Input is not a polars DataFrame or LazyFrame.")
        if self.env.logger_obj is not None:
            self.env.logger_obj.log(f"SQL query executed at activity {self.id}.")
        return {self.output_name : self.output}
