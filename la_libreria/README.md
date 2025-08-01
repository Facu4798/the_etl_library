# la_libreria

A Python library for ETL operations with credential management and database connectors.

## Installation

You can install this library directly from the GitHub repository:

```bash
pip install git+https://github.com/Facu4798/the_etl_library.git
```

## Usage
In a python file or jupyter notebook type:

```python
import la_libreria
```

# Table of contents
**Modules**
- authentication
- connectors
- enviroment
- base

# Authentication

## Credentials `class`:

```py
Credentials(params = {})
```
**params:** A dictionary of key values representing different credentials .eg:
``{"user":"facu","password":1234}``

*NOTE: this parameter can be left as `{}` and credentials added later with the `add_credential` method*

### Methods
`add_credential(self, key=None, value=None,dict=None)`
This method adds a single credential to the `Credentials` dictionary.

- **key:** Name of the credential 
- **value:** Value of the credential

`show(self)`
prints the credentials in the object

`save(self, name=None, overwrite=False)`
Saves the credentials in the object to a json file in the installation directory of the module.
- **name:** Name of the file. The file name must not include the file extension
- **overwrite:** True/False. Whether to overwrite a file with existing name. If it's set to false and file exists, it won't write a file.

`load(self, name=None)`
Loads a credentials json file to the object
- **name:** Name of the json file. The file name must not include the file extension.

`delete(self, name)`
Delets a credentials json file in the module installation directory.
- **name:** Name of the json file. The file name must not include the file extension.

### Attributes
`dict`
A dictionary of key:value pairs containing all the credentials in the object.