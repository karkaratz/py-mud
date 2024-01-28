
class Player():


    def __init__(self, name, character_name):
        super(Player, self).__init__()
        self.name = name
        self.character_name = character_name
        self.current_command = ""
        self.cursor_position = 0

    def append_command(self, input_byte):
        self.current_command += input_byte.decode("utf-8")

    def set_command(self, input_bytes):
        self.current_command = input_bytes.decode("utf-8")

    def set_cursor(self, position):
        self.cursor_position = position
