# Message Server
**🚫✏️ You do not need to change anything in this directory for the project. This is just for your reference. 🚫✏️**

## Running the message server
```
$ bash run.sh
```

## Accessing the server from your local computer
After running the server, you will be able to send HTTP requests to `http://localhost:4000`

Your can test the server locally by running the following command in your terminal:
```
$ http get http://localhost:4000/ping
HTTP/1.0 200 OK
Content-Length: 1
Content-Type: text/html; charset=utf-8
Date: Thu, 19 Nov 2020 00:25:46 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

1
```

## Accessing the server from another computer
Another computer on the same wifi network can access your bot server by using your IP address.

On a Mac, find your IP address by running the following command in your terminal:
```
$ ipconfig getifaddr en0
192.168.XX.XX
```

Give your IP address to your friend, and on their computer they can run the following command in their terminal:
(Be sure to replace the XXX with the numbers you found for your IP address!)
```
$ http get http://192.168.XXX.XX:4000/ping
HTTP/1.0 200 OK
Content-Length: 1
Content-Type: text/html; charset=utf-8
Date: Thu, 19 Nov 2020 00:25:46 GMT
Server: Werkzeug/1.0.1 Python/3.8.5

1
```

*Note: This server is setup to run on port 4000 to avoid interfering with the bot server. If you'd
like to change this setting, you can do so in the `run.sh` file. To do this, change the number after
`-p` in this line:*
```
FLASK_APP=message_server.py flask run --host=0.0.0.0 -p 4000
```

## Files
Here's an overview of the files in the directory.

### `message_server.py`
This file implements the routes for the message server. It is basically the same
file from the server lab, except now it allows for bot users on the platform.

To do this, the server asks for a server address when a user registers. If you want the user
to be a bot, put in the server address where your bot is running. While testing, this
can be your localhost address. Then, whenever a user on the platform sends a message to
a bot, the server reformats the message as an HTTP request and sends it to the bot's server.
When the bot responds, the response is transformed into a message to the original sender.

### `models.py`
This file defines the classes for `Message` and `User` objects on the server. These objects
are based on models from a package called SQL Alchemy. SQL Alchemy is a Python implementation
of a language called SQL, a language used to manage databases (like the one the messaging platform
uses to store users and messages!).
