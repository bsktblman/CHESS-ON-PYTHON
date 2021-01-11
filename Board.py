from Pieces.Bishop import Bishop
from Pieces.Knight import Knight
from Pieces.King import King
from Pieces.Rook import Rook
from Pieces.Pawn import Pawn
from Pieces.Queen import Queen


PIECES = {'Слон': Bishop, 'Конь': Knight, 'Ладья': Rook, 'Ферзь': Queen}


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


def opponent(color):
    return 'Black' if color == 'White' else 'White'


class Board:
    # создание поля
    def __init__(self):
        self.field = [[None] * 8 for _ in range(8)]
        self.white_king = King(7, 4, 'White')
        self.black_king = King(0, 4, 'Black')
        self.color = 'White'
        self.field[0] = [
            Rook(0, 0, 'Black'), Knight(0, 1, 'Black'), Bishop(0, 2, 'Black'), Queen(0, 3, 'Black'),
            self.black_king, Bishop(0, 5, 'Black'), Knight(0, 6, 'Black'), Rook(0, 7, 'Black')
        ]
        self.field[1] = [Pawn(1, i, 'Black') for i in range(8)]
        self.field[7] = [
            Rook(7, 0, 'White'), Knight(7, 1, 'White'), Bishop(7, 2, 'White'), Queen(7, 3, 'White'),
            self.white_king, Bishop(7, 5, 'White'), Knight(7, 6, 'White'), Rook(7, 7, 'White')
        ]
        self.field[6] = [Pawn(6, i, 'White') for i in range(8)]

    def get_piece(self, row, col):
        return self.field[row][col]

    def is_under_attack(self, row, col, color):
        return True if any(
            piece.can_move(self, row, col) and piece.get_color() == color for piece in
            [j for i in self.field for j in i if j is not None]) else False

    def move_piece(self, row, col, row1, col1):
        # Проверка на правильность координат
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        # Нельзя пойти в одну и ту же клетку
        if row == row1 and col == col1:
            return False
        piece = self.get_piece(row, col)
        # Проверка случая попытки хода из пустой клетки
        if piece is None:
            print('Пусто')
            return False
        # Проверка на цвет ходящего
        if self.color != piece.get_color():
            return False
        if self.field[row1][col1] is not None:
            if self.field[row1][col1].get_color() == self.color:
                return False

        if isinstance(piece, King) and row == row1 and abs(col - col1) == 2:
            if piece.make_castling(self, col, col1):
                self.field[row][col] = None
                self.field[row1][col1] = piece
                piece.set_position(row1, col1)
                rook = self.field[row][col + 3] if col < col1 else self.field[row][col - 4]
                if col < col1:
                    self.field[piece.row][piece.col - 1] = rook
                    rook.set_position(piece.row, piece.col - 1)
                    self.field[row][col + 3] = None
                else:
                    self.field[piece.row][piece.col + 1] = rook
                    rook.set_position(piece.row, piece.col + 1)
                    self.field[row][col - 4] = None
                cords1 = (row, col + 3) if col < col1 else (row, col - 4)
                cords2 = rook.row, rook.col
                self.color = opponent(self.color)
                return True, cords1, cords2
            return False
        if isinstance(piece, Pawn):
            if piece.can_move(self, row1, col1) or piece.can_attack(self, row1, col1):
                p = self.field[row1][col1]
                self.field[row][col] = None
                self.field[row1][col1] = piece
                self.color = opponent(self.color)
                piece.set_position(row1, col1)
                if piece.get_color() == 'White':
                    if self.white_king.king_is_under_attack(self, self.white_king.row,
                                                            self.white_king.col):
                        self.field[row][col] = piece
                        self.field[row1][col1] = p
                        self.color = opponent(self.color)
                        piece.set_position(row, col)
                        return False
                else:
                    if self.black_king.king_is_under_attack(self, self.black_king.row,
                                                            self.black_king.col):
                        self.field[row][col] = piece
                        self.field[row1][col1] = p
                        self.color = opponent(self.color)
                        piece.set_position(row, col)
                        return False
                return True if not self.check_winner(self.color, piece) else opponent(self.color)
        elif piece.can_move(self, row1, col1):
            p = self.field[row1][col1]
            self.field[row][col] = None
            self.field[row1][col1] = piece
            self.color = opponent(self.color)
            piece.set_position(row1, col1)
            if piece.get_color() == 'White':
                if self.white_king.king_is_under_attack(self, self.white_king.row,
                                                        self.white_king.col):
                    self.field[row][col] = piece
                    self.field[row1][col1] = p
                    self.color = opponent(self.color)
                    piece.set_position(row, col)
                    return False
            else:
                if self.black_king.king_is_under_attack(self, self.black_king.row,
                                                        self.black_king.col):
                    self.field[row][col] = piece
                    self.field[row1][col1] = p
                    self.color = opponent(self.color)
                    piece.set_position(row, col)
                    return False
            return True if not self.check_winner(self.color, piece) else opponent(self.color)

    # Проход пешки из клетки (row, col) в (row1, col1) и превращение в фигуру (char)
    def move_and_promote_pawn(self, row, col, row1, col1, char):
        pawn = self.field[row][col]
        if pawn.can_move(self, row1, col1) or pawn.can_attack(self, row1, col1):
            self.field[row][col] = None
            self.field[row1][col1] = PIECES[char](row, col, pawn.color)
            self.color = opponent(self.color)

    def check_winner(self, color, piece):
        king = self.white_king if color == 'White' else self.black_king
        if king.king_is_under_attack(self, king.row, king.col):
            for i in range(king.row - 1, king.row + 2):
                for j in range(king.col - 1, king.col + 2):
                    if i in range(0, 8) and j in range(0, 8):
                        if self.field[i][j] is None:
                            if king.can_move(self, i, j):
                                return False
                        elif self.field[i][j].color != color:
                            if king.can_move(self, i, j):
                                return False
            for p in [b for a in self.field for b in a if b is not None]:
                if isinstance(p, Pawn):
                    if p.can_attack(self, piece.row, piece.col) and p.get_color() == color:
                        return False
                else:
                    if p.can_move(self, piece.row, piece.col) and p.get_color() == color:
                        return False
            if isinstance(piece, Rook):
                if piece.row == king.row:
                    s = 1 if king.col < piece.col else -1
                    if any(p.can_move(self, piece.row, y) and p.get_color() == king.color
                           for y in range(king.col + s, piece.col, s)
                           for p in [b for a in self.field for b in a if b is not None]):
                        return False
                elif piece.col == king.col:
                    s = 1 if king.row < piece.row else -1
                    if any(p.can_move(self, x, piece.col) and p.get_color() == color
                           for x in range(king.row + s, piece.row, s)
                           for p in [b for a in self.field for b in a if b is not None]):
                        return False
            elif isinstance(piece, Bishop):
                step_x = 1 if king.row < piece.row else -1
                step_y = 1 if king.col < piece.col else -1
                if any(p.can_move(self, x, y) and p.get_color() == color
                       for x, y in zip(range(king.row + step_x, piece.row, step_x),
                                       range(king.col + step_x, piece.col, step_y))
                       for p in [b for a in self.field for b in a if b is not None]):
                    return False
            elif isinstance(piece, Queen):
                if piece.row == king.row:
                    s = 1 if king.col < piece.col else -1
                    if any(p.can_move(self, piece.row, y) and p.get_color() == color
                           for p in [b for a in self.field for b in a if b is not None]
                           for y in range(king.col + s, piece.col, s)):
                        return False
                elif piece.col == king.col:
                    s = 1 if king.row < piece.row else -1
                    if any(p.can_move(self, x, piece.col) and p.get_color() == color
                           for x in range(king.row + s, piece.row, s)
                           for p in [b for a in self.field for b in a if b is not None]):
                        return False
                else:
                    step_x = 1 if king.row < piece.row else -1
                    step_y = 1 if king.col < piece.col else -1
                    if any(p.can_move(self, x, y) and p.get_color() == color
                           for x, y in zip(range(king.row + step_x, piece.row, step_x),
                                           range(king.col + step_x, piece.col, step_y))
                           for p in [b for a in self.field for b in a if b is not None]):
                        return False
            return True
        return False
