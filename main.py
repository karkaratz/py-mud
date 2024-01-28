import socket
from IncomingThread import IncomingThread
from GameThread import GameThread
from SelectorThread import SelectorThread
import queue

port = 2222


def main():
    # Create queues for managing game states
    incoming_queue = queue.Queue()
    active_queue = queue.Queue()
    settings_queue = queue.Queue()
    pause_queue = queue.Queue()
    game_queue = queue.Queue()
    selector_update_queue = queue.Queue()

    # Create an array of IncomingThread instances
    num_i_threads = 1  # You can adjust this based on your requirements
    incoming_threads = [IncomingThread(incoming_queue, active_queue) for _ in range(num_i_threads)]
    num_g_threads = 5  # You can adjust this based on your requirements
    game_threads = [GameThread(game_queue, selector_update_queue) for _ in range(num_g_threads)]
    selector_thread = SelectorThread(active_queue, game_queue, selector_update_queue)

    # Start the IncomingThreads
    for thread in incoming_threads:
        thread.start()

    for thread in game_threads:
        thread.start()

    selector_thread.start()

    # Create a standard socket for accepting connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(10)

    print(f"SSH server is listening on port {port}")

    while True:
        client_socket, addr = server_socket.accept()
        # Add the new connection to the incoming queue
        incoming_queue.put((client_socket, addr))


if __name__ == "__main__":
    main()
