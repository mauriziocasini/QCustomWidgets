import os

from Qt import QtGui, QtCore, QtWidgets


class ImageLabel(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)

        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Plain)

        self.setAlignment(QtCore.Qt.AlignCenter)

        self.painter = QtGui.QPainter()

        self.start_draw_point = QtCore.QPoint(0, 0)

        self.is_movie = False

        self.image = None
        self.movie = None

        self.oversize = False

    def set_image(self, image_path):
        self.is_movie = False

        if self.movie is not None:
            self.movie.frameChanged.disconnect()
            self.movie.stop()
            self.movie = None

        if os.path.exists(image_path):
            self.image = QtGui.QPixmap(image_path)

        self.update()

    def set_movie(self, movie_path):
        self.is_movie = True

        # if os.path.exists(movie_path):
        self.movie = QtGui.QMovie(movie_path)
        self.movie.setCacheMode(QtGui.QMovie.CacheAll)
        self.movie.jumpToFrame(0)
        self.image = QtGui.QPixmap(self.movie.frameRect().size())
        self.movie.frameChanged.connect(self.repaint)

        self.movie.start()

    def set_oversize(self, oversize):
        self.oversize = oversize

    def reset(self):
        self.is_movie = False

        if self.movie is not None:
            self.movie.frameChanged.disconnect()
            self.movie.stop()
            self.movie = None

        self.image = QtGui.QPixmap()

        self.update()

    def paintEvent(self, event):
        if self.is_movie:
            self.image = self.movie.currentPixmap()
            self.setMask(self.image.mask())

        if self.image is not None:
            size = self.size()
            image_size = size

            if not self.oversize:
                image_size = self.size().boundedTo(self.image.size())

            scaled_image = self.image.scaled(image_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

            # start painting the label from left upper corner
            if self.alignment() & QtCore.Qt.AlignHCenter:
                self.start_draw_point.setX((size.width() - scaled_image.width()) / 2)
            elif self.alignment() & QtCore.Qt.AlignLeft:
                self.start_draw_point.setX(0)
            elif self.alignment() & QtCore.Qt.AlignRight:
                self.start_draw_point.setX(size.width() - scaled_image.width())

            if self.alignment() & QtCore.Qt.AlignVCenter:
                self.start_draw_point.setY((size.height() - scaled_image.height()) / 2)
            elif self.alignment() & QtCore.Qt.AlignTop:
                self.start_draw_point.setY(0)
            elif self.alignment() & QtCore.Qt.AlignBottom:
                self.start_draw_point.setY(size.height() - scaled_image.height())

            self.painter.begin(self)
            self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            self.painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
            self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
            self.painter.drawPixmap(self.start_draw_point, scaled_image)
            self.painter.end()


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        layout = QtWidgets.QVBoxLayout()

        widget = ImageLabel()
        widget.set_image(r'.\image.png')
        widget.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(widget)

        self.setLayout(layout)

        self.setWindowTitle("Image label")


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWin = Window()
    mainWin.show()
    sys.exit(app.exec_())
