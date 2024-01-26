import socket
from IncomingThread import IncomingThread
import queue




port = 2222
def main():
    # Create queues for managing connection states
    incoming_queue = queue.Queue()
    active_queue = queue.Queue()
    settings_queue = queue.Queue()
    pause_queue = queue.Queue()

    # Create an array of IncomingThread instances
    num_threads = 3  # You can adjust this based on your requirements
    incoming_threads = [IncomingThread(incoming_queue) for _ in range(num_threads)]

    # Start the IncomingThreads
    for thread in incoming_threads:
        thread.start()

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
