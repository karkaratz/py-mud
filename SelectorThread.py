import paramiko
import threading
import queue
import time
import common
import selectors
from Player import Player

class SelectorThread(threading.Thread):

    def __init__(self, active_queue, game_queue, selector_update_queue):
        super(SelectorThread, self).__init__()
        self.active_queue = active_queue
        self.game_queue = game_queue
        self.selector_update_queue = selector_update_queue
        self.sel = selectors.DefaultSelector()
        self.clients = {}

    def run(self):
        i = 0

        while True:

            try:
                # Get an SSH handler from the active queue
                ssh_handler = self.active_queue.get(block=False)
                self.sel.register(ssh_handler.channel, selectors.EVENT_READ, self.manage_things)
                self.clients[ssh_handler.channel] = (Player("pippo", "pluto"), ssh_handler)

            except queue.Empty:

                pass

            events = self.sel.select(timeout=0.1)
            for key, mask in events:
                key.data(key[0], self.clients[key[0]])
                #game_queue.put(clients[key.fileobjid])

            try:
                # Get an SSH handler from the active queue

                upd = self.selector_update_queue.get(block=False)
                player = upd[0]
                handler = upd[1]
                self.clients[handler]=player
            except queue.Empty:
                pass



    def manage_things(self, key, client):
        self.game_queue.put(client)
        return 0
