from Pieces.BaseFigure import BaseFigure


class Bishop(BaseFigure):
    def __init__(self, row, col, color):
        super(Bishop, self).__init__(row, col, color)

    def can_move(self, board, row1, col1):
        if abs(self.row - row1) == abs(self.col - col1):
            step_x = 1 if self.row < row1 else -1
            step_y = 1 if self.col < col1 else -1
            if all(i is None for i in [board.field[x][y]
                                       for x, y in
                                       zip(range(self.row + step_x, row1, step_x),
                                           range(self.col + step_y, col1, step_y))]):
                return True
        return False
