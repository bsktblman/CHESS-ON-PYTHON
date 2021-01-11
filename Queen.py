from Pieces.BaseFigure import BaseFigure
from Pieces.Bishop import Bishop
from Pieces.Rook import Rook


class Queen(BaseFigure):
    def __init__(self, row, col, color):
        super(Queen, self).__init__(row, col, color)

    def can_move(self, board, row1, col1):
        return Rook(self.row, self.col, self.color).can_move(board, row1, col1) or \
               Bishop(self.row, self.col, self.color).can_move(board, row1, col1)

    def __str__(self):
        return self.color + ' queen'
    