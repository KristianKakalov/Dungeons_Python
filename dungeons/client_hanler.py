from enum import Enum
from constants import Constants
from game_tactics import GameTactics, Hero, Coordinates, Messages, Direction


class CommandType(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    BACKPACK = "backpack"
    STATS = "stats"
    USE = "use"
    REMOVE = "remove"
    SWAP = "swap"
    FIGHT = "fight"
    QUIT = "quit"
    UNKNOWN = "unknown"


class Command:

    commandType: CommandType
    argument: str

    def __init__(self, line: str) -> None:
        if not line:
            self.commandType = CommandType.UNKNOWN
            self.argument = ""
        tokens: list = line.strip().split(" ", 2)
        if len(tokens) < 1:
            self.commandType = CommandType.UNKNOWN
            self.argument = ""
        self.argument = tokens[1] if len(tokens) == 2 else ""
        self.commandType = (CommandType[tokens[0].upper()]
                            if tokens[0].upper() in CommandType.__members__
                            else CommandType.UNKNOWN)


class ClientHandler:

    CLIENTS: dict = {}
    CLIENT_SYMBOLS: list = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, connection, game: GameTactics) -> None:
        self.connection = connection
        self._game = game
        self._spawn_player()

    def _spawn_player(self) -> None:
        ClientHandler.CLIENT_SYMBOLS.sort()
        symbol = ClientHandler.CLIENT_SYMBOLS[0]
        ClientHandler.CLIENT_SYMBOLS.remove(symbol)
        coordinates: Coordinates = self._game.get_random_free_coordinates()
        self.player: Hero = Hero(str(symbol), coordinates)
        self._game.spawn_hero(self.player)
        ClientHandler.CLIENTS[self.connection] = self.player
        self.connection.send(
            ("Welcome to Dungeons! Your player " +
             f"symbol is {self.player.actor_symbol}\n").encode())
        self._send_updated_map()

    def handle_client(self) -> None:
        while True and self.player.is_alive():
            client_input: str = self.connection.recv(
                Constants.BUFFER_SIZE).decode()

            command: Command = Command(client_input)
            print(
                f"player{self.player.actor_symbol};cmd:{command.commandType}-{command.argument}")

            match command.commandType:
                case (CommandType.LEFT |
                      CommandType.RIGHT |
                      CommandType.UP |
                      CommandType.DOWN):
                    self._move_player(command.commandType.name)
                case CommandType.QUIT:
                    self._disconnect_player(self.connection)
                    break
                case CommandType.BACKPACK:
                    self._display_backpack()
                case CommandType.STATS:
                    self._display_stats()
                case CommandType.USE:
                    self._use_item(command.argument)
                case CommandType.REMOVE:
                    self._remove_item(command.argument)
                case CommandType.SWAP | CommandType.FIGHT:
                    self._interact_with_other_player(command)
                case CommandType.UNKNOWN:
                    self._send_msg(Messages.UNKNOWN_COMMAND)

    def _move_player(self, direction) -> None:
        direction: Direction = Direction[direction]
        game_msg: str = self._game.move_hero(self.player, direction)
        if game_msg != Messages.INVALID_MOVE and self.player.is_alive():
            self._send_updated_map()
        if not self.player.is_alive():
            self._disconnect_player(self.connection, game_msg)
        else:
            self._send_msg(game_msg)

    def _send_updated_map(self) -> None:
        for client in ClientHandler.CLIENTS.keys():
            client.send(self._game.display_map().encode())

    def _disconnect_player(self, conn, msg="Goodbye") -> None:
        player: Hero = ClientHandler.CLIENTS[conn]
        symbol = player.actor_symbol
        ClientHandler.CLIENT_SYMBOLS.append(int(symbol))
        ClientHandler.CLIENTS.pop(conn)
        conn.send((msg + "\n").encode())
        self._game._remove_hero_from_map(player)
        self._send_updated_map()

    def _display_backpack(self) -> None:
        game_msg: str = self.player.display_backpack()
        self._send_msg(game_msg)

    def _display_stats(self) -> None:
        game_msg: str = self.player.display_stats()
        self._send_msg(game_msg)

    def _use_item(self, index: str) -> None:
        try:
            game_msg: str = self._game.hero_use_item_from_backpack(
                self.player, int(index))
            self._send_msg(game_msg)
        except ValueError:
            self._send_msg(Messages.INVALID_ARGUMENT)

    def _remove_item(self, index: str) -> None:
        try:
            game_msg: str = self._game.hero_remove_item_from_backpack(
                self.player, int(index))
            self._send_msg(game_msg)
        except ValueError:
            self._send_msg(Messages.INVALID_ARGUMENT)

    def _interact_with_other_player(self, command: Command) -> None:
        other_player_symbol: str = self._game.get_other_player_symbol(
            self.player)
        if other_player_symbol == Messages.NOT_ON_SAME_SPOT:
            self._send_msg(Messages.NOT_ON_SAME_SPOT)
        other_player_conn = [
            i for i in ClientHandler.CLIENTS
            if ClientHandler.CLIENTS[i].actor_symbol == other_player_symbol][0]
        if command.commandType == CommandType.SWAP:
            self._swap_item_with_player(other_player_conn, command.argument)
        else:
            self._fight_with_player(other_player_conn)

    def _swap_item_with_player(self, other_player_conn, index: str) -> None:
        try:
            other_player: Hero = ClientHandler.CLIENTS[other_player_conn]
            game_msg: str = self._game.swap_item(
                self.player, other_player, int(index))
            if "swapped" in game_msg:
                other_player_conn.send((game_msg + "\n").encode())
                self._send_msg(game_msg)
        except ValueError:
            self._send_msg(Messages.INVALID_ARGUMENT)

    def _fight_with_player(self, other_player_conn) -> None:
        other_player: Hero = ClientHandler.CLIENTS[other_player_conn]
        game_msg: str = self._game.heroes_fight(self.player, other_player)
        if "died" in game_msg:
            self._disconnect_player(self.connection, game_msg)
            other_player_conn.send(
                (Messages.PLAYER_KILLED_OTHER_PLAYER.format(str(self.player)) + "\n").encode())
        else:
            self._disconnect_player(other_player_conn,
                                    Messages.PLAYER_KILLED.format(
                                        str(self.player)))
            self._send_msg(game_msg)

    def _send_msg(self, msg) -> None:
        self.connection.send((msg + "\n").encode())
