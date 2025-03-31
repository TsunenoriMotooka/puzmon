import random
from const import *

class Gems:
    def __init__(self):
        self.gems = self.fill(GEMS_LENGTH)

    def fill(self, count):
        gems = [random.choice(list(ELEMENT_SYMBOLS.keys())[0:-1]) for i in range(count)]
        return gems

    def show(self, banish_element=None, banish_count=0):
        for i, element in enumerate(self.gems, 0):
            print(f'{' ' if i > 0 else ''}', end='')
            self.print_gem(element)

        if banish_element is not None:
            print('  ', end='')
            self.print_gem(banish_element)
            print(f'x{banish_count}', end='')

        print()

    def print_gem(self, element):
        color  = '4' + ELEMENT_COLORS[element]
        print(f'\033[{color}m\033[30m{ELEMENT_SYMBOLS[element]}\033[0m', end='')

    def move(self, beforeIndex, afterIndex, output=True):
        if beforeIndex < 0 or beforeIndex >= len(self.gems):
            return
        if afterIndex < 0 or afterIndex >= len(self.gems):
            return

        step = 1 if beforeIndex < afterIndex else -1 
        [self.swap(i, step, output) for i in range(beforeIndex, afterIndex, step)]

    def swap(self, index, step, output=True): 
        if index < 0 or index + step < 0 or index >= len(self.gems) or index + step >= len(self.gems):
            return

        temp = self.gems[index + step]
        self.gems[index + step] = self.gems[index]
        self.gems[index] = temp

        if output:
            self.show()
    
    def check_banishable(self):
        for i in range(GEMS_LENGTH - 2):
            banish_list = {i}
            element = self.gems[i]
            if element == ELEMENT_NONE:
                continue

            for j in range(i + 1, GEMS_LENGTH):
                if element == self.gems[j]:
                    banish_list.add(j)
                else:
                    break
            if len(banish_list) >=3:
                return (element, banish_list)
        return (None, None)

    def banish(self):
        banish_element, banish_list = self.check_banishable()
        if len(banish_list) > 0:
            for i in banish_list:
                self.gems[i] = ELEMENT_NONE
            self.show(banish_element, len(banish_list))

    def shift(self):
        self.show()
        for i in range(len(self.gems)):
            while self.gems[i] == ELEMENT_NONE:
                if self.gems[i:] == [ELEMENT_NONE] * (len(self.gems) - i):
                    break

                gem = self.gems.pop(i)
                self.gems.append(gem)
                self.show()

    def spawn(self):
        on_spawn = False
        for i in range(len(self.gems)):
            if self.gems[i] == ELEMENT_NONE:
                self.gems[i] = self.fill(1)[0]
                on_spawn = True
        if on_spawn:
            self.show()

