#! python
# coding:utf-8
# Author:VChao
# Date:2019/05/19

import random
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from puzzle import *
from search import *

class PuzzleGame(QMainWindow):
    def __init__(self):
        super(PuzzleGame, self).__init__()

        self.resize(300, 300)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

        self.container = Container(self)
        self.setCentralWidget(self.container)
        self.show()


class Container(QFrame):
    key_map = {
        'LEFT': 1,
        'RIGHT': 2,
        'DOWN': 3,
        'UP': 4
    }
    KEY2MAP = {
        Qt.Key_Left: key_map['LEFT'],
        Qt.Key_Right: key_map['RIGHT'],
        Qt.Key_Down: key_map['DOWN'],
        Qt.Key_Up: key_map['UP']
    }

    def __init__(self, parent):
        super(Container, self).__init__(parent)
        self.setFrameStyle(QFrame.StyledPanel)
        self.setFocusPolicy(Qt.StrongFocus)

        pos_list = [i for i in range(9)]
        random.shuffle(pos_list)
        #pos_list = [1, 2, 3, 0, 5, 6, 4, 7, 8]
        #pos_list = [1, 2, 3, 5, 6, 0, 4, 7, 8]
        self.puzzle_state = Puzzle(pos_list)

        self.pix_map = []
        self.lbl = []

        for i in range(9):
            self.pix_map.append(QPixmap("sources/num_" + str(i) + ".png"))
            self.lbl.append(QLabel(self))
            self.lbl[i].setPixmap(self.pix_map[i])
            self.lbl[i].setScaledContents(True)

        self.init_ui()

    def init_ui(self):
        puzzle_state = self.puzzle_state.get_states()

        for i in range(9):
            # python3 的整除问题
            # print(i, (i % 3) * 100,(i//3) * 100)
            self.lbl[puzzle_state[i]].setGeometry((i % 3) * 100, (i // 3) * 100, 100, 100)

    def move_pic(self, key):

        direction = self.KEY2MAP[key]
        self.puzzle_state.state_change_for_game(direction)
        self.init_ui()
        if self.puzzle_state.state_success():
            reply = QMessageBox.information(
                self,
                "成功",
                "成功达到目的状态，是否继续游戏",
                QMessageBox.Yes | QMessageBox.No
            )

    def keyPressEvent(self, event):
        key = event.key()
        if key in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Down, Qt.Key_Up]:
            self.move_pic(key)
        elif key == Qt.Key_Q:
            try:
                print(get_move_sequence(self.puzzle_state))
            except Exception as e:
                print(e)


def main():
    app = QApplication([])
    launch_game = PuzzleGame()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
