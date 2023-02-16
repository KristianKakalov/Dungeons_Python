import socket
import threading

from constants import Constants


def receive_data(s):
    try:
        while True:
            msg = s.recv(Constants.BUFFER_SIZE)
            print(msg.decode())
            if Constants.YOU_DIED in msg.decode():
                print("Press any key to exit...")
                break
            if msg.decode() == Constants.GOODBYE:
                break
    except:
        print("Connection lost! Press any key to exit...")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((Constants.HOST, Constants.PORT))
        thread = threading.Thread(target=receive_data, args=(s,))
        thread.start()
        while True:
            client_input = input()
            if thread.is_alive():
                s.sendall(client_input.encode())
            if client_input.lower() == "quit":
                break
    except:
        print("Connection lost!")
    thread.join()
