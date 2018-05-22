import random

class Shape(object):

    def __init__(self):

        self.coords = [[0, 0] for i in range(4)]
        self.pieceShape = Tetrominoe.NoShape
        self.config=1
        self.setShape(Tetrominoe.NoShape)

    coordsTable = (
        ((0, 0), (0, 0), (0, 0), (0, 0)),
        ((0, 0), (0, -1), (-1, 0), (-1, 1)),
        ((0, -1), (0, 0), (1, 0), (1, 1)),
        ((0, 1), (0, 0), (0, -1), (0, 2)),
        ((-1, 0), (0, 0), (1, 0), (0, -1)),
        ((0, 0), (1, 0), (0, -1), (1, -1)),
        ((0, 0), (-1, 0), (0, 1), (0, 2)),
        ((0, 0), (1, 0), (0, 1), (0, 2))
    )
 
    def shape(self):
        '''returns shape'''

        return self.pieceShape

    def setShape(self, shape):
        '''sets a shape'''

        table = Shape.coordsTable[shape]

        for i in range(4):
            for j in range(2):
                self.coords[i][j] = table[i][j]

        self.pieceShape = shape

    def setRandomShape(self):
        '''chooses a random shape'''

        self.setShape(random.randint(1, 7))

    def x(self, index):
        '''returns x coordinate'''

        return self.coords[index][0]

    def y(self, index):
        '''returns y coordinate'''

        return self.coords[index][1]

    def setX(self, index, x):
        '''sets x coordinate'''

        self.coords[index][0] = x

    def setY(self, index, y):
        '''sets y coordinate'''

        self.coords[index][1] = y

    def minX(self):
        '''returns min x value'''

        m = self.coords[0][0]
        for i in range(4):
            m = min(m, self.coords[i][0])

        return m

    def maxX(self):
        '''returns max x value'''

        m = self.coords[0][0]
        for i in range(4):
            m = max(m, self.coords[i][0])

        return m

    def minY(self):
        '''returns min y value'''

        m = self.coords[0][1]
        for i in range(4):
            m = min(m, self.coords[i][1])

        return m

    def maxY(self):
        '''returns max y value'''

        m = self.coords[0][1]
        for i in range(4):
            m = max(m, self.coords[i][1])

        return m

    def rotateLeft(self):
        '''rotates shape to the left'''

        if self.pieceShape == Tetrominoe.SquareShape:
            return self

        result = Shape()
        result.pieceShape = self.pieceShape

        for i in range(4):
            result.setX(i, -self.y(i))
            result.setY(i, self.x(i))

        return result


class Tetrominoe(object):
    NoShape = 0
    ZShape = 1
    SShape = 2
    LineShape = 3
    TShape = 4
    SquareShape = 5
    LShape = 6
    MirroredLShape = 7
