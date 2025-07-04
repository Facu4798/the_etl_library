import os
import json
import pickle
from pathlib import Path

class Credentials:
    def __init__(self,params = {}):
        for key, value in params.items():
            setattr(self, key, value)
        self.dict = params


    def _get_credentials_directory(self):
        """Get the directory where credentials should be stored (in the library installation)"""
        
        module_dir = Path(__file__).parent # Get the directory where this module is installed
        credentials_dir = module_dir / "credentials"
        
        return credentials_dir

    def _get_credential_file_path(self, name=None):
        """Get the full path for a credential file"""
        return self._get_credentials_directory() / f"{name}.json"

    def list(self):
        """
        lists all the credentials in the saved credentials directory
        """
        import os
        for f in os.listdir(self._get_credentials_directory()):
            print(f)

    def save(self, name=None, overwrite=False):
        """
        Save credentials to a file in the library installation directory
        - name: name for the credential file
        - overwrite: whether to overwrite existing files (default: False)
        
        Returns: path to the saved file or None if failed
        """
        if len(self.dict.keys())==0:
            print("No credentials to save")
            return None
        
        file_path = self._get_credential_file_path(name)
        
        if file_path.exists() and not overwrite:
            print(f"Credential file '{file_path.name}' already exists. Use overwrite=True to replace it.")
            return None
        
        try:
            with open(file_path, 'w') as f:
                json.dump(self.dict, f, indent=2)
            
            print(f"Credentials saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return None

    def load(self, name=None):
        """
        Load credentials from a file in the library installation directory
        - name: name of the credential file to load
        
        Returns: True if successful, False otherwise
        """
        file_path = self._get_credential_file_path(name)
        
        if not file_path.exists():
            print(f"Credential file '{file_path.name}' not found")
            return False
        
        try:
            with open(file_path, 'r') as f:
                loaded_creds = json.load(f)
            
            # Update the current credentials
            self.dict.update(loaded_creds)
            for key, value in loaded_creds.items():
                setattr(self, key, value)
            
            print(f"Credentials loaded from: {file_path}")
            return self
            
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return self

    
    def delete(self, name):
        """
        Delete a saved credential file
        - name: name of the credential file to delete
        
        Returns: True if successful, False otherwise
        """
        file_path = self._get_credential_file_path(name)

        if not file_path.exists():
            print(f"Credential file '{file_path.name}' not found")
            return False
        
        try:
            file_path.unlink()
            print(f"Credential file '{file_path.name}' deleted successfully")
            return True
        except Exception as e:
            print(f"Error deleting credential file: {e}")
            return False

    def add_credential(self, key=None, value=None,dict=None):
        """
        Add a credential to the credentials object
        - key: the name of the credential
        - value: the value of the credential
        
        >>> creds = Credentials().add_credential("username", "admin")
        """
        if dict != None:
            for k, v in dict.items():
                setattr(self, k, v)
                self.dict[k] = v
        if key!=None and value != None:
            setattr(self, key, value)
            self.dict[key] = value
        return self  # Enable method chaining

    def show(self):
        """
        Show the current credentials in the Credentials object.
        """
        return self.__str__()

    def __str__(self):
        try:
            if not self.dict:
                return "No credentials found"
            mk = max(len(k) for k in self.dict.keys())
            s2 = "Credentials:\n"
            for k, v in self.dict.items():
                s2 += f"{k.ljust(mk+2)} = {v}\n"
            return s2
        except:
            return "No credentials found"
