#!/usr/bin/env python
import re
import itertools
import copy


class Arena(object):


    def __init__(self, player, boss, shop):
        self.player = player
        self.boss = boss
        self.shop = shop
        self.win_configs = []


    def run_battles(self):
        # Buy items, give them to player to equip and then run battle
        for item_choice in self.shop.item_choices():
            # 'Clone' player and boss for fight simulations
            player = copy.copy(self.player)
            boss = copy.copy(self.boss)
            # Buy and give item choice
            player.buy_items(item_choice)
            # Equip items (update player's stats)
            player.equip_items()
            # Run battle
            if self.fight(player, boss):
                win_config = (player.cost, player.items, player.hps,
                        player.att, player.arm, boss.hps)
                self.win_configs.append(win_config)


    def fight(self, player, boss):
        # Function to carry out attacks and check if defender is alive
        def attack(attacker, defender):
            # Calculate attack damage
            dmg = attacker.att - defender.arm
            # An attack must deal at least 1
            if dmg < 1:
                dmg = 1
            # Make attack
            defender.hps -= dmg
            # If defender is ded, return True else False
            if defender.hps < 1:
                return True
            else:
                return False
        while True:
            # Make an attack and if it successfully kills opponent, end clone simulation
            if attack(player, boss):
                return True
            if attack(boss, player):
                return False


class Player(object):


    def __init__(self):
        self.hps = 100
        self.att = 0
        self.arm = 0
        self.items = []
        self.items_cost = 0

    def buy_items(self, items):
        # Set items and determine cost
        self.items = items
        self.cost = sum([i.cost for i in items])


    def equip_items(self):
        for item in self.items:
            # Skip item if it is an empty armor placeholder
            if not item.name:
                continue
            # Set new stats with items
            self.att += item.att
            self.arm += item.arm


class Shop(object):


    def __init__(self, shop_strings):
        self.shop_strings = shop_strings
        # Process shop strings
        self.process_shop_strings()


    def process_shop_strings(self):
        cat_re = re.compile(r'^(.+?):.+$')
        item_name_re = re.compile(r'^(.+?)  .+$')
        item_stats_re = re.compile(r' ([0-9]+)')
        # Splitting items into different categories
        items = []
        category = None
        for s in self.shop_strings:
            # If line is blank, continue
            if not s:
                continue
            # If at new category, process items in new group
            if any(s.startswith(c) for c in ['Weapons', 'Armor', 'Rings']):
                # If we've filled a category, add it to class
                if category:
                    setattr(self, category.lower(), items)
                    items = []
                # Get new category
                category = cat_re.match(s).group(1)
                continue
            # If just item, add it to the list
            item_name = item_name_re.match(s).group(1)
            item_stats = map(int, item_stats_re.findall(s))
            items.append(Item(item_name, category, *item_stats))
        # Append last category to items
        setattr(self, category.lower(), items)


    def item_choices(self):
        # Can have one or any two rings
        rings = list(itertools.combinations(self.rings, 2)) + self.rings
        # Armor is optional; weapon is not
        armor = self.armor + [Item(None, None, 0, None, None)]
        # Just using for loops here instead or recusion or itertools
        for w in self.weapons:
            for a in armor:
                for r in rings:
                    # If rings is tuple, flatten
                    if isinstance(r, tuple):
                        yield w, a, r[0], r[1]
                    else:
                        yield w, a, r


class Item(object):


    def __init__(self, name, category, cost, damage, armor):
        self.name = name
        self.category = category
        self.cost = cost
        self.att = damage
        self.arm = armor


class Boss(object):


    def __init__(self, boss_strings):
        self.boss_strings = boss_strings
        # Process boss strings
        self.process_boss_strings()


    def process_boss_strings(self):
        stats_re = re.compile(r'^(.+?): ([0-9]+)')
        for n, s in [stats_re.match(l).groups() for l in self.boss_strings]:
            if n == 'Hit Points':
                self.hps = int(s)
            elif n == 'Damage':
                self.att = int(s)
            elif n == 'Armor':
                self.arm = int(s)


def main():
    # Load input information
    input_file = 'input.txt'
    shop_file = 'shop.txt'
    with open(input_file, 'r') as f:
        boss_strings = [l.rstrip() for l in f]
    with open(shop_file, 'r') as f:
        shop_strings = [l.rstrip() for l in f]
    # Initialise objects
    player = Player()
    shop = Shop(shop_strings)
    boss = Boss(boss_strings)
    arena = Arena(player, boss, shop)
    # Select items and run battles
    arena.run_battles()
    # Find cheapest win
    print min(arena.win_configs, key=lambda k: k[0])[0]


if __name__ == '__main__':
    main()
