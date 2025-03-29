import random
from const import *
from gems import Gems

class Party:
    def __init__(self, name, friends):
        self.name = name
        self.friends = friends
        self.hp = sum([friend.hp for friend in friends])
        self.max_hp = sum([friend.max_hp for friend in friends])
        self.dp = int(sum([friend.dp for friend in friends]) / len(friends))
        self.gems = Gems()

    def show(self):
        print(f'＜パーティ編成＞')
        print(f'{'-'*LINE_LENGTH}')
        for friend in self.friends:
            friend.print_name()
            print(f' HP= {friend.hp:3} 攻撃= {friend.ap:2} 防御= {friend.dp:2}')
        print(f'{'-'*LINE_LENGTH}\n')

    def get_friend_by_element(self, element):
        friends = [friend for friend in self.friends if friend.element == element]
        if len(friends) > 0:
            return friends[0]

