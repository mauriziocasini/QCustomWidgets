###############################################################################
# Name:
#   ImageLabel.py
#
# Author:
#   Maurizio Casini
#
# Usage:
#   Visit https://github.com/mauriziocasini for details
#
###############################################################################


import os
import sys
import urllib
import logging

from Qt import QtGui, QtCore, QtWidgets


class ImageLabel(QtWidgets.QLabel):
    def __init__(self, image_path=None, parent=None):
        """
        Initialize the image label instance variables

        :param image_path: path of the image to show. It could be a file path or a url
        :type image_path: str
        :param parent: parent widget reference
        :type parent: QWidget
        """
        super(ImageLabel, self).__init__(parent)

        self.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Plain)

        self.setAlignment(QtCore.Qt.AlignCenter)

        self.painter = QtGui.QPainter()

        self.draw_point = QtCore.QPoint(0, 0)

        self.image = None
        self.scaled_image = None
        self._oversize = False

        self.set_image(image_path)

    def set_image(self, image_path):
        """
        Set the image to show

        :param image_path: path of the image to show. It could be a file path or a url
        :type image_path: str
        """

        if image_path is not None:
            if os.path.exists(image_path):
                self.image = QtGui.QPixmap(image_path)
            else:
                url = urllib.urlopen(image_path)
                if url.getcode() == 200:
                    data = url.read()
                    url.close()
                    self.image = QtGui.QPixmap()
                    self.image.loadFromData(data)
                else:
                    logging.warning('Unable to download image from "%s"' % image_path)
        else:
            self.image = None

        self.update()

    def set_oversize(self, oversize):
        """
        Use this function if you want the image to be scaled beyond its original size

        :param oversize: value to set
        :type oversize: bool
        """
        self._oversize = oversize

    def clear(self):
        """
        Clears any label contents.
        """

        super(ImageLabel, self).clear()

        self.image = None

        self.update()

    def resizeEvent(self, resize_event):
        """
        This event handler receives the widget resize events which are passed in the event parameter

        :type resize_event: QResizeEvent
        """

        if self.image is not None:
            if self._oversize:
                scaled_image_size = resize_event.size()
            else:
                scaled_image_size = resize_event.size().boundedTo(self.image.size())

            self.scaled_image = self.image.scaled(scaled_image_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)

    def paintEvent(self, event):
        """
        This event handler receives paint events passed in the event parameter
        It draws the scaled image and calls the base class method

        :type event: QPaintEvent
        """
        if self.scaled_image is not None:
            # start painting the label from left upper corner
            if self.alignment() & QtCore.Qt.AlignHCenter:
                self.draw_point.setX((self.size().width() - self.scaled_image.width()) / 2)
            elif self.alignment() & QtCore.Qt.AlignLeft:
                self.draw_point.setX(0)
            elif self.alignment() & QtCore.Qt.AlignRight:
                self.draw_point.setX(self.size().width() - self.scaled_image.width())

            if self.alignment() & QtCore.Qt.AlignVCenter:
                self.draw_point.setY((self.size().height() - self.scaled_image.height()) / 2)
            elif self.alignment() & QtCore.Qt.AlignTop:
                self.draw_point.setY(0)
            elif self.alignment() & QtCore.Qt.AlignBottom:
                self.draw_point.setY(self.size().height() - self.scaled_image.height())

            self.painter.begin(self)
            self.painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
            self.painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing, True)
            self.painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
            self.painter.drawPixmap(self.draw_point, self.scaled_image)
            self.painter.end()

        super(ImageLabel, self).paintEvent(event)


class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("Image label")

        layout = QtWidgets.QHBoxLayout()

        widget = ImageLabel(image_path=r'.\image.png')
        widget.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(widget)

        widget = ImageLabel()
        widget.set_image(r'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png')
        widget.setAlignment(QtCore.Qt.AlignCenter)
        widget.setText('GitHub')
        widget.set_oversize(True)
        layout.addWidget(widget)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
