class BaseActivity:
    def __init__(self,env,function=None,input=None,id=None,parent=None,output_name=None):
        self.env = env
        if id is None:
            self.id = len(self.env.items)
        else:
            self.id = id
        self.function = function
        self.parent = parent
        self.input = input
        self.env._add_item(self,parent)
        self.output = None
        if output_name == None:
            self.output_name = f"output_{self.id}"
        else:
            self.output_name = output_name

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
    