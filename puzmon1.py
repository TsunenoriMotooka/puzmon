'''
update: 2025/03/27
author: tsune.motooka
'''

# import

# const

# function
def main():
    player_name = input('プレイヤー名を入力してください>')

    print('*** Puzzle & Monsters ***')

    win_count = go_dungeon(player_name)

    print('*** GAME CLEARED!! ***')
    print(f'倒したモンスター数={win_count}')

def go_dungeon(player_name):
    win_count = 0
    print(f'{player_name}はダンジョンに到着した')
    print(f'{player_name}はダンジョンを制覇した')
    
    # TODO: プロット
    win_count = 5

    return win_count

# start app
main()

