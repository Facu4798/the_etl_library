import os
import json
import pickle
from pathlib import Path

class Credentials:
    def __init__(self,params):
        for key, value in params.items():
            setattr(self, key, value)
        try:
            self.dict = params
        except:
            self.dict = {}


    def _get_credentials_directory(self):
        """Get the directory where credentials should be stored (in the library installation)"""
        # Get the directory where this module is installed
        module_dir = Path(__file__).parent
        credentials_dir = module_dir / ".credentials"
        
        # Create the directory if it doesn't exist
        credentials_dir.mkdir(exist_ok=True)
        
        return credentials_dir

    def _get_credential_file_path(self, name=None, file_format='json'):
        """Get the full path for a credential file"""
        if name is None:
            name = self.credential_name or "default"
        
        filename = f"{name}.{file_format}"
        return self._credentials_dir / filename

    def save(self, name=None, file_format='json', overwrite=False):
        """
        Save credentials to a file in the library installation directory
        - name: name for the credential file (defaults to credential_name or 'default')
        - file_format: 'json' or 'pickle' (default: 'json')
        - overwrite: whether to overwrite existing files (default: False)
        
        Returns: path to the saved file or None if failed
        """
        if not self.dict:
            print("No credentials to save")
            return None
        
        file_path = self._get_credential_file_path(name, file_format)
        
        if file_path.exists() and not overwrite:
            print(f"Credential file '{file_path.name}' already exists. Use overwrite=True to replace it.")
            return None
        
        try:
            if file_format.lower() == 'json':
                with open(file_path, 'w') as f:
                    json.dump(self.dict, f, indent=2)
            elif file_format.lower() == 'pickle':
                with open(file_path, 'wb') as f:
                    pickle.dump(self.dict, f)
            else:
                print(f"Unsupported file format: {file_format}. Use 'json' or 'pickle'.")
                return None
            
            print(f"Credentials saved to: {file_path}")
            return str(file_path)
            
        except Exception as e:
            print(f"Error saving credentials: {e}")
            return None

    def load(self, name=None, file_format='json'):
        """
        Load credentials from a file in the library installation directory
        - name: name of the credential file to load (defaults to credential_name or 'default')
        - file_format: 'json' or 'pickle' (default: 'json')
        
        Returns: True if successful, False otherwise
        """
        file_path = self._get_credential_file_path(name, file_format)
        
        if not file_path.exists():
            print(f"Credential file '{file_path.name}' not found in {self._credentials_dir}")
            return False
        
        try:
            if file_format.lower() == 'json':
                with open(file_path, 'r') as f:
                    loaded_creds = json.load(f)
            elif file_format.lower() == 'pickle':
                with open(file_path, 'rb') as f:
                    loaded_creds = pickle.load(f)
            else:
                print(f"Unsupported file format: {file_format}. Use 'json' or 'pickle'.")
                return False
            
            # Update the current credentials
            self.dict.update(loaded_creds)
            for key, value in loaded_creds.items():
                setattr(self, key, value)
            
            print(f"Credentials loaded from: {file_path}")
            return True
            
        except Exception as e:
            print(f"Error loading credentials: {e}")
            return False

    def list_saved_credentials(self):
        """List all saved credential files"""
        if not self._credentials_dir.exists():
            print("No credentials directory found")
            return []
        
        credential_files = []
        for file_path in self._credentials_dir.iterdir():
            if file_path.is_file() and file_path.suffix in ['.json', '.pickle']:
                credential_files.append({
                    'name': file_path.stem,
                    'format': file_path.suffix[1:],  # Remove the dot
                    'path': str(file_path),
                    'size': file_path.stat().st_size
                })
        
        if credential_files:
            print("Saved credentials:")
            for cred in credential_files:
                print(f"  - {cred['name']} ({cred['format']}) - {cred['size']} bytes")
        else:
            print("No saved credentials found")
        
        return credential_files

    def delete_saved_credential(self, name, file_format='json'):
        """
        Delete a saved credential file
        - name: name of the credential file to delete
        - file_format: 'json' or 'pickle' (default: 'json')
        
        Returns: True if successful, False otherwise
        """
        file_path = self._get_credential_file_path(name, file_format)
        
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
        return self  # Enable method chaining



    def show(self):
        print(self.__str__())

    def __str__(self):
        try:
            if not self.dict:
                return "No credentials found"
            mk = max(len(k) for k in self.dict.keys())
            s2 = "Credentials:\n"
            for k, v in self.dict.items():
                s2 += f"{k.ljust(mk+2)} = {v}\n"
            return s2
        except Exception:
            return "No credentials found"