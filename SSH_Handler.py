import paramiko
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from base64 import b64encode, b64decode
import hashlib



class SSHHandler(paramiko.ServerInterface):
    def __init__(self, channel):
        self.channel = channel
        self.username = None

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        return True

    def check_auth_password(self, username, password):
        return paramiko.AUTH_SUCCESSFUL

    def send_message(self, message):
        self.channel.send(f"{message}\r\n")

    def pad_data(self, data):
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        return padder.update(data) + padder.finalize()

    def unpad_data(self, data):
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        return unpadder.update(data) + unpadder.finalize()

    def encrypt_aes(self, key, plaintext):
        key = key.ljust(32, '0')  # Pad or truncate the key to 32 bytes (256 bits)
        cipher = Cipher(algorithms.AES(key.encode('utf-8')), modes.ECB())
        encryptor = cipher.encryptor()
        padded_data = self.pad_data(plaintext)
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return b64encode(ciphertext).decode('utf-8')

    def decrypt_aes(self, key, ciphertext):
        key = key.ljust(32, '0')  # Pad or truncate the key to 32 bytes (256 bits)
        cipher = Cipher(algorithms.AES(key.encode('utf-8')), modes.ECB())
        decryptor = cipher.decryptor()
        ciphertext = b64decode(ciphertext)
        decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
        return self.unpad_data(decrypted_data).decode('utf-8')

    def read_key(self):
        with open("deskey", "r") as f:
            lines = f.readlines()
            for line in lines:
                f.close()
                return line

    def read_data(self, text):
        user_input = bytearray()
        self.channel.settimeout(100)
        cursor_position = 0
        while True:

            try:
                # Receive user input
                data = self.channel.recv(1)
                if not data:
                    print(f"no data")
                elif ord(data) == 127:  # Backspace key
                    # Handle backspace
                    if user_input:
                        # Remove the last character
                        user_input.pop(cursor_position - 1)
                        cursor_position -= 1
                        # Send backspace to update the displayed text
                        self.channel.send(b'\x08 \x08')

                elif data == b'\x1b':  # Escape key (arrow key sequence)
                    escape_sequence = self.channel.recv(2)

                    if escape_sequence == b'[D' and cursor_position > 0:  # Left arrow

                        cursor_position -= 1
                        # Move the cursor left
                        self.channel.send(b'\x1b[D')
                    elif escape_sequence == b'[C' and cursor_position < len(user_input.decode('utf-8', errors='ignore')):  # Right arrow
                        cursor_position += 1
                        # Move the cursor right
                        self.channel.send(b'\x1b[C')

                elif ord(data) == 32:
                    if cursor_position < len(user_input.decode('utf-8', errors='ignore')):
                        user_input.insert(cursor_position, ord(" "))
                        self.channel.send(user_input[cursor_position:])
                        self.channel.send(b'\x1b[D' * (len(user_input) - cursor_position -1))
                        cursor_position += 1

                elif data == b'\r':
                    # Handle user input
                    self.send_message("")
                    appended_message = user_input
                    user_input = bytearray()
                    cursor_position = 0
                    user_input.clear()
                    if text == "clear":
                        return appended_message
                    elif text == "hash":
                        return hashlib.sha256(appended_message).hexdigest()
                    else:
                        tmp = self.encrypt_aes(self.read_key(), appended_message)
                        return tmp


                else:
                    user_input.insert(cursor_position, data[0])
                    cursor_position += 1
                    if text == "clear":
                        self.channel.send(data)  # Echo the character

                    else:
                        # Replace the typed character with 'X'
                        self.channel.send(b'X')
                        # Update the displayed text after the cursor

            except EOFError:
                print("Connection closed by the client.")
            except Exception as e:
                print(f"Error reading data: {e}")