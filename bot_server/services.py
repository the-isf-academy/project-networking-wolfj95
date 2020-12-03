# service.py
# This file should contain the functions used to run your service.
#
# Author: Jacob Wolf

import requests

# service provided and expected arguments

services_dict = {
        "add": [float, float],
        "subtract": [float, float],
        "multiply": [float, float],
        "divide": [float, float],
        "search": [str],
        "help": []
}

def add(a, b):
    """ Adds two numbers together and returns the result.
    """
    return a+b

def subtract(a, b):
    """ Subtracts b from a returns the result.
    """
    return a-b 

def multiply(a, b):
    """ Multiplies a by b and returns the result.
    """
    return a*b

def divide(a, b):
    """ Dicvides a by b and returns the result.
    """
    return a/b

def search(query):
    """ Searches Wolfram Alpha for a query and returns
    the result.
    """
    app_id = "RPWJ2Y-U4APVU2YT7"
    params = {
            "i": query,
            "appid": app_id
    }
    address = "http://api.wolframalpha.com/v1/result"
    r = requests.get(address, params=params)
    if r.ok:
        return r.text
    else:
        return "Sorry, there was an error contacting Wolfram Alpha ({}: {})".format(r.status_code, r.reason)
