from Pieces.BaseFigure import BaseFigure


class Pawn(BaseFigure):
    def __init__(self, row, col, color):
        super(Pawn, self).__init__(row, col, color)

    def can_move(self, board, row1, col1):
        if self.col != col1:
            return False
        if ((self.row == 6 and row1 == 4) or (self.row == 1 and row1 == 3)) \
                and board.field[row1][col1] is None:
            return True
        if self.color == 'Black':
            if self.row - row1 == -1 and board.field[row1][col1] is None:
                return True
        else:
            if self.row - row1 == 1 and board.field[row1][col1] is None:
                return True
        return False

    def can_attack(self, board, row1, col1):
        piece = board.field[row1][col1]
        if piece is not None:
            if piece.get_color() != self.color:
                if self.color == 'Black':
                    if self.row - row1 == -1 and abs(self.col - col1) == 1:
                        return True
                else:
                    if self.row - row1 == 1 and abs(self.col - col1) == 1:
                        return True
        return False
