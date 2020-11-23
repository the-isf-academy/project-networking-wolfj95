# bot_server.py
# by Jacob Wolf

from flask import Flask, request
from services import services_dict, add, subtract, multiply, divide, search
from helpers import check_payload, parse_service_and_args_from, format_arguments

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello from the cs10 calculator bot!"

@app.route('/message', methods=['POST'])
def new_message():
    data = request.get_json()

    # check for errors in payload
    errors = check_payload(data, ["sender", "msg", "timestamp"])
    if len(errors) > 0:
        return {"errors": errors}, 400

    # parse message, format args, and check for errors in service and arguments
    msg = data["msg"]
    service, arguments, errors = parse_service_and_args_from(msg, services_dict)
    if len(errors) > 0:
        return {"errors": errors}, 400

    # perform service
    if service == "help":
        return { "msg": help() }
    elif service == "add":
        return { "msg": add(arguments[0], arguments[1]) }
    elif service == "subtract":
        return { "msg": subtract(arguments[0], arguments[1]) }
    elif service == "multiply":
        return { "msg": multiply(arguments[0], arguments[1]) }
    elif service == "divide":
        return { "msg": divide(arguments[0], arguments[1]) }
    elif service == "search":
        return { "msg": search(arguments[0]) }
    else:
        return { "msg": "Sorry, I don't know how to do that." }

@app.route('/help', methods=['GET'])
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
    return { "msg": message }

@app.route('/add', methods=['GET'])
def add_wrapper():
    data = request.get_json()
    errors = check_payload(data, ["num0", "num1"])
    if len(errors) > 0:
        return {"errors": errors}, 400
    a = float(data['num0'])
    b = float(data['num1'])
    numsum = add(a, b)
    return { "value": numsum }

@app.route('/subtract', methods=['GET'])
def subtract_wrapper():
    data = request.get_json()
    errors = check_payload(data, ["num0", "num1"])
    if len(errors) > 0:
        return {"errors": errors}, 400
    a = float(data['num0'])
    b = float(data['num1'])
    difference = subtract(a, b)
    return { "value": difference }

@app.route('/multiply', methods=['GET'])
def multiply_wrapper():
    data = request.get_json()
    errors = check_payload(data, ["num0", "num1"])
    if len(errors) > 0:
        return {"errors": errors}, 400
    a = float(data['num0'])
    b = float(data['num1'])
    product = multiply(a, b)
    return { "value": product }

@app.route('/divide', methods=['GET'])
def divide_wrapper():
    data = request.get_json()
    errors = check_payload(data, ["num0", "num1"])
    if len(errors) > 0:
        return {"errors": errors}, 400
    a = float(data['num0'])
    b = float(data['num1'])
    quotient = divide(a, b)
    return { "value": quotient }

@app.route('/search', methods=['GET'])
def search_wrapper():
    data = request.get_json()
    errors = check_payload(data, ["query"])
    if len(errors) > 0:
        return {"errors": errors}, 400
    query = data['query']
    result = search(query)
    return { "result": result }

