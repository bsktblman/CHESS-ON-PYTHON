import sys
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication
from ui import Chess
from Board import Board

BUTTONS, COORDS = {}, {}
FILE_NAMES = ['Rook.svg', 'Knight.svg', 'Bishop.svg', 'Queen.svg', 'King.svg', 'Bishop.svg',
              'Knight.svg', 'Rook.svg']
COUNT = 0
sound = QSound('sound.wav')


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    board = Board()
    app = QApplication(sys.argv)
    ex = Chess()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
