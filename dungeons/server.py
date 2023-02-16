import socket
import threading

from constants import Constants
from client_hanler import ClientHandler
from game_tactics import GameTactics


def run_server(game):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((Constants.HOST, Constants.PORT))
        s.listen()
        print(f"Server is listening on {Constants.HOST}:{Constants.PORT}")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            client_handler = ClientHandler(conn, game)
            threading.Thread(target=client_handler.handle_client).start()


if __name__ == '__main__':
    game: GameTactics = GameTactics()
    run_server(game)
