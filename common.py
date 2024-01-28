from SSH_Handler import SSHHandler


def main_menu(ssh_handler):
    ssh_handler.send_message("")
    ssh_handler.send_message("Welcome to the MUD!")
    ssh_handler.send_message("What do you want to do?")
    ssh_handler.send_message("1. Sign In")
    ssh_handler.send_message("2. Sign Up")
    ssh_handler.send_message("3. Settings")
    ssh_handler.send_message("4. Exit")
    return 0


def help_menu(ssh_handler):
    ssh_handler.send_message("")
    ssh_handler.send_message("Help needed!!!")
    ssh_handler.send_message("Here a list of commands that you can used during the game")
    ssh_handler.send_message(
        "look - with no parameters it will observe the room. With a parameter is will provide information about an object, enemy or character in the same room or in the inventory.")
    ssh_handler.send_message("2. Sign Up")
    ssh_handler.send_message("3. Settings")
    ssh_handler.send_message("4. Exit")
    return 0
