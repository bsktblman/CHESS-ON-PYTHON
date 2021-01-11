class BaseFigure:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.img = ''
        self.color = color

    def set_position(self, row1, col1):
        self.row, self.col = row1, col1

    def get_image(self):
        return self.img

    def get_color(self):
        return self.color
