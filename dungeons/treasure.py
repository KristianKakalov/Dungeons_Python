from enum import Enum
from messages import Messages
from constants import Constants


class TreasureType(Enum):
    WEAPON = 1
    SPELL = 2
    MANA_POTION = 3
    HEALTH_POTION = 4


class Treasure:

    _treasure_type: TreasureType
    _name: str
    _points: int

    def __init__(self, treasure_type: TreasureType, name: str, points: int, coordinates) -> None:
        self._treasure_type = treasure_type
        self._name = name
        self._points = points
        self.coordinates = coordinates

    def __str__(self) -> str:
        return str(self._treasure_type.name) + ", " + self._name + ", points=" + str(self._points)

    def use(self, hero) -> str:
        raise NotImplementedError("Subclass must implement this method")


class Weapon(Treasure):

    _level: int

    def __init__(self, name: str, points: int, level: int, coordinates) -> None:
        treasure_type: TreasureType = TreasureType.WEAPON
        super().__init__(treasure_type, name, points, coordinates)
        self._level = level

    def use(self, hero) -> str:
        if (getattr(hero, "_level") >= self._level):
            hero.equip_weapon(self)
            return Messages.WEAPON_EQUIPPED_SUCCESSFULLY.format(weapon=self._name)
        return Messages.LEVEL_NOT_ENOUGH.format(treasure=self._name, level=self._level)

    def __str__(self) -> str:
        return (str(self._treasure_type.name) + " " + self._name +
                ", Damage= " + str(self._points) + ", level= " + str(self._level))


class Spell(Treasure):

    _level: int
    _min_mana: int

    def __init__(self, name: str, points: int, level: int, min_mana: int, coordinates) -> None:
        treasure_type: TreasureType = TreasureType.SPELL
        super().__init__(treasure_type, name, points, coordinates)
        self._level = level
        self._min_mana = min_mana

    def use(self, hero) -> str:
        if (getattr(hero, "_level") >= self._level):
            hero.learn_spell(self)
            return Messages.SPELL_LEARNT_SUCCESSFULLY.format(spell=self._name)
        return Messages.LEVEL_NOT_ENOUGH.format(treasure=self._name, level=self._level)

    def __str__(self) -> str:
        return (str(self._treasure_type.name) + " " + self._name + ", Damage= "
                + str(self._points) + ", level= "
                + str(self._level) + ", min Mana= " + str(self._min_mana))


class Potion(Treasure):
    def __init__(self, name: str, points: int, coordinates, treasure_type: TreasureType) -> None:
        super().__init__(treasure_type, name, points, coordinates)

    def use(self, hero) -> str:
        return hero.drink_potion(self)


class TreasureInitializer:
    def Factory(line: str) -> Treasure:
        tokens = line.split(";")
        treasure_type = tokens[Constants.TYPE_INDEX]
        match treasure_type:
            case TreasureType.WEAPON.name:
                return Weapon(tokens[Constants.NAME_INDEX],
                              (int)(tokens[Constants.POINTS_INDEX]),
                              (int)(tokens[Constants.LEVEL_INDEX]), None)
            case TreasureType.SPELL.name:
                return Spell(tokens[Constants.NAME_INDEX],
                             (int)(tokens[Constants.POINTS_INDEX]),
                             (int)(tokens[Constants.LEVEL_INDEX]),
                             (int)(tokens[Constants.MIN_MANA_INDEX]), None)
            case TreasureType.MANA_POTION.name | TreasureType.HEALTH_POTION.name:
                return Potion((tokens[Constants.NAME_INDEX]),
                              (int)(tokens[Constants.POINTS_INDEX]),
                              None, TreasureType[treasure_type])
