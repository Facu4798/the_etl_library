import os
import json
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
