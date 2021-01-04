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

def help():
    message = "Hello! I'm the math bot. I can peform addition, subtraction,\n" \
            "multiplication, or division on any two numbers. I can also answer\n" \
            "your questions about mathematics (and osome other things too!).\n" \
            "To use my services, send me a message like \"add 3 5\" and I will\n" \
            "perform the calculation and send you the result in a message.\n" \
            "\n" \
            "Here are the commands you can use:\n" \
            "add [num0] [num1]\n" \
            "subtract [num0] [num1]\n" \
            "multiply [num0] [num1]\n" \
            "divide [num0] [num1]\n" \
            "search [search query or question]"
    return message

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
