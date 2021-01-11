from Pieces.Rook import Rook
from Pieces.BaseFigure import BaseFigure


class King(BaseFigure):
    def __init__(self, row, col, color):
        super(King, self).__init__(row, col, color)
        self.castling = False

    def set_position(self, row1, col1):
        self.row, self.col, self.castling = row1, col1, True

    def can_move(self, board, row1, col1):
        if 1 <= (self.row - row1) ** 2 + (self.col - col1) ** 2 <= 2:
            x, y = self.row, self.col
            piece = board.field[row1][col1]
            board.field[self.row][self.col] = None
            board.field[row1][col1] = self
            if not self.king_is_under_attack(board, row1, col1):
                board.field[x][y] = self
                board.field[row1][col1] = piece
                if board.field[row1][col1] is None:
                    return True
                elif board.field[row1][col1].get_color() != self.color:
                    return True
            board.field[x][y] = self
            board.field[row1][col1] = piece
            return False
        return False

    def king_is_under_attack(self, board, row, col):
        figures = []
        for i in range(len(board.field)):
            for j in range(len(board.field[0])):
                piece = board.field[i][j]
                if piece is not None:
                    if piece.get_color() != self.color:
                        figures.append(piece)
        for p in figures:
            if p.can_move(board, row, col):
                return True
        return False

    def make_castling(self, board, col, col1):
        if not self.castling:
            rook = board.field[self.row][self.col + 3] \
                if col < col1 else board.field[self.row][self.col - 4]
            if isinstance(rook, Rook):
                if not rook.castling:
                    s = 1 if col < col1 else -1
                    if all(i is None for i in [board.field[self.row][j]
                                               for j in range(col + s, rook.col, s)]):
                        if all(not self.king_is_under_attack(board, self.row, j)
                               for j in range(col, rook.col, s)):
                            return True
                        return False
                    return False
                return False
            return False
        return False
