class Credentials:
    def __init__(self,params):
        for key, value in params.items():
            setattr(self, key, value)

    def add_credential(self, key, value):
        setattr(self, key, value)

    def show(self):
        print(self.__str__())
    def __str__(self):
        s = self.__dict__
        mk = max(len(k) for k in s.keys())
        s2 = "Credentials:\n"
        for k, v in s.items():
            s2 += f"{k.ljust(mk+2)} = {v}\n"
        return s2