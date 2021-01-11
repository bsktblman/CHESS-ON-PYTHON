from Pieces.BaseFigure import BaseFigure


class Rook(BaseFigure):
    def __init__(self, row, col, color):
        super(Rook, self).__init__(row, col, color)
        self.castling = False

    def set_position(self, row1, col1):
        self.row, self.col, self.castling = row1, col1, True

    def can_move(self, board, row1, col1):
        if self.row == row1:
            s = 1 if self.col < col1 else -1
            if all(i is None for i in [board.field[row1][y] for y in range(self.col + s, col1, s)]):
                return True
        elif self.col == col1:
            s = 1 if self.row < row1 else -1
            if all(i is None for i in [board.field[x][col1] for x in range(self.row + s, row1, s)]):
                return True
        return False
