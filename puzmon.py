'''
update: 2025/03/27
author: tsune.motooka
'''

# import
import math
import random

# const
ELEMENT_SYMBOLS = {
        '火': '$',
        '水': '~',
        '風': '@',
        '土': '#',
        '命': '&',
        '無': ' ',
        }
ELEMENT_COLORS = {
        '火': '1',
        '水': '6',
        '風': '2',
        '土': '3',
        '命': '5',
        '無': '7',
        }

LINE_LENGTH = 32

# class
class Monster:
    def __init__(self, name, max_hp, element, ap, dp):
        self.name = name
        self.hp = max_hp
        self.max_hp = max_hp
        self.element = element
        self.ap = ap
        self.dp = dp

    def print_name(self):
        symbol = ELEMENT_SYMBOLS[self.element]
        color  = '4' + ELEMENT_COLORS[self.element]
        print(f'\033[{color}m\033[30m{symbol}{self.name}{symbol}\033[0m', end='')

class Party:
    def __init__(self, name, friends):
        self.name = name
        self.friends = friends
        self.hp = sum([friend.hp for friend in friends])
        self.max_hp = sum([friend.max_hp for friend in friends])
        self.dp = math.ceil(sum([friend.dp for friend in friends]) / len(friends))
        self.gems = self.fill_gems(14)

    def show(self):
        print(f'＜パーティ編成＞')
        print(f'{'-'*LINE_LENGTH}')
        for friend in self.friends:
            friend.print_name()
            print(f' HP= {friend.hp:3} 攻撃= {friend.ap:2} 防御= {friend.dp:2}')
        print(f'{'-'*LINE_LENGTH}\n')

    def fill_gems(self, count):
        gems = [random.choice(list(ELEMENT_SYMBOLS.items())) for i in range(count)]
        return gems

    def show_gems(self):
        print(f'{'-'*LINE_LENGTH}')
        [print(f'{' ' if i > 0 else ''}{chr(i+65)}', end='') for i in range(14)]
        print()
        for i, (key, value) in enumerate(self.gems, 0):
           color  = '4' + ELEMENT_COLORS[key]
           print(f'{' ' if i > 0 else ''}', end='')
           print(f'\033[{color}m\033[30m{value}\033[0m', end='')
        print(f'\n{'-'*LINE_LENGTH}')

# data
enemys = [
        Monster('スライム',    100, '水', 10,  1),
        Monster('ゴブリン',    200, '土', 20,  5),
        Monster('オオコウモリ',300, '風', 30, 10),
        Monster('ウェアウルフ',400, '風', 40, 15),
        Monster('ドラゴン',    600, '火', 50, 20),
        ]

friends = [
        Monster('青龍', 150, '風', 15, 10),
        Monster('朱雀', 150, '火', 25, 10),
        Monster('白虎', 150, '土', 20,  5),
        Monster('玄武', 150, '水', 20, 15),
        ]        

# function
def main():
    player_name = input_player_name()

    print('*** Puzzle & Monsters ***')

    party = organize_party(player_name, friends)

    win_count = go_dungeon(party, enemys)

    if win_count >= len(enemys):
        print('*** GAME CLEARED!! ***')
    else:
        print('*** GAME OVER!! ***')
    print(f'倒したモンスター数={win_count}')

def input_player_name():
    player_name = ''
    while len(player_name) == 0:
        player_name = input('プレイヤー名を入力してください>') or ''
        if len(player_name) == 0:
            print('エラー：プレイヤー名を入力してください')
    
    return player_name

def go_dungeon(party, enemys):
    print(f'{party.name}のパーティ(HP={party.hp})はダンジョンに到着した')
    party.show()

    #モンスターとの戦闘
    win_count = 0
    for enemy in enemys:
        win_count += do_battle(party, enemy)

        if party.hp > 0:
            print(f'{party.name}はさらに奥へと進んだ')
            print(f'{'='*LINE_LENGTH}')
        else:
            print(f'{party.name}はダンジョンから逃げ出した')
            break
    else:
        print(f'{party.name}はダンジョンを制覇した')

    return win_count

def organize_party(player_name, friends):
    return Party(player_name, friends)

def on_player_turn(party, enemy):
    print(f'\n【{party.name}のターン】(HP={party.hp})')
    show_battle_field(party, enemy)
    command = input('コマンド？>')
    do_attack(enemy, command)

def on_enemy_turn(party, enemy):
    print(f'\n【{enemy.name}のターン】(HP={enemy.hp})')
    do_enemy_attack(party)

def do_battle(party, enemy):
    enemy.print_name()
    print(f'が現れた！')
    
    while True:
        on_player_turn(party, enemy)
        if enemy.hp <= 0:
            enemy.print_name()
            print(f'を倒した！')
            return 1

        on_enemy_turn(party, enemy)
        if party.hp <= 0:
            print(f'パーティのHPが0になった')
            return 0

def do_attack(enemy, command):
    damage = abs(hash(command)) % 50
    damage += math.floor(damage + random.uniform(-damage/10, damage/10))
    print(f'{damage}のダメージを与えた')
    enemy.hp = max(0, enemy.hp - damage)

def do_enemy_attack(party):
    damage = 200
    print(f'{damage}のダメージを受けた')
    party.hp = max(0, party.hp - damage)

def show_battle_field(party, enemy):
    print(f'バトルフィールド')
    enemy.print_name()
    print(f'HP = {enemy.hp:3d} / {enemy.max_hp:3d}\n')
    [print(f'{' ' if i > 0 else ''}', end='') or friend.print_name() for i, friend in enumerate(party.friends, 0)]
    print(f'\nHP = {party.hp:3d} / {party.max_hp:3d}')
    party.show_gems()

# start app
main()

