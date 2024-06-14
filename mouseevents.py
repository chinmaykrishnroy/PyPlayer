from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class CustomMainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.resizing = False
        self.dragging = False
        self.resize_position = None
        self.drag_position = None
        self.fullscreen = False
        self.mouseDoubleClickEvent = self.toggle_fullscreen

    def mousePressEvent(self, event):
        edge_margin = 8
        rect = self.rect()
        if (
            rect.topLeft().x() + edge_margin >= event.x()
            or rect.bottomRight().x() - edge_margin <= event.x()
            or rect.topLeft().y() + edge_margin >= event.y()
            or rect.bottomRight().y() - edge_margin <= event.y()
        ):
            self.resizing = True
            self.dragging = False
            self.resize_position = event.globalPos()
        else:
            self.resizing = False
            self.dragging = True
            self.drag_position = event.globalPos() - self.pos()

    def mouseMoveEvent(self, event):
        if self.resizing:
            delta = event.globalPos() - self.resize_position
            new_width = max(self.width() + delta.x(), 100)
            new_height = max(self.height() + delta.y(), 100)
            self.resize(new_width, new_height)
            self.resize_position = event.globalPos()
            self.setCursor(Qt.OpenHandCursor)
        elif self.dragging:
            self.move(event.globalPos() - self.drag_position)

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.dragging = False
        if not self.fullscreen:
            self.setCursor(Qt.ArrowCursor)

    def toggle_fullscreen(self, event):
        if self.fullscreen:
            self.showNormal()
            self.ui.Player.show()
            self.ui.frame.show()
            self.unsetCursor()
        else:
            self.showFullScreen()
            self.ui.Player.hide()
            self.ui.frame.hide()
            self.setCursor(Qt.BlankCursor)
        self.fullscreen = not self.fullscreen
