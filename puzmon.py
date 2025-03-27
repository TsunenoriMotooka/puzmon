'''
update: 2025/03/27
author: tsune.motooka
'''

# import
import math

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
        color  = '3' + ELEMENT_COLORS[self.element]
        print(f'\033[{color}m{symbol}{self.name}{symbol}\033[0m', end='')

class Party:
    def __init__(self, name, friends):
        self.name = name
        self.friends = friends
        self.hp = sum([friend.hp for friend in friends])
        self_max_hp = sum([friend.max_hp for friend in friends])
        self.dp = math.ceil(sum([friend.dp for friend in friends]) / len(friends))
    
    def show(self):
        print(f'＜パーティ編成＞----------------')
        for friend in self.friends:
            friend.print_name()
            print(f' HP= {friend.hp:3} 攻撃= {friend.ap:2} 防御= {friend.dp:2}')
        print(f'{'-'*32}\n')

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
            print(f'{'='*32}')
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
    damage = 50
    print(f'{damage}のダメージを与えた')
    enemy.hp = max(0, enemy.hp - damage)

def do_enemy_attack(party):
    damage = 200
    print(f'{damage}のダメージを受けた')
    party.hp = max(0, party.hp - damage)

# start app
main()

