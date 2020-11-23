# Bot Server
**✏️ This is where you will write your code for this project. ✏️**

## Accessing the bot
To access the bot, you should follow the instructions below to run the bot server and access
it either locally or remotely.

### Running the Bot server
```
$ bash run.sh
```

### Accessing the server from your local computer
After running the server, you will be able to send HTTP requests to `http://localhost:5000`

Your can test the server locally by running the following command in your terminal:
```
$ http get http://localhost:5000/
HTTP/1.0 200 OK
Content-Length: 32
Content-Type: text/html; charset=utf-8
Date: Wed, 18 Nov 2020 08:26:43 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

Hello from the cs10 message bot!
```

### Accessing the server from another computer
Another computer on the same wifi network can access your bot server by using your IP address.

On a Mac, find your IP address by running the following command in your terminal:
```
$ ipconfig getifaddr en0
192.168.XX.XX
```

Give your IP address to your friend, and on their computer they can run the following command in their terminal:
(Be sure to replace the XXX with the numbers you found for your IP address!)
```
$ http get http://192.168.XXX.XX:5000/
HTTP/1.0 200 OK
Content-Length: 32
Content-Type: text/html; charset=utf-8
Date: Wed, 18 Nov 2020 08:26:43 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

Hello from a cs10 message bot!
```

## Services
✏️ **EDIT THIS SECTION OF THE README TO DESCRIBE THE SERVICES YOUR BOT PROVIDES.** ✏️

Here's an example:

| Service  | Description                                                                                   | API Route   | Message Platform Command | Parameters (with types)                                                                                                                                        | Example Usage       | Returns                                |
|----------|-----------------------------------------------------------------------------------------------|-------------|--------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------|----------------------------------------|
| add      | Adds two numbers and returns the sum                                                          | `/add`      | `add num0 num1`            | `num0` (`float`): first number to sum, `num1` (`float`): second number to sum                                                                                      | add 3 4             | `{ "value": sum of nums }`             |
| subtract | Subtracts two numbers and returns the difference                                              | `/subtract` | `subtract num0 num1`       | `num0` (`float`): number, `num1` (`float`): number to subtract from num0                                                                                           | subtract 5 2        | `{ "value": difference of nums }`      |
| search   | Searches Wolfram Alpha for a query and returns the short text response                        | `/search`   | `search query`             | `query` (`string`): term to search for                                                                                                                           | search golden ratio | `{ "result": result }`                 |
| message  | Receives a message from the messaging platform, triggers the service, and returns the result. | `/message`  | n/a                      | `sender` (`string`): who sent the service request, msg (`string`): message containing service request, timestamp (`float`): the time in seconds since the  epoch | n/a                 | `{ "msg": result of service request }` |


## Files
Here's an overview of the files in the directory and what you should do with them.

### `bot_server.py`
This file will define the routes for your message bot. The bot should be able
to serve routes for the following endpoints:

* `/` (`GET`) - This route just helps us know if the server is running. Nothing to
change here.
* `/message` (`POST`) - This route recieves a message from the message server, triggers
the bot's service, and responds appropriately based on the service requested. Currently,
the route parses the message sent to the bot into the `service` requested and a list
of `arguments` passed with the message. Additionally, the route checks the formatting of
the service request and generates an error if anything is wrong. However, currently the
route can only respond to a request for help.
**✏️ You will need to edit this function so that is initiates the service from the `services`
module that the user requested and responds appropriately.**
* `/help` (`GET`) - This route should return a message describing to a user what your bot
does and how to use it.
**✏️ You will need to edit this route so that the message accurately describes your bot's
services.**
* `/<your service routes>` (`GET`/`POST`) - **✏️ These routes are totally up to you to design and
write.** You should have a route for each of the services your bot provides. However, the functions
for these routes shouldn't perform the services themselves. Instead, they should call functions
from your `services` module (described below).

### `services.py`
This module defines functions for each of the services your bot provides.

**✏️ You should write any function that your bot needs to perform it's service in this file.**
For example, if your bot will translate a message to another language, your module should
probably contain a `translate()` function.

This module also contains a dictioanry object called `services_dict`. **✏️ You should edit this
dictionary to contain key-value pairs for each service your bot provides where the key is the
service as a string and the value is a list of the types of arguments you need to perform that
service.** For example, if you were writing a calculator bot, your `services_dict` might look like
this:
```
services_dict = {
        "add": [float, float],
        "subtract": [float, float],
        "multiply": [float, float],
        "divide": [float, float],
        "help": []
}
```
*Note that one of the services in your `services_dict` must be `"help": []`.*

As a reminder, here is a list of the types you might need for your bot:
* `int` - an integer (i.e. `13`)
* `float` - a decimal number (i.e. `3.14`)
* `str` - a string of characters (i.e. `"Hello, world!")
* `bool` - a `True` or `False` value

*Note: If your service needs a string with multiple words as an argument, this MUST be the last
argument in the list.*

### `helpers.py`
This module contains helper functions used by the bot server.

#### `check_payload(values_dict, expected)`
Ensures that the data sent with an HTTP request
contains all expected params and no unexpected params.

<ins>Parameters:</ins>
* `values_dict` - a dictionary of values sent with the HTTP request
* `expected` - a list of the values expected in the `values_dict`

<ins>Returns:</ins>
* a list of errors found while checking payload (empty list implies no errors in payload)

#### `parse_service_and_args_from(msg, services_dict)`
Parses the message, `msg`, sent to the bot into the service and the arguments for the service, 
formats the arguments and checks for errors, and returns serivce, arguments, and errors as a tuple.
Arguments in the `msg` should be single words, separated by spaces (execpt for the last argument).
Arguments will be returned as a list of values based on the expected values defined in the `services_dict`.

<ins>Parameters:</ins>
* `msg` - string contain service and arguments separated by single spaces
* `services_dict` - dictionary with each service provided by the bot as a string paired with a list of the types
that service requires

<ins>Returns:</ins>
* a tuple containing:
  * the single word service string
  * a list of single word argument strings
  * a list of error strings

#### `format_arguments(service, args, services_dict)`
Checks to make sure the arguements, `args`, are valid given the defintions in the `services_dict` and 
formats the arguments into the types defined in the `services_dict`. A description of errors found is placed into the
errors list and returned

<ins>Parameters:</ins>
* `service` - single word string containing the service
* `args` - list of single word strings containing the arguments for the service
* `services_dict` - dictionary with each service provided by the bot as a string paired with a list of the types
that service requires

<ins>Returns:</ins>
* a tuple containing:
  * the list of formatted arguments
  * a list of error strings
