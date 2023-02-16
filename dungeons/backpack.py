from constants import Constants
from messages import Messages
from treasure import Treasure


class Backpack:

    _backpack: list

    def __init__(self) -> None:
        self._backpack = []

    def add_item(self, item: Treasure) -> str:
        if len(self._backpack) < Constants.MAX_CAPACITY_OF_BACKPACK:
            self._backpack.append(item)
            return Messages.BACKPACK_ITEM_ADDED.format(treasure_name=getattr(item, "_name"))
        return Messages.BACKPACK_FULL

    def remove_item(self, item: Treasure) -> str:
        if item not in self._backpack:
            return ""
        self._backpack.remove(item)
        return Messages.BACKPACK_ITEM_REMOVED.format(treasure_name=getattr(item, "_name"))

    def get_item(self, index: int) -> Treasure:
        return self._backpack[index]

    def is_backpack_full(self) -> bool:
        return len(self._backpack) == Constants.MAX_CAPACITY_OF_BACKPACK

    def __str__(self) -> str:
        result: str = ""
        if len(self._backpack) == 0:
            return Messages.BACKPACK_EMPTY + "\n"
        for count, item in enumerate(self._backpack):
            result += str(count) + ". " + str(item) + "\n"
        return result
