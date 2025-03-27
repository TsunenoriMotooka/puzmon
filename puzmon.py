'''
update: 2025/03/27
author: tsune.motooka
'''

# import

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

# function
def main():
    player_name = input_player_name()

    print('*** Puzzle & Monsters ***')

    win_count = go_dungeon(player_name)

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

def go_dungeon(player_name):
    win_count = 0
    print(f'{player_name}はダンジョンに到着した')
   
    #モンスターとの戦闘
    for monster in monsters:
        win = do_battle(monster)
        if win > 0:
            win_count += win
        else:
            break

    print(f'{player_name}はダンジョンを制覇した')

    return win_count

def do_battle(monster):
    monster.print_name()
    print(f'が現れた！')
    monster.print_name()
    print(f'を倒した！')
    return 1


# start app
main()

