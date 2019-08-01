import sys

from Qt import QtCore, QtGui, QtWidgets


class ColorSelectionButton(QtWidgets.QPushButton):
    """
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    """

    NORMAL = 1
    OVER = 2
    PRESSED = 3

    color_changed = QtCore.Signal(QtGui.QColor, QtGui.QColor)

    def __init__(self, label=None, callback=None, color=None, parent=None):
        super(ColorSelectionButton, self).__init__(parent)
        self.label = label

        self.callback = callback

        self._color = color
        self._init_color = color

        self.painter = QtGui.QPainter()

        self.mouse_pressed = False

        a = QtGui.QColor(128, 255, 64)
        print a.getHsv()

        self.text_options = QtGui.QTextOption()
        self.text_options.setAlignment(QtCore.Qt.AlignCenter)

        self.pressed.connect(self.on_color_picker)

        self.dlg = QtWidgets.QColorDialog(QtGui.QColor(128, 255, 64))
        self.dlg.setOption(QtWidgets.QColorDialog.ShowAlphaChannel, on=True)

        self.setMouseTracking(True)
        self.state = ColorSelectionButton.NORMAL
        self.installEventFilter(self)

    def set_color(self, color):
        if color != self._color:
            old_color = self._color
            self._color = color
            self.color_changed.emit(old_color, self._color)
            self.update()

    def color(self):
        return self._color

    def color_rgb(self):
        if self._color is not None:
            return self._color.red(), self._color.green(), self._color.blue()

        return 0, 0, 0

    def on_color_picker(self):
        """
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        """
        col = self.dlg.getColor(self._color, parent=self, title='Select a color', options=QtWidgets.QColorDialog.ShowAlphaChannel)

        if col.isValid():
            if self.callback is not None:
                self.callback(col)

            self.set_color(col)

    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.MouseMove:
            if event.buttons() == QtCore.Qt.NoButton:
                self.state = ColorSelectionButton.OVER

        elif event.type() == QtCore.QEvent.MouseButtonPress:
            if event.buttons() == QtCore.Qt.LeftButton:
                if not self.mouse_pressed:
                    self.mouse_pressed = True

                    self.state = ColorSelectionButton.PRESSED

        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            if self.rect().contains(event.pos()):
                if self.mouse_pressed:
                    self.mouse_pressed = False

                    self.state = ColorSelectionButton.OVER
            else:
                self.mouse_pressed = False
        elif event.type() == QtCore.QEvent.Leave:
            self.state = ColorSelectionButton.NORMAL

        return QtWidgets.QPushButton.eventFilter(self, widget, event)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.set_color(self._init_color)

        return super(ColorSelectionButton, self).mousePressEvent(event)

    def paintEvent(self, event):
        self.painter.begin(self)

        self.painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self._color is not None:
            if self.state == ColorSelectionButton.NORMAL:
                self.painter.fillRect(event.rect(), QtGui.QBrush(self._color))
            elif self.state == ColorSelectionButton.OVER:
                self.painter.fillRect(event.rect(), QtGui.QBrush(self._color.darker(115)))
            elif self.state == ColorSelectionButton.PRESSED:
                self.painter.fillRect(event.rect(), QtGui.QBrush(self._color.lighter(115)))
        else:
            self.painter.setPen(QtGui.QColor(0, 0, 0, 255))
            self.painter.drawRect(event.rect().adjusted(2, 2, -2, -2))

        if self._color is not None:
            _, _, v, _ = self._color.getHsv()
            if v > 128:
                self.painter.setPen(QtGui.QColor(0, 0, 0, 255))
            else:
                self.painter.setPen(QtGui.QColor(255, 255, 255, 255))
        else:
            self.painter.setPen(QtGui.QColor(0, 0, 0, 255))

        if self.label is None:
            self.painter.drawText(event.rect(), '[%s, %s, %s, %s]' % (self._color.red(), self._color.green(), self._color.blue(), self._color.alpha()), self.text_options)
        else:
            self.painter.drawText(event.rect(), self.label, self.text_options)

        self.painter.end()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Color selection button')
        self.resize(160, 50)

        widget = QtWidgets.QWidget(self)

        q_color_button = ColorSelectionButton(label=None, color=QtGui.QColor(0, 255, 0, 255), callback=self.callback)
        q_color_button.color_changed.connect(self.color_changed)

        layout = QtWidgets.QVBoxLayout()

        layout.addWidget(q_color_button)

        widget.setLayout(layout)

        self.setCentralWidget(widget)

    def callback(self, selected_color):
        print 'Selected color: %s' % selected_color

    def color_changed(self, old_color, color):
        print 'Color changed from %s to %s' % (old_color, color)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

