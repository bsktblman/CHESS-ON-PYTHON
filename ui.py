from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QMainWindow, QPushButton
from Board import Board
from Pieces.Pawn import Pawn

BUTTONS, CORDS = {}, {}
FILE_NAMES = ['Rook.svg', 'Knight.svg', 'Bishop.svg', 'Queen.svg', 'King.svg', 'Bishop.svg',
              'Knight.svg', 'Rook.svg']
COUNT = 0
sound = QSound('sound.wav')
dct = {'Конь': 'Knight', 'Слон': 'Bishop', 'Ладья': 'Rook', 'Ферзь': 'Queen'}


class Chess(QMainWindow):
    def __init__(self):
        super(Chess, self).__init__()
        uic.loadUi('chess.ui', self)
        self.board = Board()
        self.choose.hide()
        self.step.setText('Ход белых' if self.board.color == 'White' else 'Ход чёрных')
        self.label_10.hide()
        self.new_game.hide()
        self.ok.hide()
        self.ok.clicked.connect(self.promote_pawn)
        self.setWindowTitle('Chess')
        self.setWindowIcon(QtGui.QIcon('Images/Black/BlackPawn.svg'))
        for i in range(8):
            for j in range(8):
                self.btn = QPushButton('', self)
                self.btn.resize(90, 90)
                if j == 0 or j == 7:
                    path = ['Images', 'Black', 'Black'] if j == 0 else ['Images', 'White', 'White']
                    self.btn.setIcon(QtGui.QIcon('/'.join(path) + FILE_NAMES[i]))
                elif j == 1:
                    self.btn.setIcon(QtGui.QIcon('Images/Black/BlackPawn.svg'))
                elif j == 6:
                    self.btn.setIcon(QtGui.QIcon('Images/White/WhitePawn.svg'))
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    self.btn.setStyleSheet('background: "#FECE9E";')
                else:
                    self.btn.setStyleSheet('background: "#D18B46";')
                self.btn.move(i * 90, j * 90)
                self.btn.setIconSize(QtCore.QSize(70, 70))
                BUTTONS[self.btn] = (j, i)
                CORDS[(j, i)] = self.btn
                self.btn.clicked.connect(self.press)

    def press(self):
        global COUNT
        # print(BUTTONS[self.sender()])
        COUNT += 1
        if COUNT % 2 == 1:
            self.sender().setStyleSheet('background: "#32CD32";')
            self.first = BUTTONS[self.sender()]
            self.icon = self.sender().icon()
        else:
            i, j = self.first
            CORDS[self.first].setStyleSheet('background: "#FECE9E";'
                                            if (i % 2 == 0 and j % 2 == 0)
                                            or (i % 2 == 1 and j % 2 == 1)
                                            else 'background: "#D18B46";')
            self.second = BUTTONS[self.sender()]
            if ((self.first[0] == 1 and self.second[0] == 0) or
                (self.first[0] == 6 and self.second[0] == 7)) \
                    and isinstance(self.board.field[self.first[0]][self.first[1]], Pawn) and \
                    self.board.field[self.second[0]][self.second[1]] is None:
                for key in BUTTONS.keys():
                    key.setEnabled(False)
                self.choose.show()
                self.label_10.show()
                self.ok.show()
                sound.play()
            else:
                result = self.board.move_piece(*self.first, *BUTTONS[self.sender()])
                if result == 'Black':
                    self.make_move(self.first, self.icon)
                    self.winner.setText('Победа чёрных!')
                    self.step.hide()
                    self.new_game.show()
                    for key in BUTTONS.keys():
                        key.setEnabled(False)
                    sound.play()
                elif result == 'White':
                    self.make_move(self.first, self.icon)
                    self.winner.setText('Победа белых!')
                    self.step.hide()
                    self.new_game.show()
                    for key in BUTTONS.keys():
                        key.setEnabled(False)
                    sound.play()
                elif type(result) is tuple:
                    if result[0]:
                        self.make_move(self.first, self.icon)
                        icon = CORDS[result[1]].icon()
                        CORDS[result[1]].setIcon(QtGui.QIcon())
                        CORDS[result[2]].setIcon(icon)
                        sound.play()
                        self.step.setText(
                            'Ход белых' if self.board.color == 'White' else 'Ход чёрных')
                elif result:
                    self.make_move(self.first, self.icon)
                    sound.play()
                    self.step.setText('Ход белых' if self.board.color == 'White' else 'Ход чёрных')

    def make_move(self, cords, icon):
        CORDS[cords].setIcon(QtGui.QIcon())
        self.sender().setIcon(icon)

    def promote_pawn(self):
        for key in BUTTONS.keys():
            key.setEnabled(True)
        self.choose.hide()
        self.label_10.hide()
        self.ok.hide()
        color = self.board.field[self.first[0]][self.first[1]].color
        self.board.move_and_promote_pawn(self.first[0], self.first[1], self.second[0],
                                         self.second[1], self.choose.selectedItems()[0].text())
        CORDS[self.first].setIcon(QtGui.QIcon())
        CORDS[self.second].setIcon(QtGui.QIcon(f'Images/{color}/{color}'
                                               f'{dct[self.choose.selectedItems()[0].text()]}.svg'))
        self.step.setText('Ход белых' if self.board.color == 'White' else 'Ход чёрных')
