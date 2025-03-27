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

# data
monsters = [
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

    win_count = go_dungeon(party, monsters)

    if win_count >= len(monsters):
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

def go_dungeon(party, monsters):
    win_count = 0
    print(f'{party['player_name']}のパーティ(HP={party['hp']})はダンジョンに到着した')
    show_party(party)
    #モンスターとの戦闘
    for monster in monsters:
        win_count += do_battle(monster)

        if party['hp'] > 0:
            print(f'{party['player_name']}はさらに奥へと進んだ')
            print(f'{'='*32}')
        else:
            print(f'{party['player_name']}はダンジョンから逃げ出した')
            break
    else:
        print(f'{party['player_name']}はダンジョンを制覇した')

    return win_count

def do_battle(monster):
    monster.print_name()
    print(f'が現れた！')
    monster.print_name()
    print(f'を倒した！')
    return 1

def organize_party(player_name, friends):
    sum_hp = sum([friend.hp for friend in friends])
    sum_max_hp = sum([friend.max_hp for friend in friends])
    avg_dp = math.ceil(sum([friend.dp for friend in friends]) / len(friends))

    party = {
            'player_name': player_name,
            'friends': friends,
            'hp': sum_hp,
            'max_hp': sum_max_hp,
            'dp': avg_dp
            }
    
    return party

def show_party(party):
    print(f'＜パーティ編成＞----------------')
    for friend in party['friends']:
        friend.print_name()
        print(f' HP= {friend.hp:3} 攻撃= {friend.ap:2} 防御= {friend.dp:2}')
    print(f'{'-'*32}\n')

# start app
main()

