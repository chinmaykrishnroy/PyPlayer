import os
import random
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt
from PyQt5 import sip


class CustomMainWindow(QtWidgets.QMainWindow):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.resizing = False
        self.dragging = False
        self.resize_position = None
        self.drag_position = None
        self.click_count = 0
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.reset_click_count)
        self.fullscreen = False

    def reset_click_count(self):
        self.click_count = 0
        self.timer.stop()

    def mousePressEvent(self, event):
        self.click_count += 1
        if self.click_count == 3:
            self.toggle_fullscreen()
            self.reset_click_count()
        else:
            self.timer.start()
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

    def toggle_fullscreen(self):
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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(790, 496)
        MainWindow.setWindowIcon(QtGui.QIcon(":/icons/icons/player.png"))
        MainWindow.setAcceptDrops(True)
        MainWindow.dragEnterEvent = self.dragEnterEvent
        MainWindow.dropEvent = self.dropEvent
        self.default_volume = 60
        self.media_files = []
        self.mode_random = False
        self.initial_size = MainWindow.size()
        self.audio_formats = [".mp3", ".wav", ".aac", ".pcm"]
        self.video_formats = [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".3gp"]
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.resetLabel = QtCore.QTimer()
        self.resetLabel.setSingleShot(True)
        self.resetLabel.timeout.connect(self.reset_media_title)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(
            "QWidget {\n" "background-color: #224455;\n" "}"
        )
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.VideoPlayer = QVideoWidget(self.centralwidget)
        self.VideoPlayer.setMinimumSize(QtCore.QSize(480, 270))
        self.VideoPlayer.setStyleSheet("")
        self.VideoPlayer.setObjectName("VideoPlayer")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.VideoPlayer)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout.addItem(spacerItem)
        self.mediaPlay = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlay.setVolume(self.default_volume)
        self.playlist = QMediaPlaylist()
        self.current_media_file = None
        self.current_volume = self.default_volume
        self.player_locked = False
        self.mediaPlay.setPlaylist(self.playlist)
        self.frame = QtWidgets.QFrame(self.VideoPlayer)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(
            88, 39, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem1)
        self.videoTitleLabel = QtWidgets.QLabel(self.frame)
        self.videoTitleLabel.setMinimumSize(QtCore.QSize(460, 42))
        self.videoTitleLabel.setStyleSheet(
            "QLabel {\n"
            "background: transparent;\n"
            "color: #FFEEDD;\n"
            'font-family: "Helvetica", sans-serif;\n'
            "font-size: 32px;\n"
            "}"
        )
        self.videoTitleLabel.setObjectName("videoTitleLabel")
        self.horizontalLayout_2.addWidget(self.videoTitleLabel)
        spacerItem2 = QtWidgets.QSpacerItem(
            88, 39, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 5)
        self.horizontalLayout_2.setStretch(2, 1)
        self.verticalLayout.addWidget(self.frame)
        self.verticalLayout_2.addWidget(self.VideoPlayer)
        self.mediaPlay.setVideoOutput(self.VideoPlayer)
        self.Player = QtWidgets.QFrame(self.centralwidget)
        self.Player.setObjectName("Player")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Player)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem3)
        self.MediaPlayer = QtWidgets.QFrame(self.Player)
        self.MediaPlayer.setMinimumSize(QtCore.QSize(480, 50))
        self.MediaPlayer.setMaximumSize(QtCore.QSize(16777215, 56))
        self.MediaPlayer.setStyleSheet("")
        self.MediaPlayer.setObjectName("MediaPlayer")
        self.mediaControlHorizontalLayout = QtWidgets.QHBoxLayout(self.MediaPlayer)
        self.mediaControlHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.mediaControlHorizontalLayout.setSpacing(0)
        self.mediaControlHorizontalLayout.setObjectName("mediaControlHorizontalLayout")
        self.MediaController = QtWidgets.QFrame(self.MediaPlayer)
        self.MediaController.setMinimumSize(QtCore.QSize(480, 50))
        self.MediaController.setMaximumSize(QtCore.QSize(680, 56))
        self.MediaController.setStyleSheet(
            "QFrame {\n"
            "    background-color: #111111;\n"
            '    font-family: "Helvetica", sans-serif;\n'
            "}"
        )
        self.MediaController.setObjectName("MediaController")
        self.mediaPlayerVerticalLayout = QtWidgets.QVBoxLayout(self.MediaController)
        self.mediaPlayerVerticalLayout.setContentsMargins(1, 0, 1, 0)
        self.mediaPlayerVerticalLayout.setSpacing(0)
        self.mediaPlayerVerticalLayout.setObjectName("mediaPlayerVerticalLayout")
        self.MediaProgressBar = QtWidgets.QFrame(self.MediaController)
        self.MediaProgressBar.setStyleSheet("")
        self.MediaProgressBar.setObjectName("MediaProgressBar")
        self.mediaProgressBarHorizontalLayout = QtWidgets.QHBoxLayout(
            self.MediaProgressBar
        )
        self.mediaProgressBarHorizontalLayout.setContentsMargins(8, 0, 8, 0)
        self.mediaProgressBarHorizontalLayout.setSpacing(8)
        self.mediaProgressBarHorizontalLayout.setObjectName(
            "mediaProgressBarHorizontalLayout"
        )
        self.playbackTimeLabel = QtWidgets.QLabel(self.MediaProgressBar)
        self.playbackTimeLabel.setMinimumSize(QtCore.QSize(44, 16))
        self.playbackTimeLabel.setMaximumSize(QtCore.QSize(44, 16))
        self.playbackTimeLabel.setStyleSheet(
            "QLabel {\n"
            "background: transparent;\n"
            "color: #FFEEDD;\n"
            'font-family: "Helvetica", sans-serif;\n'
            "}"
        )
        self.playbackTimeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.playbackTimeLabel.setObjectName("playbackTimeLabel")
        self.mediaProgressBarHorizontalLayout.addWidget(self.playbackTimeLabel)
        self.playbackProgress = QtWidgets.QSlider(self.MediaProgressBar)
        self.playbackProgress.setMinimumSize(QtCore.QSize(360, 12))
        self.playbackProgress.setMaximumSize(QtCore.QSize(16777215, 12))
        self.playbackProgress.setStyleSheet(
            "QSlider {\n"
            "    background: transparent;\n"
            "    height: 6px;\n"
            "}\n"
            "\n"
            "QSlider::groove:horizontal {\n"
            "    border: none;\n"
            "    height: 6px;\n"
            "    background: #33383E;\n"
            "    border-radius: 3px;\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal {\n"
            "    width: 6px;\n"
            "    background: #22272d;\n"
            "    border-radius: 3px;\n"
            "}\n"
            "\n"
            "QSlider::sub-page:horizontal {\n"
            "    background: #F1594B;\n"
            "    margin-left: 2px;\n"
            "    width: 6px;\n"
            "    border-radius: 3px;\n"
            "}\n"
            ""
        )
        self.playbackProgress.setMaximum(499)
        self.playbackProgress.setOrientation(QtCore.Qt.Horizontal)
        self.playbackProgress.setObjectName("playbackProgress")
        self.mediaProgressBarHorizontalLayout.addWidget(self.playbackProgress)
        self.mediaLenghtLabel = QtWidgets.QLabel(self.MediaProgressBar)
        self.mediaLenghtLabel.setMinimumSize(QtCore.QSize(44, 16))
        self.mediaLenghtLabel.setMaximumSize(QtCore.QSize(44, 16))
        self.mediaLenghtLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.mediaLenghtLabel.setStyleSheet(
            "QLabel {\n"
            "background: transparent;\n"
            "color: #FFEEDD;\n"
            'font-family: "Helvetica", sans-serif;\n'
            "}"
        )
        self.mediaLenghtLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.mediaLenghtLabel.setObjectName("mediaLenghtLabel")
        self.mediaProgressBarHorizontalLayout.addWidget(self.mediaLenghtLabel)
        self.mediaPlayerVerticalLayout.addWidget(self.MediaProgressBar)
        self.MediaButtons = QtWidgets.QFrame(self.MediaController)
        self.MediaButtons.setStyleSheet(
            "QFrame {\n"
            "    background-color: #0F111A; \n"
            "}\n"
            "\n"
            "QPushButton { \n"
            "    background: transparent; border: none;  border-radius: 5px;\n"
            "}\n"
            "\n"
            "QPushButton:hover {\n"
            "    background-color:#33383E; \n"
            "    border-style: solid; \n"
            "    border-radius: 2px; \n"
            "}\n"
            "\n"
            "QPushButton:pressed {\n"
            "     background-color: #4455FF; \n"
            "    border-style: solid; \n"
            "    border-radius: 2px; \n"
            "}"
        )
        self.MediaButtons.setObjectName("MediaButtons")
        self.mediaButtonsHorizontalLayout = QtWidgets.QHBoxLayout(self.MediaButtons)
        self.mediaButtonsHorizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.mediaButtonsHorizontalLayout.setSpacing(2)
        self.mediaButtonsHorizontalLayout.setObjectName("mediaButtonsHorizontalLayout")
        spacerItem4 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.mediaButtonsHorizontalLayout.addItem(spacerItem4)
        self.fileOpenerButton = QtWidgets.QPushButton(self.MediaButtons)
        self.fileOpenerButton.setMinimumSize(QtCore.QSize(24, 24))
        self.fileOpenerButton.setMaximumSize(QtCore.QSize(24, 24))
        self.fileOpenerButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/icons/cil-folder-open.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.fileOpenerButton.setIcon(icon)
        self.fileOpenerButton.setObjectName("fileOpenerButton")
        self.mediaButtonsHorizontalLayout.addWidget(self.fileOpenerButton)
        self.playerLockButton = QtWidgets.QPushButton(self.MediaButtons)
        self.playerLockButton.setMinimumSize(QtCore.QSize(24, 24))
        self.playerLockButton.setMaximumSize(QtCore.QSize(24, 24))
        self.playerLockButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/icons/cil-lock-unlocked.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.playerLockButton.setIcon(icon1)
        self.playerLockButton.setObjectName("playerLockButton")
        self.mediaButtonsHorizontalLayout.addWidget(self.playerLockButton)
        spacerItem5 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.mediaButtonsHorizontalLayout.addItem(spacerItem5)
        self.mediaTitle = QtWidgets.QLabel(self.MediaButtons)
        self.mediaTitle.setMinimumSize(QtCore.QSize(60, 0))
        self.mediaTitle.setStyleSheet(
            "QLabel {\n"
            "background: transparent;\n"
            "color: #FFEEDD;\n"
            'font-family: "Helvetica", sans-serif;\n'
            "}"
        )
        self.mediaTitle.setObjectName("mediaTitle")
        self.mediaButtonsHorizontalLayout.addWidget(self.mediaTitle)
        spacerItem6 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.mediaButtonsHorizontalLayout.addItem(spacerItem6)
        self.mediaPreviousButton = QtWidgets.QPushButton(self.MediaButtons)
        self.mediaPreviousButton.setMinimumSize(QtCore.QSize(24, 24))
        self.mediaPreviousButton.setMaximumSize(QtCore.QSize(24, 24))
        self.mediaPreviousButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/icons/cil-media-step-backward.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.mediaPreviousButton.setIcon(icon2)
        self.mediaPreviousButton.setIconSize(QtCore.QSize(20, 20))
        self.mediaPreviousButton.setObjectName("mediaPreviousButton")
        self.mediaButtonsHorizontalLayout.addWidget(self.mediaPreviousButton)
        self.mediaPlayPauseButton = QtWidgets.QPushButton(self.MediaButtons)
        self.mediaPlayPauseButton.setMinimumSize(QtCore.QSize(24, 24))
        self.mediaPlayPauseButton.setMaximumSize(QtCore.QSize(24, 24))
        self.mediaPlayPauseButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/icons/cil-media-play.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.mediaPlayPauseButton.setIcon(icon3)
        self.mediaPlayPauseButton.setIconSize(QtCore.QSize(20, 20))
        self.mediaPlayPauseButton.setObjectName("mediaPlayPauseButton")
        self.mediaButtonsHorizontalLayout.addWidget(self.mediaPlayPauseButton)
        self.mediaNextButton = QtWidgets.QPushButton(self.MediaButtons)
        self.mediaNextButton.setMinimumSize(QtCore.QSize(24, 24))
        self.mediaNextButton.setMaximumSize(QtCore.QSize(24, 24))
        self.mediaNextButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/icons/cil-media-step-forward.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.mediaNextButton.setIcon(icon4)
        self.mediaNextButton.setIconSize(QtCore.QSize(20, 20))
        self.mediaNextButton.setObjectName("mediaNextButton")
        self.mediaButtonsHorizontalLayout.addWidget(self.mediaNextButton)
        spacerItem7 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.mediaButtonsHorizontalLayout.addItem(spacerItem7)
        self.mediaRepeatButton = QtWidgets.QPushButton(self.MediaButtons)
        self.mediaRepeatButton.setMinimumSize(QtCore.QSize(24, 24))
        self.mediaRepeatButton.setMaximumSize(QtCore.QSize(24, 24))
        self.mediaRepeatButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/icons/cil-loop.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.mediaRepeatButton.setIcon(icon5)
        self.mediaRepeatButton.setIconSize(QtCore.QSize(20, 20))
        self.mediaRepeatButton.setObjectName("mediaRepeatButton")
        self.mediaButtonsHorizontalLayout.addWidget(self.mediaRepeatButton)
        self.mediaShuffleButton = QtWidgets.QPushButton(self.MediaButtons)
        self.mediaShuffleButton.setMinimumSize(QtCore.QSize(24, 24))
        self.mediaShuffleButton.setMaximumSize(QtCore.QSize(24, 24))
        self.mediaShuffleButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/icons/cil-infinity.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.mediaShuffleButton.setIcon(icon6)
        self.mediaShuffleButton.setObjectName("mediaShuffleButton")
        self.mediaButtonsHorizontalLayout.addWidget(self.mediaShuffleButton)
        self.mediaAudioTrack = QtWidgets.QPushButton(self.MediaButtons)
        self.mediaAudioTrack.setMinimumSize(QtCore.QSize(24, 24))
        self.mediaAudioTrack.setMaximumSize(QtCore.QSize(24, 24))
        self.mediaAudioTrack.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/icons/cil-notes.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.mediaAudioTrack.setIcon(icon7)
        self.mediaAudioTrack.setIconSize(QtCore.QSize(20, 20))
        self.mediaAudioTrack.setObjectName("mediaAudioTrack")
        self.mediaButtonsHorizontalLayout.addWidget(self.mediaAudioTrack)
        spacerItem8 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.mediaButtonsHorizontalLayout.addItem(spacerItem8)
        self.mediaMuteButton = QtWidgets.QPushButton(self.MediaButtons)
        self.mediaMuteButton.setMinimumSize(QtCore.QSize(16, 16))
        self.mediaMuteButton.setMaximumSize(QtCore.QSize(16, 16))
        self.mediaMuteButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/icons/cil-volume-high.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.mediaMuteButton.setIcon(icon8)
        self.mediaMuteButton.setObjectName("mediaMuteButton")
        self.mediaButtonsHorizontalLayout.addWidget(self.mediaMuteButton)
        self.volumeSlider = QtWidgets.QSlider(self.MediaButtons)
        self.volumeSlider.setMinimumSize(QtCore.QSize(72, 6))
        self.volumeSlider.setStyleSheet(
            "QSlider {\n"
            "    background: transparent;\n"
            "    height: 5px;\n"
            "}\n"
            "\n"
            "QSlider::groove:horizontal {\n"
            "    border: none;\n"
            "    height: 5px;\n"
            "    background: #33383E;\n"
            "    border-radius: 2px;\n"
            "}\n"
            "\n"
            "QSlider::handle:horizontal {\n"
            "    width: 5px;\n"
            "    background: #22272d;\n"
            "    border-radius: 2px;\n"
            "}\n"
            "\n"
            "QSlider::sub-page:horizontal {\n"
            "    background: #4b59f1;\n"
            "    margin-left: 2px;\n"
            "    width: 5px;\n"
            "    border-radius: 2px;\n"
            "}\n"
            "\n"
            ""
        )
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.volumeSlider.setValue(self.default_volume)
        self.mediaButtonsHorizontalLayout.addWidget(self.volumeSlider)
        spacerItem9 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.mediaButtonsHorizontalLayout.addItem(spacerItem9)
        self.appControlButton = QtWidgets.QFrame(self.MediaButtons)
        self.appControlButton.setStyleSheet("")
        self.appControlButton.setObjectName("appControlButton")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.appControlButton)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.minimizeButton = QtWidgets.QPushButton(self.appControlButton)
        self.minimizeButton.setMinimumSize(QtCore.QSize(24, 24))
        self.minimizeButton.setMaximumSize(QtCore.QSize(24, 24))
        self.minimizeButton.setStyleSheet(
            "QPushButton { \n"
            "    background: transparent; border-radius: 0px;\n"
            "}\n"
            "QPushButton:hover {\n"
            "    background-color:#665622;; \n"
            "}\n"
            "QPushButton:pressed {\n"
            "     background-color: #AAAA00; \n"
            "}"
        )
        self.minimizeButton.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_minimize.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.minimizeButton.setIcon(icon8)
        self.minimizeButton.setObjectName("minimizeButton")
        self.horizontalLayout_3.addWidget(self.minimizeButton)
        self.closeButton = QtWidgets.QPushButton(self.appControlButton)
        self.closeButton.setMinimumSize(QtCore.QSize(24, 24))
        self.closeButton.setMaximumSize(QtCore.QSize(24, 24))
        self.closeButton.setStyleSheet(
            "QPushButton:hover {\n"
            "    background-color:#962128; \n"
            "    border-style: none;\n"
            "    border-radius: 0px;\n"
            "}\n"
            "QPushButton:pressed {\n"
            "     background-color: #ff0000;\n"
            "    border-style: none;\n"
            "    border-radius: 0px;\n"
            "}"
        )
        self.closeButton.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/icons/icons/icon_close.png"),
            QtGui.QIcon.Normal,
            QtGui.QIcon.Off,
        )
        self.closeButton.setIcon(icon9)
        self.closeButton.setCheckable(False)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout_3.addWidget(self.closeButton)
        self.mediaButtonsHorizontalLayout.addWidget(self.appControlButton)
        self.mediaButtonsHorizontalLayout.setStretch(0, 10)
        self.mediaButtonsHorizontalLayout.setStretch(3, 20)
        self.mediaButtonsHorizontalLayout.setStretch(4, 100)
        self.mediaButtonsHorizontalLayout.setStretch(5, 20)
        self.mediaButtonsHorizontalLayout.setStretch(9, 5)
        self.mediaButtonsHorizontalLayout.setStretch(13, 10)
        self.mediaButtonsHorizontalLayout.setStretch(15, 15)
        self.mediaButtonsHorizontalLayout.setStretch(16, 5)
        self.fileOpenerButton.raise_()
        self.mediaTitle.raise_()
        self.mediaPreviousButton.raise_()
        self.mediaPlayPauseButton.raise_()
        self.mediaNextButton.raise_()
        self.mediaRepeatButton.raise_()
        self.mediaShuffleButton.raise_()
        self.mediaAudioTrack.raise_()
        self.volumeSlider.raise_()
        self.appControlButton.raise_()
        self.mediaMuteButton.raise_()
        self.playerLockButton.raise_()
        self.mediaPlayerVerticalLayout.addWidget(self.MediaButtons)
        self.mediaControlHorizontalLayout.addWidget(self.MediaController)
        self.mediaControlHorizontalLayout.setStretch(0, 3)
        self.horizontalLayout.addWidget(self.MediaPlayer)
        spacerItem10 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem10)
        self.verticalLayout_2.addWidget(self.Player)
        MainWindow.setCentralWidget(self.centralwidget)

        self.fileOpenerButton.clicked.connect(self.handle_file_opener)
        self.mediaPreviousButton.clicked.connect(self.handle_media_previous)
        self.mediaPlayPauseButton.clicked.connect(self.handle_media_play_pause)
        self.mediaNextButton.clicked.connect(self.handle_media_next)
        self.mediaRepeatButton.clicked.connect(self.handle_media_repeat)
        self.mediaShuffleButton.clicked.connect(self.handle_media_shuffle)
        self.mediaMuteButton.clicked.connect(self.handle_media_mute)
        self.playerLockButton.clicked.connect(self.handle_player_lock)
        self.closeButton.clicked.connect(self.handle_close_button)
        self.minimizeButton.clicked.connect(self.handle_minimize_button)
        self.volumeSlider.valueChanged.connect(self.handle_volume_slider)
        self.playbackProgress.sliderMoved.connect(self.seek_media)
        self.playbackProgress.valueChanged.connect(self.update_slider_position)
        self.mediaPlay.positionChanged.connect(self.update_position)
        self.mediaPlay.durationChanged.connect(self.update_duration)
        self.mediaPlay.mediaStatusChanged.connect(self.handle_media_state_changed)
        MainWindow.keyPressEvent = self.keyPressEvent
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyPlayer"))
        self.videoTitleLabel.setText(_translate("MainWindow", "Example Video Title"))
        self.playbackTimeLabel.setText(_translate("MainWindow", "--:--"))
        self.mediaLenghtLabel.setText(_translate("MainWindow", "--:--"))
        self.mediaTitle.setText(
            _translate("MainWindow", "PyPlayer: A Media-Player in Python")
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.handle_close_button()
        elif event.key() == Qt.Key_Minus:
            self.handle_minimize_button()
        elif event.key() == Qt.Key_L:
            self.handle_player_lock()
        if not self.player_locked:
            if event.key() == Qt.Key_O:
                self.handle_file_opener()
            elif event.key() == Qt.Key_P:
                self.handle_media_previous()
            elif event.key() == Qt.Key_Space:
                self.handle_media_play_pause()
            elif event.key() == Qt.Key_F:
                self.handle_media_play_pause()
            elif event.key() == Qt.Key_N:
                self.handle_media_next()
            elif event.key() == Qt.Key_R:
                self.handle_media_repeat()
            elif event.key() == Qt.Key_S:
                self.handle_media_shuffle()
            elif event.key() == Qt.Key_M:
                self.handle_media_mute()
            elif event.key() == Qt.Key_U:
                current_volume = self.volumeSlider.value()
                self.volumeSlider.setValue(min(current_volume + 5, 100))
            elif event.key() == Qt.Key_J:
                current_volume = self.volumeSlider.value()
                self.volumeSlider.setValue(max(current_volume - 5, 0))
            elif event.key() == Qt.Key_G:
                self.seek_playback_by(-10)
            elif event.key() == Qt.Key_H:
                self.seek_playback_by(10)
            elif event.key() == Qt.Key_Up:
                current_volume = self.volumeSlider.value()
                self.volumeSlider.setValue(min(current_volume + 5, 100))
            elif event.key() == Qt.Key_Down:
                current_volume = self.volumeSlider.value()
                self.volumeSlider.setValue(max(current_volume - 5, 0))
            elif event.key() == Qt.Key_Left:
                self.seek_playback_by(-10)
            elif event.key() == Qt.Key_Right:
                self.seek_playback_by(10)

    def handle_media_previous(self):
        print("Media previous button clicked")
        if (
            hasattr(self, "media_files")
            and self.media_files
            and self.current_media_file
        ):
            current_index = self.media_files.index(self.current_media_file)
            next_index = (current_index - 1) % len(self.media_files)
            next_file_path = self.media_files[next_index]
            self.play_media_file(next_file_path)
            self.current_media_file = next_file_path

    def handle_media_play_pause(self):
        if len(self.media_files):
            print("Media play/pause button clicked")
            if self.mediaPlay.state() == QMediaPlayer.PlayingState:
                self.mediaPlay.pause()
                self.mediaPlayPauseButton.setIcon(
                    QtGui.QIcon(":/icons/icons/cil-media-play.png")
                )
            else:
                self.mediaPlay.play()
                self.mediaPlayPauseButton.setIcon(
                    QtGui.QIcon(":/icons/icons/cil-media-pause.png")
                )
        else:
            self.mediaTitle.setText("Empty Playlist!")

    def handle_media_next(self):
        print("Media next button clicked")
        if (
            hasattr(self, "media_files")
            and self.media_files
            and self.current_media_file
        ):
            current_index = self.media_files.index(self.current_media_file)
            if self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
                self.mediaPlay.setPosition(0)
                #next_index = current_index
            else:
                next_index = (current_index + 1) % len(self.media_files)
                next_file_path = self.media_files[next_index]
                self.play_media_file(next_file_path)
                self.current_media_file = next_file_path
                if self.playlist.playbackMode() != QMediaPlaylist.CurrentItemInLoop:
                    if (
                        next_index == 0
                        and self.playlist.playbackMode() != QMediaPlaylist.Loop
                    ):
                        if self.mediaPlay.state() == QMediaPlayer.PlayingState:
                            self.mediaPlay.pause()
                            self.mediaPlayPauseButton.setIcon(
                                QtGui.QIcon(":/icons/icons/cil-media-play.png")
                            )
                            self.mediaTitle.setText(f"End of Playlist!")
                            self.resetLabel.start(2000)

    def handle_media_mute(self):
        print("Media mute button clicked")
        if self.mediaPlay.volume() == 0:
            self.mediaPlay.setVolume(self.current_volume)
            self.volumeSlider.setEnabled(True)
            self.mediaMuteButton.setIcon(
                QtGui.QIcon(":/icons/icons/cil-volume-high.png")
            )
        else:
            self.current_volume = self.mediaPlay.volume()
            self.volumeSlider.setEnabled(False)
            self.mediaPlay.setVolume(0)
            self.mediaMuteButton.setIcon(
                QtGui.QIcon(":/icons/icons/cil-volume-off.png")
            )

    def handle_media_state_changed(self, state):
        if state == QMediaPlayer.EndOfMedia:
            if self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
                self.mediaPlay.play()
                self.mediaPlay.setPosition(0)
                self.mediaPlay.play()
                return
            self.handle_media_next()

    def handle_media_repeat(self):
        print("Media repeat button clicked")
        if self.playlist.playbackMode() == QMediaPlaylist.Sequential:
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            self.mediaRepeatButton.setIcon(QtGui.QIcon(":/icons/icons/cil-loop-circular.png"))
        elif self.playlist.playbackMode() == QMediaPlaylist.Loop:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.mediaRepeatButton.setIcon(QtGui.QIcon(":/icons/icons/cil-loop-1.png"))
        else:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            self.mediaRepeatButton.setIcon(QtGui.QIcon(":/icons/icons/cil-loop.png"))

    def handle_media_shuffle(self):
        print("Media shuffle button clicked")
        if not self.mode_random:
            self.original_media_files = self.media_files.copy()
            random.shuffle(self.media_files)
            self.playlist.clear()
            for file_path in self.media_files:
                self.playlist.addMedia(
                    QMediaContent(QtCore.QUrl.fromLocalFile(file_path))
                )
            self.playlist.setPlaybackMode(
                QMediaPlaylist.Sequential
            )
            self.mediaShuffleButton.setIcon(QtGui.QIcon(":/icons/icons/cil-layers.png"))
        else:
            self.media_files = self.original_media_files
            self.playlist.clear()
            for file_path in self.media_files:
                self.playlist.addMedia(
                    QMediaContent(QtCore.QUrl.fromLocalFile(file_path))
                )
            self.mediaShuffleButton.setIcon(QtGui.QIcon(":/icons/icons/cil-infinity.png"))
        self.mode_random = not self.mode_random

    def handle_player_lock(self):
        print("Player lock button clicked")
        self.player_locked = not self.player_locked
        if self.player_locked:
            self.playerLockButton.setIcon(
                QtGui.QIcon(":/icons/icons/cil-lock-unlocked.png")
            )
        else:
            self.playerLockButton.setIcon(
                QtGui.QIcon(":/icons/icons/cil-lock-locked.png")
            )
        self.volumeSlider.setEnabled(not self.player_locked)
        self.playbackProgress.setEnabled(not self.player_locked)
        self.mediaPlayPauseButton.setEnabled(not self.player_locked)
        self.mediaPreviousButton.setEnabled(not self.player_locked)
        self.mediaNextButton.setEnabled(not self.player_locked)
        self.mediaRepeatButton.setEnabled(not self.player_locked)
        self.mediaShuffleButton.setEnabled(not self.player_locked)
        self.volumeSlider.setEnabled(not self.player_locked)
        self.fileOpenerButton.setEnabled(not self.player_locked)
        self.fileOpenerButton.setEnabled(not self.player_locked)

    def handle_volume_slider(self, value):
        self.mediaPlay.setVolume(value)
        self.current_volume = value

    def seek_media(self):
        self.mediaPlay.setPosition(self.playbackProgress.value() * 1000)

    def update_slider_position(self, value):
        if abs(value * 1000 - self.mediaPlay.position()) > 1000:
            self.mediaPlay.setPosition(value * 1000)

    def update_position(self, position):
        self.playbackProgress.setValue(int(position / 1000))
        self.update_time_label(position)

    def update_duration(self, duration):
        self.playbackProgress.setRange(0, int(duration / 1000))
        self.mediaLenghtLabel.setText(self.format_time(duration))
        self.update_time_label(0)

    def update_time_label(self, position):
        self.playbackTimeLabel.setText(self.format_time(position))

    def seek_playback_by(self, seconds):
        current_position = self.mediaPlay.position()
        new_position = current_position + (seconds * 1000)
        if new_position < 0:
            new_position = 0
        elif new_position > self.mediaPlay.duration():
            new_position = self.mediaPlay.duration()
        self.mediaPlay.setPosition(new_position)

    def format_time(self, ms):
        seconds = (ms / 1000) % 60
        minutes = (ms / (1000 * 60)) % 60
        hours = (ms / (1000 * 60 * 60)) % 24
        if int(hours) > 0:
            return "%02d:%02d:%02d" % (hours, minutes, seconds)
        else:
            return "%02d:%02d" % (minutes, seconds)

    def handle_close_button(self):
        print("Close button clicked")
        QtWidgets.QApplication.instance().quit()

    def handle_minimize_button(self):
        print("Minimize button clicked")
        MainWindow.showMinimized()

    def handle_file_opener(self):
        print("File opener button clicked")
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Folder")
        if directory:
            self.media_files = []
            supported_formats = self.audio_formats + self.video_formats
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if any(file.endswith(ext) for ext in supported_formats):
                        file_path = os.path.join(root, file)
                        self.media_files.append(file_path)
                        self.mediaTitle.setText("Added %s..." % file_path[:25])
                        print(f"Added file to playlist: {file_path}")
                if len(self.media_files):
                    self.play_media_file(self.media_files[0])
                else:
                    self.mediaTitle.setText("No Media Files!")
            self.current_media_file = self.media_files[0] if self.media_files else None

    def play_media_file(self, file_path):
        self.mediaPlay.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(file_path)))
        self.mediaPlay.pause()
        if self.mediaPlay.mediaStatus() == QMediaPlayer.NoMedia:
            print(f"Failed to set media source: {file_path}")
        else:
            self.mediaPlayPauseButton.setIcon(
                QtGui.QIcon(":/icons/icons/cil-media-pause.png")
            )
            self.mediaPlay.error.connect(self.handle_media_error)
        if MainWindow.size().height() > 100:
            self.initial_size = MainWindow.size()
        if any(file_path.endswith(audioFormat) for audioFormat in self.audio_formats):
            self.mediaPlay.setVideoOutput(None)
            self.VideoPlayer.setVisible(False)
            self.frame.hide()
            MainWindow.setMinimumSize(480, 50)
            MainWindow.resize(500, 50)
        elif any(file_path.endswith(videoFormat) for videoFormat in self.video_formats):
            self.mediaPlay.setVideoOutput(self.VideoPlayer)
            self.VideoPlayer.setVisible(True)
            MainWindow.setMinimumSize(480, 320)
            MainWindow.resize(self.initial_size)
        self.mediaPlay.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(file_path)))
        self.mediaTitle.setText(os.path.basename(file_path))
        self.videoTitleLabel.setText(os.path.basename(file_path))
        self.mediaPlay.play()
        self.mediaPlayPauseButton.setIcon(
            QtGui.QIcon(":/icons/icons/cil-media-pause.png")
        )

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        new_files_added = False
        for url in urls:
            file_path = url.toLocalFile()
            if any(file_path.endswith(ext) for ext in self.audio_formats + self.video_formats):
                if file_path not in self.media_files:
                    self.media_files.append(file_path)
                    new_files_added = True
                    self.mediaTitle.setText(f"Added {os.path.basename(file_path)[:25]}...")
                    print(f"Added file to playlist: {file_path}")
                else:
                    print(f"File {file_path} already exists in the playlist")
        if new_files_added:
            self.mediaTitle.setText(f"Added {os.path.basename(file_path)[:25]}...")
            self.resetLabel.start(2000)
        if not self.current_media_file and self.media_files:
            self.play_media_file(self.media_files[0])
            self.current_media_file = self.media_files[0]
        if not self.media_files:
            self.mediaTitle.setText("No Media Files!")

    def reset_media_title(self):
        if self.current_media_file:
            self.mediaTitle.setText(os.path.basename(self.current_media_file))

    def handle_media_error(self):
        print(f"Media error: {self.mediaPlay.errorString()}")
        msg_box = QtWidgets.QMessageBox()
        msg_box.setIcon(QtWidgets.QMessageBox.Critical)
        msg_box.setWindowTitle("Media Error")
        msg_box.setText("Fatal Error!")
        msg_box.setInformativeText(self.mediaPlay.errorString())
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Close)
        msg_box.exec_()

import res_rc

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    MainWindow = CustomMainWindow(ui)
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
