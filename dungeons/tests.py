import unittest

from actor import Hero, Minion
from map import Coordinates, Map, MapSymbols
from constants import Constants
from messages import Messages
from game_tactics import Direction, GameTactics
from treasure import Weapon, Spell, Potion, TreasureType, TreasureInitializer, Treasure


class HeroAndTreasureTest(unittest.TestCase):

    def setUp(self) -> None:
        self.coordinates: Coordinates = Coordinates(1, 1)
        self.hero: Hero = Hero("1", self.coordinates)

    def test_increase_xp(self):
        self.hero.increase_xp(Constants.XP_PER_LEVEL)
        self.hero.take_damage(130)

        self.assertTrue(self.hero.is_alive())
        self.assertEqual(getattr(self.hero, "_level"), 2)

    def test_equip_spell_and_weapon(self):
        weapon: Weapon = Weapon("weapon", 10, 1, self.coordinates)
        spell: Spell = Spell("spell", 10, 1, 10, self.coordinates)

        weapon.use(self.hero)
        spell.use(self.hero)

        expected: int = 35
        actual: int = self.hero.attack()

        self.assertEqual(actual, expected)

    def test_equip_weapon_and_then_equip_another_weapon(self):
        weapon1: Weapon = Weapon("weapon1", 10, 1, self.coordinates)
        weapon2: Weapon = Weapon("weapon2", 10, 1, self.coordinates)

        weapon1.use(self.hero)
        weapon2.use(self.hero)

        weapon_from_backpack: Weapon = self.hero.get_from_backpack(0)

        self.assertEqual(weapon1, weapon_from_backpack)

    def test_use_spell_and_then_increase_mana(self):
        spell: Spell = Spell("spell", 50, 1, 100, self.coordinates)
        mana_potion: Potion = Potion(
            "mana_potion", 100, self.coordinates, TreasureType.MANA_POTION)
        spell.use(self.hero)

        expected_dmg: int = 65
        actual_dmg: int = self.hero.attack()
        self.assertEqual(actual_dmg, expected_dmg)

        expected_dmg_no_spell: int = 15
        actual_dmg_no_spell: int = self.hero.attack()
        self.assertEqual(actual_dmg_no_spell, expected_dmg_no_spell)

        mana_potion.use(self.hero)
        expected_dmg_after_potion: int = 65
        actual_dmg_after_potion: int = self.hero.attack()
        self.assertEqual(actual_dmg_after_potion, expected_dmg_after_potion)

    def test_drink_health_potion(self):
        health_potion: Potion = Potion(
            "health_potion", 100, self.coordinates, TreasureType.HEALTH_POTION)

        self.hero.take_damage(100)
        self.assertTrue(self.hero.is_alive())

        health_potion.use(self.hero)
        self.hero.take_damage(100)
        self.assertTrue(self.hero.is_alive())

    def test_backpack_overflow(self):
        for _ in range(10):
            weapon: Weapon = Weapon("weapon", 10, 1, self.coordinates)
            expected_msg: str = Messages.BACKPACK_ITEM_ADDED.format(
                treasure_name=weapon._name)
            actual_msg: str = self.hero.add_to_backpack(weapon)
            self.assertEqual(actual_msg, expected_msg)
        weapon: Weapon = Weapon("weapon", 10, 1, self.coordinates)
        expected_msg: str = Messages.BACKPACK_FULL
        actual_msg: str = self.hero.add_to_backpack(weapon)
        self.assertEqual(actual_msg, expected_msg)

    def test_remove_item_from_backpack(self):
        weapon1: Weapon = Weapon("weapon1", 10, 1, self.coordinates)
        weapon2: Weapon = Weapon("weapon2", 10, 1, self.coordinates)

        self.hero.add_to_backpack(weapon1)
        self.hero.add_to_backpack(weapon2)

        self.hero.remove_from_backpack(0)

        expected_backpack_content: str = "0. WEAPON weapon2, Damage= 10, level= 1\n"
        actual_backpack_content: str = self.hero.display_backpack()
        self.assertEqual(actual_backpack_content, expected_backpack_content)

    def test_hero_displayed(self):
        weapon: Weapon = Weapon("weapon", 10, 1, self.coordinates)
        spell: Spell = Spell("spell", 50, 1, 100, self.coordinates)

        weapon.use(self.hero)
        spell.use(self.hero)

        expected: str = ("Hero 1, Level= 1, Weapon= WEAPON weapon, " +
                         "Damage= 10, level= 1, Spell= SPELL spell, Damage= 50, level= 1, " +
                         "min Mana= 100, Stats: health=100, mana=100, attack=50, defense=50")
        actual: str = self.hero.__str__()

        self.assertEqual(actual, expected)

    def test_hero_when_attack_and_dies(self):
        health_potion: Potion = Potion(
            "health_potion", 1000, self.coordinates, TreasureType.HEALTH_POTION)

        health_potion.use(self.hero)
        for _ in range(5):
            self.hero.take_damage(60)
            self.assertTrue(self.hero.is_alive())
        self.hero.take_damage(1000)
        self.assertFalse(self.hero.is_alive())

    def test_equip_weapon_level_not_enough(self):
        weapon: Weapon = Weapon("weapon", 10, 2, self.coordinates)
        spell: Spell = Spell("spell", 10, 2, 10, self.coordinates)

        actual_weapon_msg: str = weapon.use(self.hero)
        expected_weapon_msg: str = Messages.LEVEL_NOT_ENOUGH.format(
            treasure=weapon._name, level=weapon._level)
        actual_spell_msg: str = spell.use(self.hero)
        expected_spell_msg: str = Messages.LEVEL_NOT_ENOUGH.format(
            treasure=spell._name, level=spell._level)

        self.assertEqual(actual_weapon_msg, expected_weapon_msg)
        self.assertEqual(actual_spell_msg, expected_spell_msg)


class TreasureInitialierTest(unittest.TestCase):

    def test_initialize_spell(self):
        line: str = "SPELL;Dark magic;25;1;20"
        spell: Spell = TreasureInitializer.Factory(line)

        expected_name: str = "Dark magic"
        expected_type: TreasureType = TreasureType.SPELL
        expected_points: int = 25
        expected_level: int = 1
        expected_min_mana: int = 20

        self.assertEqual(spell._name, expected_name)
        self.assertEqual(spell._treasure_type, expected_type)
        self.assertEqual(spell._points, expected_points)
        self.assertEqual(spell._level, expected_level)
        self.assertEqual(spell._min_mana, expected_min_mana)

    def test_initialize_potion(self):
        line: str = "HEALTH_POTION;Health potion 1;30"
        spell: Spell = TreasureInitializer.Factory(line)

        expected_name: str = "Health potion 1"
        expected_type: TreasureType = TreasureType.HEALTH_POTION
        expected_points: int = 30

        self.assertEqual(spell._name, expected_name)
        self.assertEqual(spell._treasure_type, expected_type)
        self.assertEqual(spell._points, expected_points)


class MinionTest (unittest.TestCase):

    def setUp(self) -> None:
        self.coordinates: Coordinates = Coordinates(1, 1)
        self.minion: Minion = Minion(1, self.coordinates)

    def test_give_xp(self):
        self.minion._level = 2
        expected_xp: int = 20
        actual_xp: int = self.minion.give_xp()
        self.assertEqual(actual_xp, expected_xp)

    def test_minion_attack(self):
        expected_dmg: int = 15
        actual_dmg: int = self.minion.attack()
        self.assertEqual(actual_dmg, expected_dmg)

    def test_diplay_minion(self):
        expected: str = "Minion level= 1"
        actual: str = self.minion.__str__()
        self.assertEqual(actual, expected)


class MapTest(unittest.TestCase):

    def setUp(self) -> None:
        self.map: Map = Map()

    def test_map_loaded_correctly(self):
        actual_map: str = self.map.__str__()
        expected_map: str = ("#.#.#.T###.####...M.\n" +
                             "#..T...T..##.##T....\n" +
                             "TT.TT..#....M...###.\n" +
                             "T..#.#TM..##...##M..\n" +
                             "#T..TT.#.T..M.##....\n")
        self.assertEqual(actual_map, expected_map)

    def test_change_coordinate(self):
        empty_coordinates: Coordinates = Coordinates(0, 1)
        symbol: str = "1"
        self.map.change_symbol(empty_coordinates, symbol)
        actual: str = self.map.get_symbol(empty_coordinates)
        self.assertEqual(actual, symbol)

    def test_get_minion(self):
        minion_coordinates: Coordinates = Coordinates(0, 18)

        symbol: str = self.map.get_symbol(minion_coordinates)
        self.assertEqual(symbol, MapSymbols.MINION.value)

        minion = self.map.get_object(minion_coordinates)
        self.assertTrue(isinstance(minion, Minion))

    def test_get_treasure(self):
        treasure_coordinates: Coordinates = Coordinates(1, 3)

        symbol: str = self.map.get_symbol(treasure_coordinates)
        self.assertEqual(symbol, MapSymbols.TREASURE.value)

        treasure = self.map.get_object(treasure_coordinates)
        self.assertTrue(isinstance(treasure, Treasure))


class GameTacticsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.game: GameTactics = GameTactics()

    def test_move_hero_to_free_spot(self):
        hero_symbol: str = "1"
        free_coordinates: Coordinates = Coordinates(0, 1)
        hero: Hero = Hero(hero_symbol, free_coordinates)
        self.game.spawn_hero(hero)

        acutal_msg: str = self.game.move_hero(hero, Direction.DOWN)
        expected_msg: str = Messages.SUCCESSFUL_MOVE
        self.assertEqual(acutal_msg, expected_msg)

        previous_spot_symbol: str = self.game._map.get_symbol(free_coordinates)
        self.assertEqual(previous_spot_symbol, MapSymbols.FREE_SPOT.value)

        current_spot_symbol: str = self.game._map.get_symbol(
            Direction.coordinates_after_movement(free_coordinates, Direction.DOWN))
        self.assertEqual(current_spot_symbol, hero_symbol)

    def test_move_hero_to_obstacle(self):
        hero_symbol: str = "1"
        free_coordinates: Coordinates = Coordinates(0, 10)
        hero: Hero = Hero(hero_symbol, free_coordinates)
        self.game.spawn_hero(hero)

        acutal_msg: str = self.game.move_hero(hero, Direction.DOWN)
        expected_msg: str = Messages.INVALID_MOVE
        self.assertEqual(acutal_msg, expected_msg)

        hero_spot_coordinates: str = self.game._map.get_symbol(
            free_coordinates)
        self.assertEqual(hero_spot_coordinates, hero_symbol)

        obstacle_spot_symbol: str = self.game._map.get_symbol(
            Direction.coordinates_after_movement(free_coordinates, Direction.DOWN))
        self.assertEqual(obstacle_spot_symbol, MapSymbols.OBSTACLE.value)

    def test_move_hero_to_treasure(self):
        hero_symbol: str = "1"
        free_coordinates: Coordinates = Coordinates(0, 5)
        hero: Hero = Hero(hero_symbol, free_coordinates)
        self.game.spawn_hero(hero)

        acutal_msg: str = self.game.move_hero(hero, Direction.RIGHT)
        self.assertTrue("added" in acutal_msg)

        previous_spot_symbol: str = self.game._map.get_symbol(free_coordinates)
        self.assertEqual(previous_spot_symbol, MapSymbols.FREE_SPOT.value)

        current_spot_symbol: str = self.game._map.get_symbol(
            Direction.coordinates_after_movement(free_coordinates, Direction.RIGHT))
        self.assertEqual(current_spot_symbol, hero_symbol)

    def test_move_hero_and_fight_with_minion_and_win(self):
        hero_symbol: str = "1"
        free_coordinates: Coordinates = Coordinates(3, 18)
        hero: Hero = Hero(hero_symbol, free_coordinates)
        self.game.spawn_hero(hero)

        acutal_msg: str = self.game.move_hero(hero, Direction.LEFT)
        self.assertTrue("Minion killed" in acutal_msg)
        self.assertTrue(hero.is_alive())

        previous_spot_symbol: str = self.game._map.get_symbol(free_coordinates)
        self.assertEqual(previous_spot_symbol, MapSymbols.FREE_SPOT.value)

        current_spot_symbol: str = self.game._map.get_symbol(
            Direction.coordinates_after_movement(free_coordinates, Direction.LEFT))
        self.assertEqual(current_spot_symbol, hero_symbol)

    def test_move_hero_and_fight_with_minion_and_die(self):
        hero_symbol: str = "1"
        free_coordinates: Coordinates = Coordinates(4, 13)
        hero: Hero = Hero(hero_symbol, free_coordinates)
        self.game.spawn_hero(hero)

        acutal_msg: str = self.game.move_hero(hero, Direction.LEFT)
        self.assertTrue("You died" in acutal_msg)
        self.assertFalse(hero.is_alive())

        previous_spot_symbol: str = self.game._map.get_symbol(free_coordinates)
        self.assertEqual(previous_spot_symbol, MapSymbols.FREE_SPOT.value)

        current_spot_symbol: str = self.game._map.get_symbol(
            Direction.coordinates_after_movement(free_coordinates, Direction.LEFT))
        self.assertEqual(current_spot_symbol, MapSymbols.MINION.value)

    def test_move_hero_to_another_hero_and_back(self):
        hero_symbol1: str = "1"
        free_coordinates1: Coordinates = Coordinates(1, 1)
        hero1: Hero = Hero(hero_symbol1, free_coordinates1)
        hero_symbol2: str = "2"
        free_coordinates2: Coordinates = Coordinates(1, 2)
        hero2: Hero = Hero(hero_symbol2, free_coordinates2)
        self.game.spawn_hero(hero1)
        self.game.spawn_hero(hero2)

        acutal_msg: str = self.game.move_hero(hero2, Direction.LEFT)
        self.assertEqual(acutal_msg, Messages.SUCCESSFUL_MOVE)

        previous_spot_symbol: str = self.game._map.get_symbol(
            free_coordinates2)
        self.assertEqual(previous_spot_symbol, MapSymbols.FREE_SPOT.value)

        current_spot_symbol: str = self.game._map.get_symbol(
            Direction.coordinates_after_movement(free_coordinates2, Direction.LEFT))
        self.assertEqual(current_spot_symbol, hero_symbol2 + hero_symbol1)

        acutal_msg: str = self.game.move_hero(hero2, Direction.RIGHT)
        self.assertEqual(acutal_msg, Messages.SUCCESSFUL_MOVE)

        previous_spot_symbol: str = self.game._map.get_symbol(
            free_coordinates1)
        self.assertEqual(previous_spot_symbol, hero_symbol1)

        current_spot_symbol: str = self.game._map.get_symbol(
            Direction.coordinates_after_movement(free_coordinates1, Direction.RIGHT))
        self.assertEqual(current_spot_symbol, hero_symbol2)

    def test_move_hero_to_invalid_coordinates(self):
        hero_symbol: str = "1"
        free_coordinates: Coordinates = Coordinates(0, 19)
        hero: Hero = Hero(hero_symbol, free_coordinates)
        self.game.spawn_hero(hero)

        acutal_msg: str = self.game.move_hero(hero, Direction.RIGHT)
        self.assertEqual(acutal_msg, Messages.INVALID_MOVE)

    def test_swap_item(self):
        hero_symbol1: str = "1"
        hero_symbol2: str = "2"
        coordinates: Coordinates = Coordinates(1, 1)
        hero1: Hero = Hero(hero_symbol1, coordinates)
        hero2: Hero = Hero(hero_symbol2, coordinates)
        item: Treasure = Potion("potion", 10, coordinates,
                                TreasureType.HEALTH_POTION)
        hero1.add_to_backpack(item)
        actual_msg: str = self.game.swap_item(hero1, hero2, 0)
        self.assertTrue("swapped" in actual_msg)
        treasure: Treasure = hero2.get_from_backpack(0)
        self.assertEqual(treasure, item)

    def test_swap_item_with_full_backpack(self):
        hero_symbol1: str = "1"
        hero_symbol2: str = "2"
        coordinates: Coordinates = Coordinates(1, 1)
        hero1: Hero = Hero(hero_symbol1, coordinates)
        hero2: Hero = Hero(hero_symbol2, coordinates)
        item: Treasure = Potion("potion", 10, coordinates,
                                TreasureType.HEALTH_POTION)
        hero1.add_to_backpack(item)
        self._fill_backpack(hero2)
        actual_msg: str = self.game.swap_item(hero1, hero2, 0)
        self.assertEqual(actual_msg, Messages.OPPONENT_BACKPACK_FULL)
        treasure: Treasure = hero1.get_from_backpack(0)
        self.assertEqual(treasure, item)

    def _fill_backpack(self, hero: Hero) -> None:
        coordinates: Coordinates = Coordinates(0, 0)
        for _ in range(10):
            hero.add_to_backpack(Potion("potion", 10, coordinates,
                                        TreasureType.HEALTH_POTION))

    def test_swap_item_with_heroes_different_coordinates(self):
        hero_symbol1: str = "1"
        hero_symbol2: str = "2"
        coordinates1: Coordinates = Coordinates(1, 1)
        coordinates2: Coordinates = Coordinates(1, 2)
        hero1: Hero = Hero(hero_symbol1, coordinates1)
        hero2: Hero = Hero(hero_symbol2, coordinates2)
        item: Treasure = Potion("potion", 10, coordinates1,
                                TreasureType.HEALTH_POTION)
        hero1.add_to_backpack(item)
        actual_msg: str = self.game.swap_item(hero1, hero2, 0)
        self.assertEqual(actual_msg, Messages.NOT_ON_SAME_SPOT)
        treasure: Treasure = hero1.get_from_backpack(0)
        self.assertEqual(treasure, item)

    def test_swap_item_with_heroes_invalid_index(self):
        hero_symbol1: str = "1"
        hero_symbol2: str = "2"
        coordinates: Coordinates = Coordinates(1, 1)
        hero1: Hero = Hero(hero_symbol1, coordinates)
        hero2: Hero = Hero(hero_symbol2, coordinates)
        item: Treasure = Potion("potion", 10, coordinates,
                                TreasureType.HEALTH_POTION)
        hero1.add_to_backpack(item)
        actual_msg: str = self.game.swap_item(hero1, hero2, 3)
        self.assertEqual(actual_msg, Messages.ITEM_NOT_FOUND_IN_BACKPACK)
        treasure: Treasure = hero1.get_from_backpack(0)
        self.assertEqual(treasure, item)

    def test_hero_use_item_from_backpack(self):
        hero_symbol: str = "1"
        coordinates: Coordinates = Coordinates(1, 1)
        hero: Hero = Hero(hero_symbol, coordinates)
        item: Treasure = Potion("potion", 10, coordinates,
                                TreasureType.HEALTH_POTION)
        hero.add_to_backpack(item)
        message_use: str = self.game.hero_use_item_from_backpack(hero, 0)
        self.assertEqual(message_use, "+10 health")
        self.assertFalse(item in hero._backpack._backpack)

    def test_hero_use_item_from_backpack_invalid_index(self):
        hero_symbol: str = "1"
        coordinates: Coordinates = Coordinates(1, 1)
        hero: Hero = Hero(hero_symbol, coordinates)
        item: Treasure = Potion("potion", 10, coordinates,
                                TreasureType.HEALTH_POTION)
        hero.add_to_backpack(item)
        message_use: str = self.game.hero_use_item_from_backpack(hero, 3)
        self.assertEqual(message_use, Messages.ITEM_NOT_FOUND_IN_BACKPACK)

    def test_hero_remove_item_from_backpack(self):
        hero_symbol: str = "1"
        coordinates: Coordinates = Coordinates(1, 1)
        hero: Hero = Hero(hero_symbol, coordinates)
        item: Treasure = Potion("potion", 10, coordinates,
                                TreasureType.HEALTH_POTION)
        hero.add_to_backpack(item)
        message: str = self.game.hero_remove_item_from_backpack(hero, 0)
        self.assertTrue("removed" in message)
        self.assertFalse(item in hero._backpack._backpack)

    def test_hero_remove_item_from_backpack_invalid_index(self):
        hero_symbol: str = "1"
        coordinates: Coordinates = Coordinates(1, 1)
        hero: Hero = Hero(hero_symbol, coordinates)
        item: Treasure = Potion("potion", 10, coordinates,
                                TreasureType.HEALTH_POTION)
        hero.add_to_backpack(item)
        message: str = self.game.hero_remove_item_from_backpack(hero, 3)
        self.assertEqual(message, Messages.ITEM_NOT_FOUND_IN_BACKPACK)
        self.assertTrue(item in hero._backpack._backpack)

    def test_heroes_fight_not_on_same_spot(self):
        hero_symbol1: str = "1"
        hero_symbol2: str = "2"
        coordinates1: Coordinates = Coordinates(1, 1)
        coordinates2: Coordinates = Coordinates(1, 2)
        hero1: Hero = Hero(hero_symbol1, coordinates1)
        hero2: Hero = Hero(hero_symbol2, coordinates2)

        message: str = self.game.heroes_fight(hero1, hero2)
        self.assertEqual(message, Messages.NOT_ON_SAME_SPOT)

    def test_heroes_fight_hero1_win(self):
        hero_symbol1: str = "1"
        hero_symbol2: str = "2"
        coordinates: Coordinates = Coordinates(1, 1)
        hero1: Hero = Hero(hero_symbol1, coordinates)
        hero2: Hero = Hero(hero_symbol2, coordinates)
        item: Treasure = Potion("potion", 10, coordinates,
                                TreasureType.HEALTH_POTION)
        item.use(hero1)
        message: str = self.game.heroes_fight(hero1, hero2)
        self.assertTrue(hero1.is_alive())
        self.assertFalse(hero2.is_alive())
        self.assertTrue("You killed Hero 2" in message)

    def test_heroes_fight_hero2_win(self):
        hero_symbol1: str = "1"
        hero_symbol2: str = "2"
        coordinates: Coordinates = Coordinates(1, 1)
        hero1: Hero = Hero(hero_symbol1, coordinates)
        hero2: Hero = Hero(hero_symbol2, coordinates)
        item: Treasure = Potion("potion", 10, coordinates,
                                TreasureType.HEALTH_POTION)
        item.use(hero2)
        message: str = self.game.heroes_fight(hero1, hero2)
        self.assertTrue(hero2.is_alive())
        self.assertFalse(hero1.is_alive())
        self.assertTrue("You died from Hero 2" in message)

    def test_get_other_player_symbol(self):
        hero_symbol1: str = "1"
        free_coordinates1: Coordinates = Coordinates(1, 1)
        hero1: Hero = Hero(hero_symbol1, free_coordinates1)
        hero_symbol2: str = "2"
        free_coordinates2: Coordinates = Coordinates(1, 2)
        hero2: Hero = Hero(hero_symbol2, free_coordinates2)
        self.game.spawn_hero(hero1)
        self.game.spawn_hero(hero2)

        self.game.move_hero(hero2, Direction.LEFT)

        other_player_symbol = self.game.get_other_player_symbol(hero1)
        self.assertEqual(other_player_symbol, hero_symbol2)

    def test_get_other_player_symbol_not_on_same_coordiantes(self):
        hero_symbol1: str = "1"
        free_coordinates1: Coordinates = Coordinates(1, 1)
        hero1: Hero = Hero(hero_symbol1, free_coordinates1)
        hero_symbol2: str = "2"
        free_coordinates2: Coordinates = Coordinates(1, 2)
        hero2: Hero = Hero(hero_symbol2, free_coordinates2)
        self.game.spawn_hero(hero1)
        self.game.spawn_hero(hero2)

        message = self.game.get_other_player_symbol(hero1)
        self.assertEqual(message, Messages.NOT_ON_SAME_SPOT)

    def test_get_random_free_coordinates(self):
        free_coordinates: Coordinates = self.game.get_random_free_coordinates()
        symbol: str = self.game._map.get_symbol(free_coordinates)
        self.assertEqual(symbol, MapSymbols.FREE_SPOT.value)


if __name__ == '__main__':
    unittest.main()
