class Constants:

    HEALTH_START_STAT: int = 100
    MANA_START_STAT: int = 100
    ATTACK_START_STAT: int = 50
    DEFENSE_START_STAT: int = 50

    HEALTH_PER_LEVEL: int = 10
    MANA_PER_LEVEL: int = 10
    ATTACK_PER_LEVEL: int = 5
    DEFENSE_PER_LEVEL: int = 5

    MAX_CAPACITY_OF_BACKPACK: int = 10

    PERCENTAGE_PER_HIT: float = 0.3
    PERCENTAGE_DEFENSE_ABSORPTION: float = 0.2

    XP_PER_KILL_MINION: int = 10
    MINION_MAX_LEVEL = 3
    MINION_SYMBOL: str = "M"
    HERO_START_LEVEL: int = 1
    XP_PER_LEVEL: int = 15

    MAP_WIDTH: int = 20
    MAP_HEIGHT: int = 5
    MAP_FILE_NAME: str = "map.txt"
    TREASURES_FILE_NAME = "TreasureItems.csv"

    TREASURE_LINE_SPLITTER: str = ";"
    TYPE_INDEX: int = 0
    NAME_INDEX: int = 1
    POINTS_INDEX: int = 2
    LEVEL_INDEX: int = 3
    MIN_MANA_INDEX: int = 4

    HOST = '127.0.0.1'
    PORT = 6968
    BUFFER_SIZE = 1024

    YOU_DIED: str = "You died"
    GOODBYE: str = "Goodbye\n"
