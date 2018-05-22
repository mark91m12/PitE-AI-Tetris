import random
import sys

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Shape import Shape
from Shape import Tetrominoe
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor

class NextBoard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setPalette(QPalette(Qt.white))  
        self.setAutoFillBackground(True)  
        self.curPiece = Shape()
        self.shape = 1
        self.BoardWidth = 3.5
        self.BoardHeight = 6

    def display(self, msg):
        self.shape = msg
        self.update()

    def squareWidth(self):
        return self.contentsRect().width() // self.BoardWidth

    def squareHeight(self):
        return self.contentsRect().height() // self.BoardHeight

    def paintEvent(self, event):
        painter = QPainter(self)
        rect = self.contentsRect()
        boardTop = rect.bottom() - self.BoardHeight * self.squareHeight()
        for i in range(4):
            x = 1 + self.curPiece.x(i)
            y = 1 + self.curPiece.y(i)

            self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                            boardTop + (self.BoardHeight - y - 1) * self.squareHeight(),
                            self.shape)

    def drawSquare(self, painter, x, y, shape):
        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[int(shape)])
        painter.fillRect(x + 1, y + 1, self.squareWidth() - 2,
                         self.squareHeight() - 2, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + self.squareHeight() - 1, x, y)
        painter.drawLine(x, y, x + self.squareWidth() - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + self.squareHeight() - 1,
                         x + self.squareWidth() - 1, y + self.squareHeight() - 1)
        painter.drawLine(x + self.squareWidth() - 1,
                         y + self.squareHeight() - 1, x + self.squareWidth() - 1, y + 1)
