from constants import Constants


class Stats:

    _health: int
    _mana: int
    _attack: int
    _defense: int

    def __init__(self, health: int = Constants.HEALTH_START_STAT, mana: int = Constants.MANA_START_STAT,
                 attack: int = Constants.ATTACK_START_STAT, defense: int = Constants.DEFENSE_START_STAT) -> None:
        self._health = health
        self._mana = mana
        self._attack = attack
        self._defense = defense

    def _increase_stats(self, health_increase: int, mana_increase: int, attack_increase: int, defense_increase: int) -> None:
        self._health += health_increase
        self._mana += mana_increase
        self._attack += attack_increase
        self._defense += defense_increase

    def increase_level(self) -> None:
        self._increase_stats(Constants.HEALTH_PER_LEVEL, Constants.MANA_PER_LEVEL,
                             Constants.ATTACK_PER_LEVEL, Constants.DEFENSE_PER_LEVEL)

    def __str__(self) -> str:
        return ("Stats: health=" + str(self._health) + ", mana=" +
                str(self._mana) + ", attack=" + str(self._attack)
                + ", defense=" + str(self._defense))
