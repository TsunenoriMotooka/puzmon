'''
update: 2025/03/27
author: tsune.motooka
'''

# import
import random

from const import *
from monster import Monster
from party import Party

# main
def main():
    player_name = input_player_name()

    print('*** Puzzle & Monsters ***')

    # data
    enemys = [
            Monster('スライム',    100, '水', 10,  1),
            Monster('ゴブリン',    200, '土', 20,  5),
            Monster('オオコウモリ',300, '風', 30, 10),
            Monster('ウェアウルフ',400, '風', 40, 15),
            Monster('ドラゴン',    600, '火', 50, 20),
            ]

    friends = [
            Monster('朱雀', 150, '火', 25, 10),
            Monster('青龍', 150, '風', 15, 10),
            Monster('白虎', 150, '土', 20,  5),
            Monster('玄武', 150, '水', 20, 15),
            ]        
    party = Party(player_name, friends)

    win_count = go_dungeon(party, enemys)
    if win_count >= len(enemys):
        print('*** GAME CLEARED!! ***')
    else:
        print('*** GAME OVER!! ***')
    print(f'倒したモンスター数={win_count}')

def input_player_name():
    while True:
        player_name = input('プレイヤー名を入力してください>') or ''
        if len(player_name) == 0:
            print('エラー：プレイヤー名を入力してください')
        else:
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

def on_player_turn(party, enemy):
    print(f'\n【{party.name}のターン】(HP={party.hp})')
    show_battle_field(party, enemy)
    command = input_command()

    before = command[0:1].upper()
    after = command[-1:].upper()
    beforeIndex = ord(before) - 65 
    afterIndex = ord(after) - 65
    party.gems.move(beforeIndex, afterIndex)

    evaluate_gems(party, enemy)
            
def evaluate_gems(party, enemy):
    combo = 0
    while True:
        has_banished = False
        while True: 
            element, banish_list = party.gems.check_banishable()
            if element is None:
                break

            party.gems.banish()
            has_banished = True
        
            if element == ELEMENT_LIFE:
                do_recover(party, len(banish_list), combo)
            else:
                friend = party.get_friend_by_element(element)
                if friend is not None:
                    combo += 1
                    do_attack(friend, enemy, len(banish_list), combo)

        if has_banished:
            party.gems.shift()
            party.gems.spawn()
        else:
            break

def on_enemy_turn(party, enemy):
    print(f'\n【{enemy.name}のターン】(HP={enemy.hp})')
    do_enemy_attack(party, enemy)

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

def do_attack(friend, enemy, banish_count, combo):
    element_boost = get_element_boost(friend.element, enemy.element)
    combo_boost = get_combo_boost(banish_count, combo)

    damage = (friend.ap - enemy.dp) * element_boost * combo_boost
    threshold = damage  / 10
    
    damage = blur_damage(damage, threshold)
    
    friend.print_name()
    print(f'の攻撃！{f' {combo} Commbo!!' if combo > 1 else ''}')
    enemy.print_name()
    print(f'に{damage}のダメージを与えた')
    enemy.hp = max(0, enemy.hp - damage)

def do_recover(party, banish_count, combo):
    combo_boost = get_combo_boost(banish_count, combo)
    heal = 20 * combo_boost
    threshold = heal / 10
    heal = blur_damage(heal, threshold)
    print(f'{party.name}のHPは{heal}回復した')
    party.hp = min(party.hp + heal, party.max_hp)

def do_enemy_attack(party, enemy):
    damage = enemy.ap - party.dp
    threshold = damage / 10
    damage = blur_damage(damage, threshold)
    print(f'{damage}のダメージを受けた')
    party.hp = max(0, party.hp - damage)

def get_element_boost(attack_element, defence_element):
    return ELEMENT_BOOST.get(attack_element+defence_element) or 1.0

def get_combo_boost(banish_count, combo):
    return 1.5 ** max(1, banish_count - 3 + combo) 

def show_battle_field(party, enemy):
    print(f'バトルフィールド')
    enemy.print_name()
    print(f'HP = {enemy.hp:3d} / {enemy.max_hp:3d}\n')
    [print(f'{' ' if i > 0 else ''}', end='') or friend.print_name() for i, friend in enumerate(party.friends, 0)]
    print(f'\nHP = {party.hp:3d} / {party.max_hp:3d}')
    print(f'{'-'*LINE_LENGTH}')
    [print(f'{' ' if i > 0 else ''}{chr(i+65)}', end='') for i in range(GEMS_LENGTH)]
    print()
    party.gems.show()
    print(f'{'-'*LINE_LENGTH}')

def input_command():
    while True:
        command = input('コマンド？>')
        if check_valid_command(command):
            return command

def check_valid_command(command):
    if len(command) != 2:
        print(f'2文字で入力して下さい。')
        return False

    before = command[0:1].upper()
    after = command[-1:].upper()
    
    table = [chr(i+65) for i in range(GEMS_LENGTH)]
    if before not in table or after not in table:
        print(f'{table[0]}~{table[-1]}の範囲で入力してくだい')
        return False
    
    if before == after:
        print(f'1文字目と2文字目が同じ値です')
        return False

    return True

def blur_damage(damage, threshold):
    return max(1, int(damage + random.uniform(-threshold, threshold)))

# start app
main()

