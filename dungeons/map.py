import random

from enum import Enum
from constants import Constants
from actor import Minion
from treasure import TreasureInitializer, Treasure


class Coordinates:

    x: int
    y: int

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def generate_random_coordinates(x_boundary, y_boundary):
        x: int = random.randint(0, x_boundary)
        y: int = random.randint(0, y_boundary)
        return Coordinates(x, y)

    def __eq__(self, other) -> bool:
        if isinstance(other, Coordinates):
            return self.x == other.x and self.y == other.y
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.x, self.y))


class MapSymbols(Enum):
    OBSTACLE = "#"
    TREASURE = "T"
    FREE_SPOT = "."
    MINION = "M"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def is_valid_map_symbol(symbol: str) -> bool:
        return symbol in MapSymbols._value2member_map_


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    @staticmethod
    def coordinates_after_movement(coordinates: Coordinates, direction) -> Coordinates:
        match direction:
            case Direction.UP:
                return Coordinates(coordinates.x - 1, coordinates.y)
            case Direction.DOWN:
                return Coordinates(coordinates.x + 1, coordinates.y)
            case Direction.LEFT:
                return Coordinates(coordinates.x, coordinates.y - 1)
            case Direction.RIGHT:
                return Coordinates(coordinates.x, coordinates.y + 1)


class NotEnoughTreasuresException(Exception):
    pass


class InvalidMapCoordinatesException(Exception):
    pass


class Map:

    _map: list
    _objects: dict

    def __init__(self) -> None:
        self._map = []
        self._objects = {}
        self._initialize_map()
        self._save_objects()

    def _initialize_map(self) -> None:
        with open(Constants.MAP_FILE_NAME) as f:
            for line in f:
                row: list = []
                for char in line.strip():
                    row.append(char)
                self._map.append(row)

    def __str__(self) -> str:
        result: str = ""
        for row_index, row in enumerate(self._map):
            for col_index, col in enumerate(row):
                result += str(self._map[row_index][col_index])
            result += "\n"
        return result

    def _save_objects(self) -> None:
        minion_coordinates: set = set()
        treasures_coordinates: set = set()
        for row, line in enumerate(self._map):
            for col, symbol in enumerate(line):
                if str(symbol) == MapSymbols.MINION.value:
                    minion_coordinates.add(Coordinates(row, col))
                if str(symbol) == MapSymbols.TREASURE.value:
                    treasures_coordinates.add(Coordinates(row, col))
        self._initialize_mionions(minion_coordinates)
        self._initialize_treasures(treasures_coordinates)

    def _initialize_mionions(self, minion_coordinates: set) -> None:
        for level, coordinate in enumerate(minion_coordinates):
            minion: Minion = Minion(
                level % Constants.MINION_MAX_LEVEL + 1, coordinate)
            self._objects[coordinate] = minion

    def _initialize_treasures(self, treasure_coordinates: set) -> None:
        num_of_treasures_in_file: int = self._total_num_of_items_in_file()
        if num_of_treasures_in_file < len(treasure_coordinates):
            raise NotEnoughTreasuresException(
                "Not enough treasures in {file_name} to generate in map", Constants.TREASURES_FILE_NAME)
        with open(Constants.TREASURES_FILE_NAME) as f:
            next(f)
            lines = f.readlines()
            random.shuffle(lines)
            for line, coordinate in zip(lines, treasure_coordinates):
                treasure: Treasure = TreasureInitializer.Factory(line.strip())
                treasure.coordinates = coordinate
                self._objects[coordinate] = treasure

    def _total_num_of_items_in_file(self) -> int:
        with open(Constants.TREASURES_FILE_NAME) as f:
            return len(f.readlines()) - 1

    def _validate_coordinates(self, coordinates: Coordinates) -> bool:
        x: int = coordinates.x
        y: int = coordinates.y
        return x >= 0 and y >= 0 and x < Constants.MAP_HEIGHT and y < Constants.MAP_WIDTH

    def _is_coorinate_empty(self, coordinates: Coordinates) -> bool:
        x: int = coordinates.x
        y: int = coordinates.y
        return (self._validate_coordinates(coordinates) and
                self._map[x][y] != MapSymbols.MINION.value and
                self._map[x][y] != MapSymbols.TREASURE.value and
                self._map[x][y] != MapSymbols.OBSTACLE.value)

    def get_symbol(self, coordinates: Coordinates) -> str:
        x: int = coordinates.x
        y: int = coordinates.y
        if self._validate_coordinates(coordinates):
            return self._map[x][y]
        else:
            raise InvalidMapCoordinatesException(
                "Coordinates out of map bounds")

    def change_symbol(self, coordinates: Coordinates, symbol: str) -> None:
        x: int = coordinates.x
        y: int = coordinates.y
        if self._validate_coordinates(coordinates):
            self._map[x][y] = symbol

    def get_object(self, coordinates: Coordinates):
        return self._objects[coordinates]

    def add_object_to_map(self, coordinates: Coordinates, object) -> None:
        self._objects[coordinates] = object

    def remove_object(self, coordinates: Coordinates) -> None:
        del self._objects[coordinates]

    def get_free_coordinates(self) -> Coordinates:
        while True:
            coordinates: Coordinates = Coordinates.generate_random_coordinates(
                Constants.MAP_HEIGHT - 1, Constants.MAP_WIDTH - 1)
            if self.get_symbol(coordinates) == MapSymbols.FREE_SPOT.value:
                return coordinates
