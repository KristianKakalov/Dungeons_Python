class Messages:

    # treasure messages
    WEAPON_EQUIPPED_SUCCESSFULLY: str = "{weapon} equpped"
    SPELL_LEARNT_SUCCESSFULLY: str = "{spell} spell leant"
    LEVEL_NOT_ENOUGH: str = "Minimum level to use {treasure} is {level}"
    HEALTH_INCREASE_MESSAGE: str = "+{health_stat} health"
    MANA_INCREASE_MESSAGE: str = "+{mana_stat} mana"
    POTION_NOT_VALID: str = "Potion not correct type"
    # backpack messages
    BACKPACK_FULL: str = "Backpack is full"
    BACKPACK_EMPTY: str = "Backpack is empty"
    BACKPACK_ITEM_REMOVED: str = "{treasure_name} removed"
    BACKPACK_ITEM_ADDED: str = "{treasure_name} added"
    ITEM_NOT_FOUND_IN_BACKPACK: str = "No item at that index"
    # game tactics messages
    INVALID_MOVE: str = "Inavalid move"
    SUCCESSFUL_MOVE: str = "Player moved"
    MINION_KILLED: str = "Minion killed +{xp}XP"
    PLAYER_KILLED: str = "You died from {0}"
    PLAYER_KILLED_OTHER_PLAYER: str = "You killed {killed}"
    OPPONENT_BACKPACK_FULL: str = "Other player's backpack is full"
    ITEM_SWAPPED: str = "{item} swapped"
    NOT_ON_SAME_SPOT: str = "Not on same coordinates"
    INVALID_ARGUMENT: str = "Invalid argument"
    UNKNOWN_COMMAND: str = "Unknown command"
