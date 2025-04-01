'''
update: 2025/03/27
author: tsune.motooka
'''

# import
import math
import random

# const
ELEMENT_NONE = '無'
ELEMENT_LIFE = '命'

ELEMENT_SYMBOLS = {
        '火': '$',
        '風': '@',
        '土': '#',
        '水': '~',
        '命': '&',
        '無': ' ',
        }
ELEMENT_COLORS = {
        '火': '1',
        '風': '2',
        '土': '3',
        '水': '6',
        '命': '5',
        '無': '7',
        }

ELEMENT_BOOST = [
        1.0,
        0.5,
        1.0,
        2.0,
        ]

GEMS_LENGTH = 14

LINE_LENGTH = 34

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
        self.gems = self.fill_gems(GEMS_LENGTH)

    def show(self):
        print(f'＜パーティ編成＞')
        print(f'{'-'*LINE_LENGTH}')
        for friend in self.friends:
            friend.print_name()
            print(f' HP= {friend.hp:3} 攻撃= {friend.ap:2} 防御= {friend.dp:2}')
        print(f'{'-'*LINE_LENGTH}\n')

    def fill_gems(self, count):
        gems = [random.choice(list(ELEMENT_SYMBOLS.keys())[0:-1]) for i in range(count)]
        return gems

    def show_gems(self, banish_element=None, banish_count=0):
        for i, element in enumerate(self.gems, 0):
            print(f'{' ' if i > 0 else ''}', end='')
            self.show_gem(element)

        if banish_element is not None:
            print('  ', end='')
            self.show_gem(banish_element)
            print(f'x{banish_count}', end='')

        print()

    def show_gem(self, element):
        color  = '4' + ELEMENT_COLORS[element]
        print(f'\033[{color}m\033[30m{ELEMENT_SYMBOLS[element]}\033[0m', end='')

    def move_gem(self, beforeIndex, afterIndex, output=True):
        if beforeIndex < 0 or beforeIndex >= len(self.gems):
            return
        if afterIndex < 0 or afterIndex >= len(self.gems):
            return

        self.show_gems()
        step = 1 if beforeIndex < afterIndex else -1 
        [self.swap_gem(i, step, output) for i in range(beforeIndex, afterIndex, step)]

    def swap_gem(self, index, step, output=True): 
        if index < 0 or index + step < 0 or index >= len(self.gems) or index + step >= len(self.gems):
            return

        temp = self.gems[index + step]
        self.gems[index + step] = self.gems[index]
        self.gems[index] = temp

        if output:
            self.show_gems()
    
    def check_banishable(self):
        for i in range(GEMS_LENGTH - 2):
            if self.gems[i] == ELEMENT_NONE:
                continue

            if self.gems[i:i+3] == [self.gems[i]] * 3:
                return i
        return -1

    def banish_gems(self, index):
        gem = self.gems[index]
        count = 0
        for i in range(index, len(self.gems)):
            if gem == self.gems[i]:
                count += 1
                self.gems[i] = ELEMENT_NONE
            else:
                break
        self.show_gems(gem, count)
        return gem, count

    def shift_gems(self):
        self.show_gems()
        for i in range(GEMS_LENGTH - 1):
            while self.gems[i] == ELEMENT_NONE:
                if self.gems[i:] == [ELEMENT_NONE] * (GEMS_LENGTH - i):
                    break
                gem = self.gems.pop(i)
                self.gems.append(gem)
                self.show_gems()

    def spawn_gems(self):
        on_spawn = False
        for i in range(len(self.gems)):
            if self.gems[i] == ELEMENT_NONE:
                self.gems[i] = self.fill_gems(1)[0]
                on_spawn = True
        if on_spawn:
            self.show_gems()

    def get_friend_by_element(self, element):
        friends = [friend for friend in self.friends if friend.element == element]
        if len(friends) > 0:
            return friends[0]

# data
enemys = [
        Monster('スライム',    100, '水', 10,  1),
        Monster('ゴブリン',    200, '土', 20,  5),
        Monster('オオコウモリ',300, '風', 30, 10),
        Monster('ウェアウルフ',400, '風', 40, 15),
        Monster('ドラゴン',    600, '火', 50, 20),
        ]

friends = [
        Monster('朱雀', 150, '火', 30, 10),
        Monster('青龍', 150, '風', 20, 10),
        Monster('白虎', 150, '土', 25,  5),
        Monster('玄武', 150, '水', 25, 15),
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

def organize_party(player_name, friends):
    return Party(player_name, friends)

def on_player_turn(party, enemy):
    print(f'\n【{party.name}のターン】(HP={party.hp})')
    show_battle_field(party, enemy)
    command = input_command()
    before = command[0:1].upper()
    after = command[-1:].upper()
    beforeIndex = ord(before) - 65 
    afterIndex = ord(after) - 65
    party.move_gem(beforeIndex, afterIndex)
   
    evaluate_gems(party, enemy)
            
def evaluate_gems(party, enemy):
    combo = 0
    while True:     
        while True: 
            index = party.check_banishable()
            if index < 0:
                break

            gem, count = party.banish_gems(index)

            if gem == ELEMENT_LIFE:
                do_recover(party, count, combo)
            else:
                friend = party.get_friend_by_element(gem)
                if friend is not None:
                    combo += 1
                    has_banished = True
                    do_attack(friend, enemy, count, combo)
            party.shift_gems()

        if ELEMENT_NONE in party.gems:
            party.spawn_gems()
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

def do_attack(friend, enemy, count, combo):
    element_boost = get_element_boost(friend.element, enemy.element)
    combo_boost = get_combo_boost(count, combo)

    damage = max(1, friend.ap - enemy.dp) * element_boost * combo_boost
    damage = blur_damage(damage)
    
    friend.print_name()
    print(f'の攻撃！{f' {combo} Commbo!!' if combo > 1 else ''}')
    enemy.print_name()
    print(f'に{damage}のダメージを与えた')
    enemy.hp = max(0, enemy.hp - damage)

def do_recover(party, count, combo):
    combo_boost = get_combo_boost(count, combo)
    heal = 20 * combo_boost
    heal = blur_damage(heal)
    heal = min(heal, party.max_hp - party.hp)
    print(f'{party.name}のHPは{heal}回復した')
    party.hp = party.hp + heal

def do_enemy_attack(party, enemy):
    damage = enemy.ap - party.dp
    damage = blur_damage(damage)
    print(f'{damage}のダメージを受けた')
    party.hp = max(0, party.hp - damage)

def get_element_boost(attack_element, defence_element):
    elements = list(ELEMENT_SYMBOLS.keys())[0:4]
    index = (elements.index(attack_element) + 4 - elements.index(defence_element)) % 4
    return ELEMENT_BOOST[index]

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
    party.show_gems()
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

def blur_damage(damage):
    return max(1, int(damage * (random.uniform(-0.1, 0.1) + 1)))

# start app
main()

