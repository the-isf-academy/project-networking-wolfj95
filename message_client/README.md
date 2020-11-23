# Message Client
**🚫✏️ You do not need to change anything in this directory for the project. This is just for your reference. 🚫✏️**

## Running the message client application
```
$ python client.py
```

After running the command above, the application will ask you for the server address of the message
server you want to connect to. By default, the application will connect to `localhost:4000`, the address
at which the message server is setup to run. If you would like to access a different message server,
like another student's or the class server, enter the server's IP address and port in the following
form:
```
What server would you like to use? (default, return) <IP ADDRESS>:<PORT>
```

## Files
Here's an overview of the files in the directory.

### `client.py`
This file runs the core funcationality of the message client. You wrote most of this code
back in the HTTP Lab! However, it has been altered slightly to allow the application to register
bot users.

Additionally, the application has been updated to allow a user to change their password or server
address. This allows you to change the address of a bot without having to create a new user.

### `view.py`
This file defines the `View` class used by the message server application. All input and output
after the setup goes through here!
