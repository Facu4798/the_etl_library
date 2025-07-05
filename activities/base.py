class BaseActivity:
    def __init__(self,env=None,function=None,input=None,id=None,parent=None,output_name=None):
        self.env = env
        if id is None:
            self.id = len(self.env.items)
        else:
            self.id = id
        self.function = function
        self.parent = parent
        self.input = input
        try:
            self.env._add_item(self,parent)
        except: pass
        self.output = None
        if output_name == None:
            self.output_name = f"output_{self.id}"
        else:
            self.output_name = output_name
            
    def config(self,var,value):
        """
        update the configuration of the activity
        """
        setattr(self,var,value)
        return self
    
    def add_parent(self,parent):
        """
        add a parent activity to the current activity
        """
        if self.parent is None:
            self.parent = parent
        elif type(self.parent) == list:
            self.parent.append(parent)
        else:
            self.parent = [self.parent, parent]
    
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
    
    def run(self,input=None):
        if self.function is None:
            return self.input
        if self.input is None:
            self.output = self.function(input)
        else:    
            self.output = self.function(**self.input)
        self.input = None # clear input to release memory
        return {self.output_name : self.output}

    def __str__(self):
        return f"Base Activity {self.id} in {self.env}"
    