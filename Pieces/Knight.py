from Pieces.BaseFigure import BaseFigure


class Knight(BaseFigure):
    def __init__(self, row, col, color):
        super(Knight, self).__init__(row, col, color)

    def can_move(self, board, row1, col1):
        if (abs(self.col - col1) == 1 and abs(self.row - row1) == 2) \
                or (abs(self.col - col1) == 2 and abs(self.row - row1) == 1):
            return True
        return False

    def __str__(self):
        return 'Knight'
