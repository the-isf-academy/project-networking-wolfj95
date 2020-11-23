# cs10 Networking Project
In This project, you will develop a bot that runs on the cs10 messaging platform and provides a service to users (including other bots!).

## Repo outline
* [bot_server](bot_server/) - Server to run your bot services (*where you will write your code for this lab*)
  * [server.py](bot_server/bot_server.py) - Server file with route implementations (**add code here**)
  * [services.py](bot_server/services.py) - Module containing the services your bot performs (**add code here**)
  * [helpers.py](bot_server/helpers.py) - Module containing helper functions to support your bot (**use these, but don't edit**)
  * [run.sh](bot_server/run.sh) - Script to run the bot_server from the command line (*no need to edit*)
* [message_server](message_server/) - Server to run the cs10 messaging platform (*no need to edit*)
  * [message_server.py](message_server/message_server.py) - Server file with messaging platform routes
  * [models.py](message_server/models.py) - Classes defining User and Message objects for the messaging platform
  * [run.sh](message_server/run.sh) - Script to run the message_server from the command line
* [message_client](message_client/) - Client application to interface with the messaging platform (*no need to edit*)
  * [client.py](message_client/client.py) - Client file that runs the messaging app
  * [view.py](message_client/view.py) - Class defining the View for the messaging app
  
## Getting started
Here's the general workflow for running all the parts of this project:
1. Start the `bot_server`
2. Start the `message_server`
3. Start `message_client`
4. Use the `message_client` to send and recieve messages

## Project spec
The details for what to do in this project can be found in the [project spec on the cs10 website](http://cs.fablearn.org/courses/cs10/unit00/project/)
