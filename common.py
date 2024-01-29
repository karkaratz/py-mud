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
    ssh_handler.send_message("--------------Help needed!!!----------------")
    ssh_handler.send_message("Here a list of commands that you can used during the game.")
    ssh_handler.send_message(
        "look -  To observe the room. "
        "look object/enemy/character - Will provide information about an object, enemy or character.")
    ssh_handler.send_message("inventory - Will show the list of items you have in your inventory.")
    ssh_handler.send_message("go north/south/east/west - To go in a specific direction.")
    ssh_handler.send_message("exit - You need to be in a safe place to exit. It will save your progress and quit the game.")
    return 0
