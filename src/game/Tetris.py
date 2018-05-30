import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from NextBoard import NextBoard
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from Board import Board
from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *

class Tetris(QWidget):

    def __init__(self,mode,parent=None):
       super(Tetris, self).__init__(parent)

       self.initUI(mode)

    def initUI(self,mode):
        '''initiates application UI'''

        self.setWindowTitle("Skynet Tetris")
        self.setStyleSheet("QWidget {background: rgb(20,62,100);}")
        self.paused = False

        label1 = QLabel("Next：")
        label2 = QLabel("Level：")
        label3 = QLabel("Lines：")
        label4 = QLabel("State of Game: ")
        

        label1.setStyleSheet("QLabel { font: 20pt; color: rgb(0, 255, 0)}")
        label2.setStyleSheet("QLabel { font: 20pt; color: rgb(0, 255, 0)}")
        label3.setStyleSheet("QLabel { font: 20pt; color: rgb(0, 255, 0)}")
        label4.setStyleSheet("QLabel { font: 20pt; color: rgb(0, 255, 0)}")

        
        self.scoreLCD = QLCDNumber(10)
        self.scoreLCD.setSegmentStyle(QLCDNumber.Flat)
        self.scoreLCD.setStyleSheet("QWidget {background-image: url(../../data/border_part_4.png); color: rgb(253, 158, 52); border: 1px solid rgb(253, 158, 52); border-radius: 3px;}")
        
        
        self.levelLCD = QLCDNumber(10)
        self.levelLCD.setSegmentStyle(QLCDNumber.Flat)
        self.levelLCD.setStyleSheet("QWidget {background-image: url(../../data/border_part_4.png); color: rgb(253, 158, 52); border: 1px solid rgb(253, 158, 52); border-radius: 3px;}")
        
        self.state_of_gameLCD = QLCDNumber(10)
        self.state_of_gameLCD.setSegmentStyle(QLCDNumber.Flat)
        self.state_of_gameLCD.setWindowIconText("Play")
        self.state_of_gameLCD.setStyleSheet("QWidget {background-image: url(../../data/border_part_4.png); color: rgb(253, 158, 52); border: 1px solid rgb(253, 158, 52); border-radius: 3px;}")
        self.state_of_gameLCD.display("Play")
        
        
        
        self.PausePushButton = QPushButton("Pause")
        self.PausePushButton.setStyleSheet(" background-color: rgb(0, 255, 0); border: none;")
        

        self.board = Board(mode)
        self.stack2 = QStackedWidget()
        self.stack2.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.area2 = NextBoard()
        self.area2.display(self.board.nextCurPiece.nextNum)
        self.area2.curPiece = self.board.nextCurPiece
        self.stack2.addWidget(self.area2)
        self.stack2.setStyleSheet("QWidget {background-image: url(../../data/border_part_4.png); border: 1px solid rgb(253, 158, 52); border-radius: 3px;}")

        labelCol = 10
        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.setOpaqueResize(True)

        frame = QFrame(mainSplitter)

        mainLayout = QGridLayout(frame)
        mainLayout.setSpacing(3)

        mainLayout.addWidget(self.stack2,1,labelCol,2,2)  
        mainLayout.addWidget(label2, 3, labelCol, 1, 1)
        mainLayout.addWidget(self.levelLCD, 5, labelCol, 1, 1)
        mainLayout.addWidget(label3, 6, labelCol, 1, 1)
        mainLayout.addWidget(self.scoreLCD, 7, labelCol, 1, 1)
        mainLayout.addWidget(label4, 8, labelCol, 1, 1)
        mainLayout.addWidget(self.state_of_gameLCD, 9, labelCol, 1, 1)
        mainLayout.addWidget(self.PausePushButton, 10, labelCol, 1, 1)

        stack1 = QStackedWidget()
        stack1.setFrameStyle(QFrame.Panel | QFrame.Raised)

        stack1.addWidget(self.board)

        mainSplitter1 = QSplitter(Qt.Horizontal)
        mainSplitter1.setOpaqueResize(True)
        frame1 = QFrame(mainSplitter1)
        mainLayout1 = QVBoxLayout(frame1)
        mainLayout1.setSpacing(0)
        mainLayout1.addWidget(stack1)

        layout = QGridLayout(self)
        layout.addWidget(mainSplitter1, 0, 0)
        layout.addWidget(mainSplitter, 0, 1)
        self.setLayout(layout)


        self.PausePushButton.clicked.connect(self.slotPuse)
        self.board.msg2Level.connect(self.slotGetLevel)
        self.board.msg2Score.connect(self.slotGetScore)
        self.board.msg2State.connect(self.slotGetState)
        self.board.msg2NextBoard.connect(self.slotNextBoard)
        
        quit = QAction("Quit", self)
        quit.triggered.connect(self.close)
            
            
    def closeEvent(self, event):
        self.board.stop_main_music()
        self.board.endGame()

    
    def slotPuse(self, value):
        if self.paused == True:
            self.board.restart_main_music()
            self.board.pause()
            self.paused = False
            return
        else: 
            self.board.pause_main_music()
            self.board.start_pause_sound()
            self.board.pause()
            self.paused = True
            return

    def slotGetLevel(self, msg):
        #print("slotGetLevel = >" + msg)
        self.levelLCD.display(msg)

    def slotGetScore(self, msg):
        #print("slotGetScore = >" + msg)
        self.scoreLCD.display(msg)

    def slotGetState(self, msg):
        #print("slotGetState = >" + msg)
        self.state_of_gameLCD.display(msg)

    def slotNextBoard(self, msg):
        #print("slotNextBoard = >" + msg)
        self.area2.display(msg)
        self.area2.curPiece = self.board.nextCurPiece
        
  