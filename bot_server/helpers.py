# helpers.py
# by Jacob Wolf
#
# This file offers functions to help with running a bot server

def check_payload(values_dict, expected):
    """
    A helper to ensure that the data sent with an HTTP request
    contains all expected params and no unexpected params. 
    """
    errors = []
    if values_dict is None:
        return ["no data provided"]
    for key in values_dict.keys():
        if key not in expected:
            errors.append("unexpected field: {}".format(key))
    for key in expected:
        if key not in values_dict.keys():
            errors.append("missing field: {}".format(key))
    return errors

def parse_service_and_args_from(msg, services_dict):
    """ Parses the message, msg, sent to the bot into
    the service and the arguments for the service, 
    formats the arguments and checks for errors,
    and returns serivce, arguments, and errors as a tuple.
    Arguments should be single words, separated by spaces 
    (execpt for the last argument).
    Arguments will be returned as a list of values based 
    on the expected values defined in the services_dict.
    """
    if len(msg) == 0:
        return ("", [], ["No content in message."])
    else:
        service, *arguments = msg.split(maxsplit=1)
        if len(arguments) > 0:
            arguments = arguments[0]
            expected_args = len(services_dict[service])
            arguments = arguments.split(maxsplit=expected_args-1)
    arguments, errors = format_arguments(service, arguments, services_dict)
    return (service, arguments, errors)

def format_arguments(service, args, services_dict):
    """ Checks to make sure the arguments are valid given
    the defintions in the services_dict and formats the arguments into the types
    defined in the services_dict.
    """
    formatted_args = []
    errors = []
    if service not in services_dict.keys():
        errors.append("Service not available.")
    else:
        # not right number of args
        if len(args) != len(services_dict[service]):
            errors.append("Expected {} arguments, but got {}". format(len(services_dict[service]), len(args)))

        # arg types don't match service_dict
        for i, arg in enumerate(args):
            try:
                arg = services_dict[service][i](arg)
                formatted_args.append(arg)
            except:
                errors.append("Type of argument {} is incorrect. {} expected.".format(i, services_dict[service][i]))
    return (formatted_args, errors)
