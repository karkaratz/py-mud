import paramiko
import re
import threading
import hashlib
from SSH_Handler import SSHHandler
import common

# SSH server parameters
host_key_path = 'key.pem'


class IncomingThread(threading.Thread):
    def __init__(self, incoming_queue, active_queue):
        super(IncomingThread, self).__init__()
        self.incoming_queue = incoming_queue
        self.active_queue = active_queue

    def run(self):
        while True:
            client_socket, addr = self.incoming_queue.get()
            print(f"Accepted connection from {addr}")

            # Handle the client using Paramiko directly
            self.handle_client(client_socket)

    def is_valid_password(self, pass1, pass2, ssh_handler):
        if pass1 != pass2:
            return "Password Do Not Match"

        # Check length
        if not (8 <= len(ssh_handler.decrypt_aes(ssh_handler.read_key(), pass1)) <= 16):
            return "Length not between 8 and 16 characters."

        # Check if alphanumeric and allowed special characters only
        if not re.match("^[a-zA-Z0-9/,.\\-?_*]*$", ssh_handler.decrypt_aes(ssh_handler.read_key(), pass1)):
            return "Password Contains Wrong Special Characters."

        return "ok"

    def is_valid_username(self, username):
        # Check length
        if not (3 <= len(username) <= 16):
            return False

        # Check if it starts with a number
        if not re.match(r'\D', username[0]):
            return False

        # Check if alphanumeric and underscores only
        if not re.match("^[a-zA-Z0-9_]*$", username):
            return False

        return True

    def handle_client(self, client_socket):
        # Create a Paramiko Transport object for the accepted connection
        transport = paramiko.Transport(client_socket)
        transport.add_server_key(paramiko.RSAKey(filename=host_key_path))

        # Start the SSH server
        ssh_handler = SSHHandler(None)  # Pass None for channel initially
        transport.start_server(server=ssh_handler)

        print("SSH server started")

        # Set the state to active
        # self.state_queue.put(("active", transport))
        channel = transport.accept(20)
        if channel is None:
            print("SSH channel negotiation failed.")
            return

        ssh_handler.channel = channel  # Set the channel for the SSHHandler

        print("SSH channel opened.")

        # Send initial MUD messages

        res = "ko"
        while res == "ko":
            res = common.main_menu(ssh_handler)
            if res == 0:
                res = self.handle_user_input(ssh_handler, ssh_handler.read_data("clear"))
        if res == "Signed In":
            self.active_queue.put(ssh_handler)

    def settings(self, ssh_handler, user_input):
        return "ok"

    def sign_in(self, ssh_handler, user_input):
        username = ""
        passwd = ""
        user_ok = False
        ssh_handler.channel.send("Enter your username:")
        username = ssh_handler.read_data("clear")
        ssh_handler.channel.send("Enter your password:")
        # You can continue the authentication process
        passwd = ssh_handler.read_data("hash")
        with open("credentials.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                stored_email, charname, stored_pwd = line.split(":")
                if username.decode("utf-8") == stored_email:
                    user_ok = True
                    stored_pwd = stored_pwd.replace("\n", "")
                    break
            f.close()
            if user_ok and stored_pwd == passwd:
                ssh_handler.send_message("Login Successful!")
                return "Signed In"
            else:
                ssh_handler.send_message("Login Not Found!")
                return "ko"

    def sign_up(self, ssh_handler, user_input):
        user_ok = True
        email_ok = True
        ssh_handler.send_message("Rules for a valid username :")
        ssh_handler.send_message("   - Minimum 3, maximum 16 characters.")
        ssh_handler.send_message("   - Cannot start with a number.")
        ssh_handler.send_message("   - Alpanumeric characters allowed.")
        ssh_handler.send_message("   - Only UNDERSCORE \"_\" allowed as a special character.")
        ssh_handler.send_message("Enter your desired username :")
        username = ssh_handler.read_data("clear").decode('utf-8', errors='ignore')

        while not self.is_valid_username(username):
            ssh_handler.send_message("Username Not Valid. Enter your desired username:")
            username = ssh_handler.read_data("clear").decode('utf-8', errors='ignore')

        ssh_handler.send_message("Enter your email (mandatory for password recovery, we DO NOT spam.):")
        email = ssh_handler.read_data("clear")

        ssh_handler.send_message("Rules for a valid password :")
        ssh_handler.send_message("   - Minimum 8, maximum 16 characters.")
        ssh_handler.send_message("   - Alpanumeric characters allowed.")
        ssh_handler.send_message("   - /,.-?_* are the only allowed special characters.")
        ssh_handler.send_message("Enter your password :")
        pass1 = ssh_handler.read_data("cypher")
        ssh_handler.send_message("Confirm your password :")
        pass2 = ssh_handler.read_data("cypher")

        res = self.is_valid_password(pass1, pass2, ssh_handler)
        while res != "ok":
            ssh_handler.send_message(res)
            pass1 = ssh_handler.read_data("cypher")
            ssh_handler.send_message("Confirm your password :")
            pass2 = ssh_handler.read_data("cypher")
            res = self.is_valid_password(pass1, pass2, ssh_handler)

        with open("credentials.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                stored_email, stored_username, stored_pwd = line.split(":")
                if not (email_ok and user_ok):
                    f.close()
                    return "ko"
                if email.decode("utf-8") == stored_email:
                    email_ok = False
                    ssh_handler.send_message("Email already registered.")
                    break
                if username == stored_username:
                    ssh_handler.send_message("Username already registered.")
                    user_ok = False
                    break
            f.close()

        if user_ok and email_ok:
            with open("credentials.txt", "a") as f:
                f.write(email.decode("utf-8") + ":")
                f.write(username + ":")
                f.write(hashlib.sha256(
                    ssh_handler.decrypt_aes(ssh_handler.read_key(), pass1).encode("utf-8")).hexdigest() + "\n")
                f.close()
                ssh_handler.send_message("Registration Successful!")
                return "Signed Up"
        else:
            return "ko"

    def handle_user_input(self, ssh_handler, user_input_str):
        # Implement logic based on user input
        username = ""
        passwd = ""
        user_ok = False
        user_input = user_input_str.decode('utf-8')

        if user_input.lower() == "sign in" or user_input.lower() == "1":
            res = self.sign_in(ssh_handler, user_input)
            return res

        elif user_input.lower() == "sign up" or user_input.lower() == "2":
            res = self.sign_up(ssh_handler, user_input)
            return "ko"


        elif user_input.lower() == "settings" or user_input.lower() == "3":
            res = self.settings(ssh_handler, user_input)
            return "ko"

        elif user_input.lower() == "exit" or user_input.lower() == "4":
            ssh_handler.send_message("Goodbye!")
            ssh_handler.channel.close()
            return "ok"
        else:
            ssh_handler.send_message("Invalid choice. Please choose again.")
            return "ko"
