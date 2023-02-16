from map import Map, MapSymbols, Coordinates, Direction, InvalidMapCoordinatesException
from actor import Hero, Minion, Messages, Treasure


class GameTactics:

    _map: Map

    def __init__(self) -> None:
        self._map = Map()

    def move_hero(self, hero: Hero, direction: Direction) -> str:
        hero_current_coordinates: Coordinates = hero.coordinates
        coordinates_after_movement: Coordinates = (Direction.coordinates_after_movement(
            hero_current_coordinates, direction))
        try:
            symbol_after_movement: str = self._map.get_symbol(
                coordinates_after_movement)
        except InvalidMapCoordinatesException:
            return Messages.INVALID_MOVE

        is_map_symbol: bool = MapSymbols.is_valid_map_symbol(
            symbol_after_movement)
        if is_map_symbol:
            match MapSymbols(symbol_after_movement):
                case MapSymbols.FREE_SPOT:
                    return self._move_hero_to_free_potition(hero, hero_current_coordinates, coordinates_after_movement)

                case MapSymbols.OBSTACLE:
                    return Messages.INVALID_MOVE

                case MapSymbols.TREASURE:
                    treasure: Treasure = self._map.get_object(
                        coordinates_after_movement)
                    return self._collect_treasure(hero, treasure)

                case MapSymbols.MINION:
                    minion: Minion = self._map.get_object(
                        coordinates_after_movement)
                    return self._fight_with_minion(hero, minion)
        else:
            self._change_previous_coordinates(hero, hero_current_coordinates)
            self._map.change_symbol(coordinates_after_movement, hero.actor_symbol
                                    + symbol_after_movement)
            hero.coordinates = coordinates_after_movement
            return Messages.SUCCESSFUL_MOVE
        return Messages.INVALID_MOVE

    def _move_hero_to_free_potition(self, hero: Hero,
                                    hero_current_coordinates: Coordinates,
                                    coordinates_after_movement: Coordinates) -> str:
        self._change_previous_coordinates(hero, hero_current_coordinates)
        self._map.change_symbol(coordinates_after_movement, hero.actor_symbol)
        hero.coordinates = coordinates_after_movement
        return Messages.SUCCESSFUL_MOVE

    def _change_previous_coordinates(self, hero: Hero, hero_current_coordinates: Coordinates) -> None:
        currentSymbol = self._map.get_symbol(hero_current_coordinates)
        if currentSymbol == hero.actor_symbol:
            self._map.change_symbol(
                hero_current_coordinates, MapSymbols.FREE_SPOT.value)
        else:
            self._map.change_symbol(
                hero_current_coordinates, currentSymbol.replace(hero.actor_symbol, ""))

    def _collect_treasure(self, hero: Hero, treasure: Treasure) -> str:
        self._change_previous_coordinates(hero, hero.coordinates)
        message: str = hero.add_to_backpack(treasure)
        if message == Messages.BACKPACK_FULL:
            self._map.change_symbol(
                treasure.coordinates, hero.actor_symbol + MapSymbols.TREASURE.value)
        else:
            self._map.change_symbol(treasure.coordinates, hero.actor_symbol)
            self._map.remove_object(treasure.coordinates)
        hero.coordinates = treasure.coordinates
        return message

    def _fight_with_minion(self, hero: Hero, minion: Minion) -> str:
        self._change_previous_coordinates(hero, hero.coordinates)
        hero_won: bool = False
        while True:
            minion.take_damage(hero.attack())
            if not minion.is_alive():
                hero_won = True
                break
            hero.take_damage(minion.attack())
            if not hero.is_alive():
                break
        if hero_won:
            self._map.change_symbol(minion.coordinates, hero.actor_symbol)
            hero.coordinates = minion.coordinates
            xp: int = minion.give_xp()
            hero.increase_xp(xp)
            return Messages.MINION_KILLED.format(xp=str(xp))
        return Messages.PLAYER_KILLED.format(str(minion))

    def swap_item(self, fromHero: Hero, toHero: Hero, index: int) -> str:
        if fromHero.coordinates != toHero.coordinates:
            return Messages.NOT_ON_SAME_SPOT
        if toHero.is_backpack_full():
            return Messages.OPPONENT_BACKPACK_FULL
        try:
            item: Treasure = fromHero.get_from_backpack(index)
            toHero.add_to_backpack(item)
            fromHero.remove_from_backpack(index)
            return Messages.ITEM_SWAPPED.format(item=item._name)
        except IndexError:
            return Messages.ITEM_NOT_FOUND_IN_BACKPACK

    def hero_use_item_from_backpack(self, hero: Hero, index: int) -> str:
        try:
            item: Treasure = hero.get_from_backpack(index)
            return item.use(hero)
        except IndexError:
            return Messages.ITEM_NOT_FOUND_IN_BACKPACK

    def hero_remove_item_from_backpack(self, hero: Hero, index: int) -> str:
        try:
            item: Treasure = hero.get_from_backpack(index)
            item.coordinates = hero.coordinates
            self._map.add_object_to_map(item.coordinates, item)
            self._map.change_symbol(item.coordinates,
                                    hero.actor_symbol + MapSymbols.TREASURE.value)
            return hero.remove_from_backpack(index)
        except IndexError:
            return Messages.ITEM_NOT_FOUND_IN_BACKPACK

    def heroes_fight(self, hero1: Hero, hero2: Hero) -> str:
        if hero1.coordinates != hero2.coordinates:
            return Messages.NOT_ON_SAME_SPOT
        hero1Won: bool = False
        while True:
            hero2.take_damage(hero1.attack())
            if not hero2.is_alive():
                hero1Won = True
                break
            hero1.take_damage(hero2.attack())
            if not hero1.is_alive():
                break
        if hero1Won:
            self._remove_hero_from_map(hero2)
            return Messages.PLAYER_KILLED_OTHER_PLAYER.format(killed=str(hero2))
        else:
            self._remove_hero_from_map(hero1)
            return Messages.PLAYER_KILLED.format(str(hero2))

    def _remove_hero_from_map(self, hero: Hero) -> None:
        coordinates: Coordinates = hero.coordinates
        symbol: str = self._map.get_symbol(coordinates)
        if len(symbol) == 2:
            self._map.change_symbol(
                coordinates, symbol.replace(hero.actor_symbol, ""))
        else:
            self._map.change_symbol(coordinates, MapSymbols.FREE_SPOT.value)

    def display_map(self) -> str:
        return str(self._map)

    def get_other_player_symbol(self, hero: Hero) -> str:
        symbols: str = self._map.get_symbol(hero.coordinates)
        if len(symbols) != 2:
            return Messages.NOT_ON_SAME_SPOT
        other_player_symbol = symbols.replace(hero.actor_symbol, "")
        return other_player_symbol if self._is_valid_player_symbol((int)(other_player_symbol)) else Messages.NOT_ON_SAME_SPOT

    def _is_valid_player_symbol(self, other_player_symbol: int) -> bool:
        return (int)(other_player_symbol) in range(1, 10)

    def spawn_hero(self, hero: Hero) -> None:
        self._map.change_symbol(hero.coordinates, hero.actor_symbol)

    def get_random_free_coordinates(self) -> Coordinates:
        return self._map.get_free_coordinates()
