# Client file for server lab (client.py)
# By: Will Chau

import requests, sys, json

from view import TerminalView

DEFAULT_MSG_SERVER = '127.0.0.1:4000'

#error codes
SUCCESS = 1
USER_EXISTS_IN_DB = 10
USER_DOES_NOT_EXIST = 11
AUTHENTICATION_FAILED = 12
NO_MSGS = 13

class Client():

    def __init__(self, server_address):

        authenticated = False
        self.user = ''
        self.server_address = server_address
        self.view = TerminalView()

    def start(self):
        while True:
            choices = ["Register a New User", "Send a Message", "Get Your Messages", "Edit Registration", "Quit"]
            choice = self.view.menu_choice(choices)
            if choice == 0:
                self.register()
            elif choice == 1:
                self.send_message()
            elif choice == 2:
                self.get_messages()
            elif choice == 3:
                self.edit_registration()
            elif choice == 4:
                break
            else:
                pass

    def get_server_address(self):
        while True:
            server_address = self.view.get_server_address()
            if server_address.find("http://") == -1 and server_address.find("https://") == -1:
                server_address = "http://" + server_address
            try:
                ping_address = server_address + "/"
                r = requests.get(ping_address, timeout=5)
                if r.status_code == requests.codes.ok:
                    break
            except:
                pass
            self.view.report_ping_failed()
        return server_address
    
    def register(self):
        '''Gets a username and password (with a password verification) and sends it to the server'''

        user = self.view.get_username()
        password = self.view.get_password()
        confirm = self.view.get_password_confirm()
        if password == confirm:
            bot_server_address = None
            if self.view.check_if_bot():
                bot_server_address = self.get_server_address()
            register_address = self.server_address + "/register"
            payload = {"username": user, "password": password, "server_address": bot_server_address}
            r = requests.post(register_address, json=payload)
            response = r.json()
            if r.ok:
                if response == USER_EXISTS_IN_DB:
                    self.view.error(USER_EXISTS_IN_DB, "User already exists. Please try again.")
                    return USER_EXISTS_IN_DB
                else:
                    self.view.success("Thank you for registering!")
                    return SUCCESS
            else:
                self.view.error(r.status_code, r.reason)
                return r.status_code
        else:
            self.view.error(AUTHENTICATION_FAILED, "Passwords do not match.")

    def authenticate(self):
        ''' Gets a username and password and sends it to the server'''

        username = self.view.get_username()
        password = self.view.get_password()
        auth_address = self.server_address + "/auth"
        payload = {"username": username, "password": password}
        r = requests.get(auth_address, json=payload)
        response = r.json()
        if response == SUCCESS:
            self.user = username
            return SUCCESS
        else:
            return r.json()

    def get_messages(self):
        isAuthenticated = self.authenticate()
        if isAuthenticated == SUCCESS:
            get_address = self.server_address + "/get_messages"
            payload = {"username": self.user}
            r = requests.get(get_address, json=payload)
            if r.ok:
                response_content = r.json()
                messageList = response_content['messages']
                self.view.display(messageList, len(messageList))
            else:
                self.view.error(r.status_code, r.reason)
        elif isAuthenticated == USER_DOES_NOT_EXIST:
            self.view.error(USER_DOES_NOT_EXIST, "User does not exist.")
        else:
            self.view.error(AUTHENTICATION_FAILED, "Authentication Failed.")

    def send_message(self):
        isAuthenticated = self.authenticate()
        if isAuthenticated == SUCCESS:
            # Post the message to the server
            send_address = self.server_address + "/"
            payload = self.view.create_message(self.user)
            r = requests.post(send_address, json=payload)
            if r.ok:
                self.view.success('Message Sent!')
            else:
                self.view.error(r.status_code, r.text)
        elif isAuthenticated == USER_DOES_NOT_EXIST:
            self.view.error(USER_DOES_NOT_EXIST, "User does not exist.")
        else:
            self.view.error(AUTHENTICATION_FAILED, "Authentication Failed.")

    def edit_registration(self):
        user = self.view.get_username()
        password = self.view.get_password()

        new_password = None
        if self.view.change("password"):
            new_password = self.view.get_password()
            confirm = self.view.get_password_confirm()
            if new_password != confirm:
                self.view.error(AUTHENTICATION_FAILED, "Passwords do not match.")
                return

        new_server_address = None
        if self.view.change("server address"):
            new_server_address = self.get_server_address()

        edit_address = self.server_address + "/edit"
        payload = {"username": user, "old_password": password, "new_password": new_password, "server_address": new_server_address}
        r = requests.post(edit_address, json=payload)
        response = r.json()
        if r.ok:
            if response == SUCCESS:
                self.view.success("Registration updated.")
                return SUCCESS
            elif response == USER_DOES_NOT_EXIST:
                self.view.error(USER_DOES_NOT_EXIST, "User does not exist.")
                return USER_DOES_NOT_EXIST
            elif response == AUTHENTICATION_FAILED:
                self.view.error(AUTHENTICATION_FAILED, "Authentication failed.")
                return AUTHENTICATION_FAILED
        else:
            self.view.error(r.status_code, r.reason)
            return r.status_code


def set_up_client():
    while True:
        server_address = input("What server would you like to use? (default, return) ")
        if server_address == "":
            server_address = DEFAULT_MSG_SERVER
        if server_address.find("http://") == -1 and server_address.find("https://") == -1:
            server_address = "http://" + server_address
        try:
            ping_address = server_address + "/ping"
            r = requests.get(ping_address, timeout=5)
            if r.status_code == requests.codes.ok:
                break
        except:
            pass
        print("Sorry, we can't access that server. Try another.")

    c = Client(server_address)
    c.start()

if __name__ == "__main__":
    set_up_client()
