from inspect import getfullargspec

def inspect_services(services):
    """ Extracts service parameters from the module `services`, returning 
    name, description, services, where services is a list of service properties like:
    [
        {
            "name": "add",
            "description": "Adds two numbers together and returns the result.",
            "arguments": [("a", float), ("b", float)]
        }, ...
    ]
    """
    services_dict = getattr(services, "services_dict")
    name = getattr(services, "name") if hasattr(services, "name") else "Bot"
    description = getattr(services, "description") if hasattr(services, "description") else None
    params = []
    for key in services_dict.keys():
        fn = getattr(services, key)
        arg_names = getfullargspec(fn)[0]
        params.append({
            "name": key,
            "description": fn.__doc__.strip() if fn.__doc__ else "",
            "arguments": list(zip(arg_names, services_dict[key]))
        })
    return name, description, params

if __name__ == '__main__':
    import services
    print(inspect_services(services))
    
