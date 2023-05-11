import sys
import random
from PyQt5.QtWidgets import QMainWindow, QFrame, QLabel, QApplication
from PyQt5.QtCore import Qt, QBasicTimer
from PyQt5.QtGui import QPainter, QColor


class Tetris(QMainWindow):
    def __init__(self, main):
        super().__init__()
        self.tboard = None
        self.main = main
        self.initUI()

    def initUI(self):
        self.setFixedSize(360, 760)
        self.setWindowTitle(self.main.name_row.text())
        self.show()
        self.tboard = Board(self, self.main)
        self.setCentralWidget(self.tboard)


class Board(QFrame):
    BoardWidth = 10
    BoardHeight = 22
    Speed = 300

    def __init__(self, parent, main):
        super().__init__(parent)
        self.main = main
        self.score = 0
        self.score_label = QLabel(self)
        self.score_label.setGeometry(0, 0, 200, 10)
        self.score_label.setText(str(self.score))
        self.initBoard()


    def initBoard(self):
        self.timer = QBasicTimer()
        self.isWaitingAfterLine = False

        self.curX = 0
        self.curY = 0
        self.numLinesRemoved = 0
        self.board = []

        self.setFocusPolicy(Qt.StrongFocus)
        self.isStarted = False
        self.isPaused = False

    def shapeAt(self, x, y):
        return self.board[(y * Board.BoardWidth) + x]

    def setShapeAt(self, x, y, shape):
       self.board[(y * Board.BoardWidth) + x] = shape

    def squareWidth(self):
        return self.contentsRect().width() // Board.BoardWidth

    def squareHeight(self):
        return self.contentsRect().height() // Board.BoardHeight

    # def paintEvent(self, event):
    #     painter = QPainter(self)
    #     rect = self.contentsRect()
    #
    #     boardTop = rect.bottom() - Board.BoardHeight * self.squareHeight()
    #
    #     for i in range(Board.BoardHeight):
    #         for j in range(Board.BoardWidth):
    #             shape = self.shapeAt(j, Board.BoardHeight - i - 1)
    #
    #             if shape != Tetrominoe.NoShape:
    #                 self.drawSquare(painter,
    #                                 rect.left() + j * self.squareWidth(),
    #                                 boardTop + i * self.squareHeight(), shape)
    #
    #     if self.curPiece.shape() != Tetrominoe.NoShape:
    #
    #         for i in range(4):
    #             x = self.curX + self.curPiece.x(i)
    #             y = self.curY - self.curPiece.y(i)
    #             self.drawSquare(painter, rect.left() + x * self.squareWidth(),
    #                             boardTop + (Board.BoardHeight - y - 1) * self.squareHeight(),
    #                             self.curPiece.shape())

    def keyPressEvent(self, event):
        if not self.isStarted or self.curPiece.shape() == Tetrominoe.NoShape:
            super(Board, self).keyPressEvent(event)
            return
        key = event.key()
        if key == Qt.Key_P:
            self.pause()
            return
        if self.isPaused:
            return
        elif key == Qt.Key_Left:
            self.tryMove(self.curPiece, self.curX - 1, self.curY)
        elif key == Qt.Key_Right:
            self.tryMove(self.curPiece, self.curX + 1, self.curY)
        elif key == Qt.Key_Down:
            self.tryMove(self.curPiece.rotateRight(), self.curX, self.curY)
        elif key == Qt.Key_Up:
            self.tryMove(self.curPiece.rotateLeft(), self.curX, self.curY)
        elif key == Qt.Key_Space:
            self.dropDown()

        elif key == Qt.Key_D:
            self.oneLineDown()

        else:
            super(Board, self).keyPressEvent(event)


class Tetrominoe(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7


if __name__ == '__main__':
    app = QApplication([])
    tetris = Tetris("Tetris")
    sys.exit(app.exec_())
