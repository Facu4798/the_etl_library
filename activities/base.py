class BaseActivity:
    def __init__(self,env,function=None,input=None,id=None,parent=None):
        self.env = env
        if id is None:
            self.id = len(self.env.items)
        else:
            self.id = id
        self.function = function
        self.input = input
        self.env._add_item(self,parent)
        
    def run(self,input=None):
        if self.function is None:
            return self.input
        output = self.function(self.input)
        self.input = None # clear input to release memory
        return output

    def __str__(self):
        return f"Base Activity {self.id} in {self.env}"
    