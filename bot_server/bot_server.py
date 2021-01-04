# bot_server.py
# by Jacob Wolf

import traceback
from flask import Flask, request, render_template
from bot_harness import inspect_services

import services
from services import services_dict, add, subtract, multiply, divide, search, help
from helpers import check_payload, parse_service_and_args_from, format_arguments

class ServiceArgumentError(Exception):
    pass

name, description, service_properties = inspect_services(services)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        try:
            service_name = request.form['service']
            service = getattr(services, service_name)
            service_args = get_service_args(service_name, request.form)
            print("Calling service {} with arguments: {}".format(service_name, service_args))
            service_response = service(**service_args)
            print("Result:".format(service_response))
            message = {
                "status": "success",
                "content": service_response
            }
        except IndexError:
            message = {"status": "error", "content": "There is no service called '{}'.".format(service_name)}
        except AttributeError:
            message = {"status": "error", "content": "The function '{}' is not defined in services.py".format(service_name)}
        except ServiceArgumentError as e:
            message = {"status": "error", "content": str(e)}
        except Exception as e:
            print(traceback.format_exc())
            message = {"status": "error", "content": "The function '{}' raised an error.".format(service_name)}
    else:
        message = None
        service_name = service_properties[0]['name']
        service_args = {}
        
    return render_template('index.html', name=name, description=description, services=service_properties, message=message, service_name=service_name, service_args=service_args)

def get_service_args(service_name, form):
    "Reads service arguments from the form and casts them to the appropriate type"
    props = [s for s in service_properties if s['name'] == service_name][0]
    args = {}
    for argname, argtype in props['arguments']:
        try:
            args[argname] = argtype(form[argname])
        except IndexError:
            raise ServiceArgumentError("Expected argument '{}'".format(argname))
        except ValueError:
            raise ServiceArgumentError("Could not parse '{}' value '{}' as type {}".format(argname, form[argname], argtype))
    return args



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
def help_wrapper():
    return { "msg": help() }

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

