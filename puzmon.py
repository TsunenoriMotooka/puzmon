'''
update: 2025/03/27
author: tsune.motooka
'''

# import

# const
monster_names = [
        'スライム',
        'ゴブリン',
        'オオコウモリ',
        'ウェアウルフ',
        'ドラゴン',
        ]

# function
def main():
    player_name = input_player_name()

    print('*** Puzzle & Monsters ***')

    win_count = go_dungeon(player_name)

    if win_count >= len(monster_names):
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
    for monster_name in monster_names:
        win = do_battle(monster_name)
        if win > 0:
            win_count += win
        else:
            break

    print(f'{player_name}はダンジョンを制覇した')

    return win_count

def do_battle(monster_name):
    print(f'{monster_name}が現れた！')
    print(f'{monster_name}を倒した！')
    return 1


# start app
main()

