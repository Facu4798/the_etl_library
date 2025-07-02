class Credentials:
    def __init__(self,params):
        for key, value in params.items():
            setattr(self, key, value)
        try:
            self.dict = params
        except:
            self.dict = {}

    def add_credential(self, key, value):
        setattr(self, key, value)
        self.dict[key] = value

    def persist(self,service):
        import keyring
        for k, v in self.dict.items():
            try:
                keyring.set_password(service, k, v)
            except Exception as e:
                print(f"Error persisting for {k}: {e}")
    
    def get_from_system(self,service,names):
        import keyring
        self.dict= {}
        #get credentials that match the service
        for k in names:
            try:
                self.dict[k] = keyring.get_password(service, k)
            except Exception as e:
                print(f"Error retrieving credentials: {e}")


    def remove_from_system(self,service,names):
        import keyring
        for k in names:
            try:
                keyring.delete_password(service, k)
            except Exception as e:
                print(f"Error removing {k}: {e}")



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