#! python
# coding:utf-8
# Author:VChao
# Date: 2019/05/19

import copy
import random

key_map = {
    'LEFT': 1,
    'RIGHT': 2,
    'DOWN': 3,
    'UP': 4
}


class Puzzle(object):


    def __init__(self, pos_list = None):
        # deepcopy 非常耗时
        # self.pos_list = copy.deepcopy(pos_list)
        if pos_list is None:
            pos_list = [i for i in range(9)]
            random.shuffle(pos_list)

        self.pos_list = pos_list[:]
        self.goal = [1, 2, 3, 4, 5, 6, 7, 8, 0]

        # self.goal.append(0)

    def __eq__(self, other):
        if other.pos_list == self.pos_list:
            return True
        else:
            return False

    def __str__(self):
        return str(self.pos_list)

    def get_states(self):
        return self.pos_list

    def get_actions(self):
        pos_0 = self.pos_list.index(0)

        pos_map = {
            0: [1, 4],
            1: [1, 2, 4],
            2: [2, 4],
            3: [1, 3, 4],
            4: [1, 2, 3, 4],
            5: [2, 3, 4],
            6: [1, 3],
            7: [1, 2, 3],
            8: [2, 3]
        }
        return pos_map[pos_0]

    def state_success(self):

        if self.pos_list == self.goal:
            return True
        else:
            return False

    @staticmethod
    def state_change_(pos_list, direction):

        pos_0 = pos_list.index(0)
        if direction == key_map['LEFT']:
            if (pos_0 + 1) % 3 != 0:
                pos_list[pos_0], pos_list[pos_0 + 1] = \
                    pos_list[pos_0 + 1], pos_list[pos_0]

        elif direction == key_map['RIGHT']:
            if pos_0 % 3 != 0:
                pos_list[pos_0], pos_list[pos_0 - 1] = \
                    pos_list[pos_0 - 1], pos_list[pos_0]

        elif direction == key_map['UP']:
            if pos_0 // 3 != 2:
                pos_list[pos_0], pos_list[pos_0 + 3] = \
                    pos_list[pos_0 + 3], pos_list[pos_0]

        elif direction == key_map['DOWN']:
            if pos_0 // 3 != 0:
                pos_list[pos_0], pos_list[pos_0 - 3] = \
                    pos_list[pos_0 - 3], pos_list[pos_0]
        return pos_list

    def state_change_for_game(self, direction):
        self.state_change_(self.pos_list, direction)

    def state_change(self, direction):
        pos_list = self.pos_list[:]
        return Puzzle(self.state_change_(pos_list, direction))


if __name__ == "__main__":
    print(Puzzle([i for i in range(9)]).state_success())
