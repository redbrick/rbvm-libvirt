import json
import pdb

def rpc(func):
    """
    Executes an RPC function passing in JSON dictionary entries as kwargs entries.
    """
    def wrapper(*args, **kwargs):
        
        if (kwargs.keys().__len__() > 0):
            json_kwargs = json.loads(kwargs.keys()[0])
        else:
            json_kwargs = {}
        
        return func(**json_kwargs)
    return wrapper

def json_encode(**kwargs):
    """
    Encodes kwargs as JSON and returns it in string form.
    """
    return json.dumps(kwargs)