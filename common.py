from Room import Room


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
    ssh_handler.send_message("attack object/character  - Attack with your primary weapon.")
    ssh_handler.send_message("cast spell_name object/character  - Cast a spell towards an object or character.")
    ssh_handler.send_message("pick/release object - Pick/release an object in/from your inventory.")
    ssh_handler.send_message("use object  other_object/character - Perform an action with an object.")
    ssh_handler.send_message("look -  To observe the room."
                             "look object/room/character - Will provide information about an object, room or character.")
    ssh_handler.send_message("inventory - Will show the list of items you have in your inventory.")
    ssh_handler.send_message("inventory look - As standard look but for items you have in your inventory.")
    ssh_handler.send_message("go north/south/east/west/room name - To go in a specific direction.")
    ssh_handler.send_message(
        "exit - You need to be in a safe place to exit. It will save your progress and quit the game.")
    return 0


def load_rooms(rooms_file):
    rooms = {}
    with open(rooms_file, "r") as f:
        lines = f.readlines()
    for line in lines:
        name, desc, links, items = line.split("|")
        links = links.split("-->")
        rooms[name] = Room(name, desc)
        for i in links:
            a, b = i.split(":")
            rooms[name].add_link(a, b)
    return rooms
