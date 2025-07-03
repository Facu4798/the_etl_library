class Credentials:
    def __init__(self,params):
        for key, value in params.items():
            setattr(self, key, value)
        try:
            self.dict = params
        except:
            self.dict = {}

    def add_credential(self, key, value):
        """
        Add a credential to the credentials object
        - key: the name of the credential
        - value: the value of the credential
        
        ```
        creds = Credentials().add_credential("username", "admin")
        ```
        """
        setattr(self, key, value)
        self.dict[key] = value



    def show(self):
        print(self.__str__())

    def __str__(self):
        try:
            mk = max(len(k) for k in self.dict.keys())
            s2 = "Credentials:\n"
            for k, v in self.dict.items():
                s2 += f"{k.ljust(mk+2)} = {v}\n"
            return s2
        except:
            print("No credentials found")