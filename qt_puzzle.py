#! python
# coding:utf-8
# Author:VChao
# Date:2019/05/19

import random
import sys
import traceback
import time

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
        self.auto_timer = QBasicTimer()
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

    def move_pic_by_direction(self, direction):

        self.puzzle_state.state_change_for_game(direction)

        print(self.puzzle_state)
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
                    reply = QMessageBox.information(
                        self,
                        "提示",
                        "已完成动作搜索，是否进行自动化运行?",
                        QMessageBox.Yes | QMessageBox.No
                    )
                    print("Solution:",self.solution)
                    if reply == QMessageBox.Yes:
                        # 这里尝试了直接在函数中进行动作的转换，但是利用循环的方法导致没有从这个函数中走出来
                        # 影响了底层的GUI绘图机制
                        # 所以最好的办法，估计还是利用定时器的方法
                        self.auto_timer.start(150,self)


            except Exception:
                traceback.print_exc()

    def timerEvent(self, event):
        if event.timerId() == self.auto_timer.timerId():
            try:
                if len(self.solution) > 0:
                    direction = self.solution.pop(0)
                    self.move_pic_by_direction(direction)
                else:
                    self.auto_timer.stop()
            except TypeError:
                # 如果现在的状态已经是成功的，搜素返回值是0，引发类型错误
                self.auto_timer.stop()
            except Exception:
                traceback.print_exc()



def main():
    app = QApplication([])
    launch_game = PuzzleGame()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
