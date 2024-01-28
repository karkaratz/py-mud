import paramiko
import threading
import queue
import time
import common


class GameThread(threading.Thread):
    def __init__(self, game_queue, selector_update_queue):
        super(GameThread, self).__init__()
        self.game_queue = game_queue
        self.selector_update_queue = selector_update_queue

    def run(self):
        while True:
            try:
                # Get an SSH handler from the active queue
                tmp = self.game_queue.get()
                player = tmp[0]
                ssh_handler = tmp[1]
            except queue.Empty:
                # No active sessions, sleep for a while
                time.sleep(1)
                continue

            self.handle_active_session(ssh_handler, player)

    def handle_active_session(self, ssh_handler, player):
        # Check if there is data available to read from the channel
        if ssh_handler.channel.recv_ready():
            # Read the data from the channel using read_data method
            # player.current_command += self.handle_user_input(ssh_handler, ssh_handler.read_data_single("clear", player.current_command))

            result = ssh_handler.read_data_single("clear", player.current_command, player.cursor_position)
            print(result[0].decode("utf-8")[len(result[0])-1])
            if result[0].decode("utf-8")[len(result[0])-1]!="\r":
                player.set_command(result[0])
                player.set_cursor(result[1])
            else :
                player.set_command("".encode("utf-8"))
                player.set_cursor(0)
                self.handle_user_input(ssh_handler, result[0].decode("utf-8")[:len(result[0])-1])
            self.selector_update_queue.put((player, ssh_handler))

    def handle_user_input(self, ssh_handler, user_input_str):
        # Implement logic based on user input
        username = ""
        passwd = ""
        user_ok = False
        user_input = user_input_str

        if user_input.lower() == "help" or user_input.lower() == "1":
            res = common.help_menu(ssh_handler)
            return "portanna"

        if user_input.lower() == "settings" or user_input.lower() == "3":
            res = self.settings(ssh_handler, user_input)
            return "portanna"

        elif user_input.lower() == "exit" or user_input.lower() == "4":
            ssh_handler.send_message("Goodbye!")
            ssh_handler.channel.close()
            return "ok"
        else:
            ssh_handler.send_message(user_input_str)
            ssh_handler.send_message("Invalid choice. Please choose again.")
            return "ko"
