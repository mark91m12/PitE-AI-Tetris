import random
import sys
from Shape import Shape
from Shape import Tetrominoe
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor
from py4j.java_gateway import JavaGateway, GatewayParameters
from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtGui
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from Tetris import *

gateway = JavaGateway(gateway_parameters=GatewayParameters(port=25335))

dlv = gateway.entry_point.getData()


class Board(QMainWindow):
    msg2Level = pyqtSignal(object)
    msg2Score = pyqtSignal(object)
    msg2State = pyqtSignal(object)
    msg2NextBoard = pyqtSignal(object)
    BoardWidth = 10
    BoardHeight = 22
    
 
    def __init__(self,mode):
        super().__init__()
        self.setStyleSheet("QMainWindow {background-image: url(../../data/border_part.png); border: 2px solid rgb(251, 226, 19); border-radius: 3px;}")
        self.setPalette(QPalette(Qt.white))
        self.setAutoFillBackground(True)
        self.setMinimumSize(300, 600)
        self.curPiece = Shape()
        self.curPiece.setRandomShape()
        self.nextCurPiece = Shape()
        self.nextCurPiece.setRandomShape()
        self.initBoard()
        self.mode = mode
        if mode == "n":
           self.Speed = 70 
           self.level = 0
           self.counter = 0
           self.msg2Level.emit(str(self.level))
        elif mode == "f":
           self.Speed = 5 
           self.level = 5
           self.counter = 0
           self.msg2Level.emit(str(self.level))
        self.start()
        self.newPiece()
        self.player_main_music = QMediaPlayer()
        self.player_main_fast = QMediaPlayer()
        self.player_delete1row = QMediaPlayer()
        self.player_delete4row = QMediaPlayer()
        self.player_pause_sound = QMediaPlayer()
        self.playlist_main = QMediaPlaylist()
        if mode == "n":
            self.start_main_music()
        elif mode == "f":
            self.start_main_music_fast()
                  
                
               
    def initBoard(self):
        '''initiates board'''

        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.top_board = 0
        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False
        self.clearBoard()
        
        quit = QAction("Quit", self)
        quit.triggered.connect(self.close)

    def shapeAt(self, x, y):
        '''determines shape at the board position'''

        return self.board[(y * self.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
        '''sets a shape at the board'''

        self.board[(y * self.BoardWidth) + x] = shape

    def squareWidth(self):
        '''returns the width of one square'''

        return self.contentsRect().width() // self.BoardWidth

    def squareHeight(self):
        '''returns the height of one square'''

        return self.contentsRect().height() // self.BoardHeight

    def start(self):
        '''starts game'''

        if self.isPaused:
            return

        self.isStarted = True
        self.isWaitingAfterLine = False
        self.numLinesRemoved = 0
        self.clearBoard()

        self.newPiece()
        self.timer.start(self.Speed, self)
        

    def pause(self):
        '''pauses game'''
        
        if not self.isStarted:
            return

        self.isPaused = not self.isPaused

        if self.isPaused:
            self.timer.stop()
            
        else:
            self.timer.start(self.Speed, self)
           
        self.update()

    def paintEvent(self, event):
        '''paints all shapes of the game'''

        painter = QPainter(self)
        rect = self.contentsRect()

        boardTop = rect.bottom() - self.BoardHeight * self.squareHeight()

        for i in range(self.BoardHeight):
            for j in range(self.BoardWidth):
                shape = self.shapeAt(j, self.BoardHeight - i - 1)

                if shape != Tetrominoe.NoShape:
                    self.drawSquare(painter,
                                    rect.left() + j * self.squareWidth(),
                                    boardTop + i * self.squareHeight(), shape)

        if self.curPiece.shape() != Tetrominoe.NoShape:

            for i in range(4):
                x = self.curX + self.curPiece.x(i)
                y = self.curY - self.curPiece.y(i)
                self.drawSquare(painter, rect.left() + x * self.squareWidth(),
                                boardTop + (self.BoardHeight - y - 1) * self.squareHeight(),
                                self.curPiece.shape())

    def keyPressEvent(self, event):
        '''processes key press events'''

        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)
            return
        key = event.key()

        if self.isPaused:
            return
        else:
            super(Board, self).keyPressEvent(event)

    def timerEvent(self, event):
        '''handles timer event'''

        if event.timerId() == self.timer.timerId():

            if self.isWaitingAfterLine:
                self.isWaitingAfterLine = False
                self.newPiece()
            else:
                self.oneLineDown()
                
                if self.mode == "n" :
                      
     
                    x = int(dlv.getX())
                    
                    if self.curY <= 18:
                        self.rotatePiece(int(dlv.getRotation()))
    
                    if x < self.curX :
                        self.tryMove(self.curPiece, self.curX - 1, self.curY)
                    elif x > self.curX :
                        self.tryMove(self.curPiece, self.curX + 1, self.curY)

                 
    def clearBoard(self):
        '''clears shapes from the board'''

        for i in range(self.BoardHeight * self.BoardWidth):
            self.board.append(Tetrominoe.NoShape)

    def oneLineDown(self):
        '''goes one line down with a shape'''

        if not self.tryMove(self.curPiece, self.curX, self.curY - 1):
            self.pieceDropped()

    def pieceDropped(self):
        '''after dropping shape, remove full lines and create new shape'''

        for i in range(4):
            x = self.curX + self.curPiece.x(i)
            y = self.curY - self.curPiece.y(i)
            self.setShapeAt(x, y, self.curPiece.shape())

        self.removeFullLines()

        if not self.isWaitingAfterLine:
            self.newPiece()

    def removeFullLines(self):
        '''removes all full lines from the board'''

        numFullLines = 0
        rowsToRemove = []

        for i in range(self.BoardHeight):

            n = 0
            for j in range(self.BoardWidth):
                if not self.shapeAt(j, i) == Tetrominoe.NoShape:
                    n = n + 1

            if n == 10:
                rowsToRemove.append(i)

        rowsToRemove.reverse()

        for m in rowsToRemove:

            for k in range(m, self.BoardHeight):
                for l in range(self.BoardWidth):
                    self.setShapeAt(l, k, self.shapeAt(l, k + 1))

        if  len(rowsToRemove) == 4:
            self.start_delete_4_row()
        elif 0< len(rowsToRemove) < 4:
            self.start_delete_1_row()
        
        
        numFullLines = numFullLines + len(rowsToRemove)

        if numFullLines > 0:
            
            self.counter = self.counter + numFullLines
            
            if self.level != 5:
                
                if self.counter >= 4 :
                    self.counter -= 4 
                    self.level +=1
                    self.msg2Level.emit(str(self.level))
                    self.Speed = self.Speed - 10
                    print("current speed : ",self.Speed)
                    self.timer.start(self.Speed,self)
           
            self.numLinesRemoved = self.numLinesRemoved + numFullLines
            self.msg2Score.emit(str(self.numLinesRemoved))

            self.isWaitingAfterLine = True
            self.curPiece.setShape(Tetrominoe.NoShape)
            self.update()
            
    def endGame(self):
        self.curPiece.setShape(Tetrominoe.NoShape)
        self.timer.stop()
        self.isStarted = False
        

    def newPiece(self):
        '''creates a new shape'''
        self.curPiece = Shape()
        self.curPiece.setRandomShape()
       
        self.tempCurPiece = Shape()
        self.tempCurPiece = self.nextCurPiece
        self.nextCurPiece = self.curPiece
        self.curPiece = self.tempCurPiece
        self.msg2NextBoard.emit(str(self.nextCurPiece.nextNum))
       
       
        self.curPiece.set_congif(1)

        if self.mode == "n":
            self.curX = self.BoardWidth // 2                    
            self.skynet(self.curPiece.shape())
        else :
            self.skynet(self.curPiece.shape())
            self.rotatePiece(int(dlv.getRotation()))
            self.curX = int(dlv.getX())
           
        self.curY = self.BoardHeight - 1 + self.curPiece.minY()


        if not self.tryMove(self.curPiece, self.curX, self.curY):
            self.endGame()
            self.msg2State.emit(str("LOSE"))
            self.start_lose_sound()
       
            
   
            

    def skynet(self, shape):
        file_input = open("../../AI/input.dl", "w")
        file_input.write(
            "place(F,X,Y,C) v notPlace(F,X,Y,C) :- shape(F,_,_,C),cell(X,Y), X<=" + str(self.top_board + 4) + ".")
        
        file_optimize = open("../../AI/optimize.dl","w")
 
        if self.top_board >= 7 :
            file_optimize.write(":~emptyRow(X,Y). [1:1] \n"
                                +":~smallest(X,Y,F,C),empty(X1,Y), X1=X-1 . [1:2]\n"
                                +":~occupiedRow(R). [1:3]\n"
                                +":~notFullRow(R). [1:4]\n")
        else :
            file_optimize.write(":~emptyRow(X,Y). [1:1] \n"
                                +":~smallest(X,Y,F,C),empty(X1,Y), X1=X-1 . [1:4]\n"
                                +":~occupiedRow(R). [1:2]\n"
                                +":~notFullRow(R). [1:3]\n")
            
        file_optimize.close()
        
        
        self.top_board = 0

        file_board_configuration = open("../../AI/config.dl", "w")

        if shape == Tetrominoe.ZShape:
            file_input.write("shape(z,2,2,1). shape(z,3,2,1). shape(z,2,1,1). shape(z,1,1,1)."
                             + "shape(z,2,2,2). shape(z,3,2,2). shape(z,3,1,2). shape(z,2,3,2). "
                             + "shape(z,2,2,3). shape(z,2,3,3). shape(z,1,2,3). shape(z,3,3,3). "
                             + "shape(z,2,2,4). shape(z,1,2,4). shape(z,1,3,4). shape(z,2,1,4).")
        elif shape == Tetrominoe.TShape:
            file_input.write("shape(t,2,2,1). shape(t,2,1,1). shape(t,2,3,1). shape(t,3,2,1)."
                             + "shape(t,2,2,2). shape(t,2,3,2). shape(t,1,2,2). shape(t,3,2,2). "
                             + "shape(t,2,2,3). shape(t,2,1,3). shape(t,2,3,3). shape(t,1,2,3). "
                             + "shape(t,2,2,4). shape(t,1,2,4). shape(t,3,2,4). shape(t,2,1,4).")
        elif shape == Tetrominoe.LShape:
            file_input.write("shape(l,2,2,1). shape(l,2,1,1). shape(l,1,2,1). shape(l,0,2,1)."
                             + "shape(l,2,2,2). shape(l,2,1,2). shape(l,2,0,2). shape(l,3,2,2). "
                             + "shape(l,2,2,3). shape(l,2,3,3). shape(l,3,2,3). shape(l,4,2,3)."
                             + "shape(l,2,2,4). shape(l,2,3,4). shape(l,2,4,4). shape(l,1,2,4).")
        elif shape == Tetrominoe.MirroredLShape:
            file_input.write("shape(j,2,2,1). shape(j,2,3,1). shape(j,1,2,1). shape(j,0,2,1)."
                             + "shape(j,2,2,2). shape(j,2,1,2). shape(j,2,0,2). shape(j,1,2,2). "
                             + "shape(j,2,2,3). shape(j,2,1,3). shape(j,3,2,3). shape(j,4,2,3). "
                             + "shape(j,2,2,4). shape(j,2,3,4). shape(j,2,4,4). shape(j,3,2,4).")
        elif shape == Tetrominoe.SquareShape:
            file_input.write("shape(o,2,2,1). shape(o,2,3,1). shape(o,3,2,1). shape(o,3,3,1).")
        elif shape == Tetrominoe.LineShape:
            file_input.write("shape(i,2,2,1). shape(i,3,2,1). shape(i,1,2,1). shape(i,0,2,1)."
                             + "shape(i,2,2,2). shape(i,2,3,2). shape(i,2,1,2). shape(i,2,0,2).")
        elif shape == Tetrominoe.SShape:
            file_input.write(" shape(s,2,2,1). shape(s,3,2,1). shape(s,2,3,1). shape(s,1,3,1)."
                             + "shape(s,2,2,2). shape(s,1,1,2). shape(s,1,2,2). shape(s,2,3,2). "
                             + "shape(s,2,2,3). shape(s,1,2,3). shape(s,2,1,3). shape(s,3,1,3). "
                             + "shape(s,2,2,4). shape(s,2,1,4). shape(s,3,2,4). shape(s,3,3,4).")

        file_input.close()

        # write board config
        for i in range(self.BoardWidth):
            for j in range(self.BoardHeight):
                if self.shapeAt(i, j) != Tetrominoe.NoShape:
                    if j > self.top_board:
                        self.top_board = j;
                    file_board_configuration.write("occupied1(" + str(j) + "," + str(i) + ",shape).");

        file_board_configuration.close()
        dlv.reset()
        dlv.runAI()

    def tryMove(self, newPiece, newX, newY):
        '''tries to move a shape'''

        for i in range(4):

            x = newX + newPiece.x(i)
            y = newY - newPiece.y(i)

            if x < 0 or x >= self.BoardWidth or y < 0 or y >= self.BoardHeight:
                return False

            if self.shapeAt(x, y) != Tetrominoe.NoShape:
                return False

        self.curPiece = newPiece
        self.curX = newX
        self.curY = newY
        self.update()

        return True

    def rotatePiece(self, new_position):

        num_rotation = new_position - self.curPiece.get_congif()

        i = 0
        while (i < num_rotation):
            self.curPiece = self.curPiece.rotateLeft();
            i += 1
        
        self.curPiece.set_congif(new_position)

    def drawSquare(self, painter, x, y, shape):
        '''draws a square of a shape'''

        colorTable = [0x000000, 0xCC6666, 0x66CC66, 0x6666CC,
                      0xCCCC66, 0xCC66CC, 0x66CCCC, 0xDAAA00]

        color = QColor(colorTable[shape])
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
                
    
    
           
    def start_main_music(self):
        version = random.randint(1,2)
        url = "../../data/sound/tetris_"+str(version)+".mp3"
        self.url_main = QUrl.fromLocalFile(url)
        self.playlist_main.addMedia(QMediaContent(self.url_main))
        self.playlist_main.setPlaybackMode(QMediaPlaylist.Loop)
        self.player_main_music.setPlaylist(self.playlist_main)
        self.player_main_music.play()    
    
    def start_main_music_fast(self):
        version = random.randint(1,2)
        url = "../../data/sound/soundtrack_frenzy.mp3"
        self.url_main = QUrl.fromLocalFile(url)
        self.playlist_main.addMedia(QMediaContent(self.url_main))
        self.playlist_main.setPlaybackMode(QMediaPlaylist.Loop)
        self.player_main_music.setPlaylist(self.playlist_main)
        self.player_main_music.play()
    
    def stop_main_music(self):
        self.player_main_music.stop()
    
    def pause_main_music(self):
        self.player_main_music.pause()
    
    def restart_main_music(self):
        self.player_main_music.play()
    
    
    def start_lose_sound(self):
        self.playlist = QMediaPlaylist()
        self.url = QUrl.fromLocalFile("../../data/sound/lose.mp3")
        self.playlist.addMedia(QMediaContent(self.url))
        self.player_main_music.setPlaylist(self.playlist)
        self.player_main_music.play()
        
    def start_pause_sound(self):
        self.playlistPause = QMediaPlaylist()
        self.url = QUrl.fromLocalFile("../../data/sound/pause.mp3")
        self.playlistPause.addMedia(QMediaContent(self.url))
        self.player_pause_sound.setPlaylist(self.playlistPause)
        self.player_pause_sound.play()    

    def start_delete_1_row(self):
        self.playlist1Row = QMediaPlaylist()
        self.url2 = QUrl.fromLocalFile("../../data/sound/line-remove.mp3")
        self.playlist1Row.addMedia(QMediaContent(self.url2))
        self.player_delete1row.setPlaylist(self.playlist1Row)
        self.player_delete1row.play()
    
    def start_delete_4_row(self):
        self.playlist4Row = QMediaPlaylist()
        self.url1 = QUrl.fromLocalFile("../../data/sound/line-removal4.mp3")
        self.playlist4Row.addMedia(QMediaContent(self.url1))
        self.player_delete4row.setPlaylist(self.playlist4Row)
        self.player_delete4row.play()