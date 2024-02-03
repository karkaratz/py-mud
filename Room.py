class Room:
    def __init__(self, name, description, visible=True):
        self.name = name
        self.description = description
        self.visible = visible
        self.items = []
        self.links = {}  # Dictionary to store links to other rooms

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        self.items.remove(item)

    def add_link(self, direction, linked_room):
        self.links[direction] = linked_room

    def set_visible(self, visible):
        self.visible = visible

    def display_items(self):
        if not self.visible:
            print("This room is currently not visible.")
            return

        if not self.items:
            print("No items in this room.")
        else:
            print("Items in the room:")
            for item in self.items:
                print(f"- {item.name}: {item.description}")

    def display_links(self):
        if not self.visible:
            print("This room is currently not visible.")
        if not self.links:
            print("No Paths in this room.")
        else:
            print("{} Paths to other places:".format(self.name))
            for direction, linked_room in self.links.items():
                print(f"- {direction.capitalize()}: {linked_room}")

