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

        self.pix_map = []
        self.lbl = []
        self.init_label()

        self.puzzle_state = None
        self.init_puzzle_state()
        self.solution = []
        self.init_ui()

    def init_puzzle_state(self):
        self.puzzle_state = Puzzle()

    def init_label(self):
        for i in range(9):
            self.pix_map.append(QPixmap("sources/num_" + str(i) + ".png"))
            self.lbl.append(QLabel(self))
            self.lbl[i].setPixmap(self.pix_map[i])
            self.lbl[i].setScaledContents(True)

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
                "成功达到目的状态，是否继续游戏?",
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.init_puzzle_state()
                self.init_ui()

    def keyPressEvent(self, event):
        key = event.key()
        if key in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Down, Qt.Key_Up]:
            self.move_pic(key)
        elif key == Qt.Key_Q:
            try:
                self.solution = get_move_sequence(self.puzzle_state)
                if self.solution is None:
                    reply = QMessageBox.information(
                        self,
                        "失败",
                        "该状态无法完成最终目标，是否重置棋盘?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    if reply == QMessageBox.Yes:
                        self.init_puzzle_state()
                        self.init_ui()
                else:
                    print(self.solution)


            except Exception as e:
                print(e)


def main():
    app = QApplication([])
    launch_game = PuzzleGame()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
