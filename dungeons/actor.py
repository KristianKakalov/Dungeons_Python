from stats import Stats
from constants import Constants
from messages import Messages
from backpack import Backpack
from treasure import Weapon, Spell, Potion, Treasure, TreasureType


class BaseActor:

    _level: int
    actor_symbol: str
    _alive: bool
    _stats: Stats
    _experience : int

    def __init__(self, actor_symbol: str, coordinates) -> None:
        self.actor_symbol = actor_symbol
        self.coordinates = coordinates
        self._alive = True
        self._stats = Stats()
        self._experience = 0

    def take_damage(self, damage: int) -> None:
        absorbed_damage: int = (int)(
            damage * Constants.PERCENTAGE_DEFENSE_ABSORPTION)
        current_deffense: int = getattr(self._stats, "_defense")
        current_health: int = getattr(self._stats, "_health")
        if absorbed_damage > current_deffense:
            absorbed_damage = current_deffense
        damage_taken: int = damage - absorbed_damage
        setattr(self._stats, "_health", current_health - damage_taken)
        setattr(self._stats, "_defense", current_deffense - absorbed_damage)
        if getattr(self._stats, "_health") <= 0:
            self._alive = False
            setattr(self._stats, "_health", 0)

    def is_alive(self) -> bool:
        return self._alive


class Minion(BaseActor):
    def __init__(self, level: int, coordinates) -> None:
        super().__init__(Constants.MINION_SYMBOL, coordinates)
        self._level = level
        self._set_stats_for_level()

    def _set_stats_for_level(self) -> None:
        if self._level == 1:
            return
        setattr(self._stats, "_health", getattr(self._stats, "_health") +
                (self._level * Constants.XP_PER_KILL_MINION))
        setattr(self._stats, "_mana", int(getattr(self._stats, "_mana") +
                                          (self._level * Constants.XP_PER_KILL_MINION)))
        setattr(self._stats, "_attack", int(getattr(self._stats, "_attack") +
                                            (self._level * Constants.XP_PER_KILL_MINION)))
        setattr(self._stats, "_defense", int(getattr(self._stats, "_defense") +
                                             (self._level * Constants.XP_PER_KILL_MINION)))

    def give_xp(self) -> int:
        return self._level * Constants.XP_PER_KILL_MINION

    def attack(self) -> int:
        attack_stat = getattr(self._stats, "_attack")
        return int(attack_stat * Constants.PERCENTAGE_PER_HIT)

    def __str__(self) -> str:
        return "Minion " + "level= " + str(self._level)


class Hero(BaseActor):

    _experience: int
    _weapon: Weapon
    _spell: Spell
    _backpack: Backpack

    def __init__(self, actor_symbol: str, coordinates) -> None:
        super().__init__(actor_symbol, coordinates)
        self._backpack = Backpack()
        self._level = Constants.HERO_START_LEVEL
        self._weapon = None
        self._spell = None

    def increase_xp(self, xp: int) -> None:
        self._experience += xp
        if self._experience >= Constants.XP_PER_LEVEL:
            self._experience %= Constants.XP_PER_LEVEL
            self._level += 1
            self._stats.increase_level()

    def attack(self) -> int:
        weapon_dmg: int = 0 if self._weapon is None else getattr(
            self._weapon, "_points")
        spell_dmg: int = 0
        if self._spell is not None and self._spell._min_mana <= self._stats._mana:
            spell_dmg = self._spell._points
            setattr(self._stats, "_mana", int(getattr(self._stats, "_mana") -
                                              getattr(self._spell, "_min_mana")))
            if int(getattr(self._stats, "_mana")) < 0:
                setattr(self._stats, "_mana", 0)
        return ((getattr(self._stats, "_attack") * Constants.PERCENTAGE_PER_HIT) +
                weapon_dmg + spell_dmg)

    def equip_weapon(self, weapon: Weapon) -> None:
        self._backpack.remove_item(weapon)
        if self._weapon is not None:
            self._backpack.add_item(self._weapon)
        self._weapon = weapon

    def learn_spell(self, spell: Spell) -> None:
        self._backpack.remove_item(spell)
        if self._spell is not None:
            self._backpack.add_item(self._weapon)
        self._spell = spell

    def drink_potion(self, potion: Potion) -> str:
        self._backpack.remove_item(potion)
        if getattr(potion, "_treasure_type") == TreasureType.HEALTH_POTION:
            self._stats._health = self._stats._health + potion._points
            return Messages.HEALTH_INCREASE_MESSAGE.format(health_stat=potion._points)
        else:
            self._stats._mana = self._stats._mana + potion._points
            return Messages.MANA_INCREASE_MESSAGE.format(mana_stat=potion._points)

    def add_to_backpack(self, item: Treasure):
        return self._backpack.add_item(item)

    def get_from_backpack(self, index: int) -> Treasure:
        return self._backpack.get_item(index)

    def remove_from_backpack(self, index: int) -> str:
        return self._backpack.remove_item(self.get_from_backpack(index))

    def is_backpack_full(self) -> bool:
        return self._backpack.is_backpack_full()

    def display_backpack(self) -> str:
        return self._backpack.__str__()

    def display_stats(self) -> str:
        return ("Level= " + str(self._level) +
                ", Weapon= " + str(self._weapon) +
                ", Spell= " + str(self._spell) + ", " +
                self._stats.__str__())

    def __str__(self) -> str:
        return "Hero " + self.actor_symbol + ", " + self.display_stats()
