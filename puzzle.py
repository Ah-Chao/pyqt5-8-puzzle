#! python
# coding:utf-8
# Author:VChao
# Date:2019/05/19

import sys
import random
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class PuzzleGame(QMainWindow):
    def __init__(self):
        super(PuzzleGame, self).__init__()

        self.resize(300, 300)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2, (screen.height()-size.height())/2)

        self.container = Container(self)
        self.setCentralWidget(self.container)
        self.show()


# 现在设想一下，我是想通过设置9个label来进行这个部分的内容
# 但是这个容器先是Frame


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

        self.pos_list = [i for i in range(9)]
        random.shuffle(self.pos_list)
        self.goal = [i for i in range(9)]
        self.pixmap = []
        self.lbl = []

        for i in range(9):
            self.pixmap.append(QPixmap("sources/num_" + str(i) + ".png"))
            self.lbl.append(QLabel(self))
            self.lbl[i].setPixmap(self.pixmap[i])
            self.lbl[i].setScaledContents(True)

        self.init_ui()

    def init_ui(self):

        for i in range(9):
            # python3 的整除问题
            # print(i, (i % 3) * 100,(i//3) * 100)
            self.lbl[self.pos_list[i]].setGeometry((i % 3) * 100, (i // 3) * 100,100,100)

    def move_pic(self,key):

        direction = self.KEY2MAP[key]
        pos_0 = self.pos_list.index(0)
        if direction == self.key_map['LEFT']:
            if (pos_0 + 1) % 3 == 0:
                return
            self.pos_list[pos_0], self.pos_list[pos_0 + 1] = \
                self.pos_list[pos_0 + 1],self.pos_list[pos_0]

        elif direction == self.key_map['RIGHT']:
            if pos_0 % 3 == 0:
                return
            self.pos_list[pos_0], self.pos_list[pos_0 - 1] = \
                self.pos_list[pos_0 - 1],self.pos_list[pos_0]
        elif direction == self.key_map['UP']:
            if pos_0 // 3 == 2:
                return
            self.pos_list[pos_0], self.pos_list[pos_0 + 3] = \
                self.pos_list[pos_0 + 3], self.pos_list[pos_0]
        elif direction == self.key_map['DOWN']:
            if pos_0 // 3 == 0:
                return
            self.pos_list[pos_0], self.pos_list[pos_0 - 3] = \
                self.pos_list[pos_0 - 3], self.pos_list[pos_0]
        print(self.pos_list)
        self.init_ui()
        if self.pos_list == self.goal:
            reply = QMessageBox.information(self,
                                            "成功",
                                            "成功达到目的状态，是否继续游戏",
                                            QMessageBox.Yes | QMessageBox.No)

    def keyPressEvent(self, event):
        key = event.key()
        if key in [Qt.Key_Left, Qt.Key_Right, Qt.Key_Down, Qt.Key_Up]:
            self.move_pic(key)


def main():
    app = QApplication([])
    launch_game = PuzzleGame()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
