import sys, os, io, ctypes
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QSizePolicy, QVBoxLayout, QLineEdit, QLabel
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QPoint, QSize, QUrl
from PyQt6.QtGui import QPixmap, QIcon, QImage
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from pathlib import Path
import qrcode

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

def set_win_app_id():
    if sys.platform == 'win32':
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("island")
        except AttributeError:
            pass

class MainWindow():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.player = QMediaPlayer()
        self.output = QAudioOutput()

        self.player.setAudioOutput(self.output)

        self.output.setVolume(1)

        self.island_width = 250
        self.island_height = 25

        self.screen = QApplication.primaryScreen()
        self.geometry = self.screen.geometry()

        self.width = self.geometry.width()

        self.window = QWidget()
        self.window.resize(self.island_width, self.island_height)

        self.layout = QVBoxLayout(self.window)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.window.move((int(self.width / 2)) - int(self.island_width / 2), 0)

        self.window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.window.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.create_island()
        self.layout.addWidget(self.island)

        self.is_open = False
        self.patch = None

        self.all_track = []
        self.n = 0
        self.max_n = None

        self.player_st = False

        self.clipboard = QApplication.clipboard()
        self.clipboard.dataChanged.connect(self.update_buffer_history)

        self.pre_last_copy_txt = ""
        self.last_copy_txt = ""

        self.island.clicked.connect(self.open_island)

        self.main_menu()

        #patch music menu
        self.player_patch_menu()
        self.music_btn.clicked.connect(self.open_player_patch_menu)
        self.close_m_btn.clicked.connect(self.close_player_patch_menu)

        #player menu
        self.player_menu()
        self.m_ready_btn.clicked.connect(self.save_patch)
        self.close_music_btn.clicked.connect(self.close_player)
        self.m_name.clicked.connect(self.open_island)

        self.play_btn.clicked.connect(self.play)
        self.next_btn.clicked.connect(self.next_track)
        self.previous_btn.clicked.connect(self.previous_track)

        #qr_menu
        self.qr_menu()
        self.snd_btn_qr.clicked.connect(self.qr_generate)
        self.qr_btn.clicked.connect(self.qr_menu_open)
        self.close_btn_qr.clicked.connect(self.qr_menu_close)

        #buffer menu
        self.buffer_menu()
        self.buffer_btn.clicked.connect(self.open_buffer_menu)

        self.exit_buffer_menu.clicked.connect(self.close_buffer_menu)
        self.pre_last_copy.clicked.connect(self.savePre_from_buff)
        self.last_copy.clicked.connect(self.saveLast_from_buff)

        self.window.show()
        sys.exit(self.app.exec())

    def create_island(self):
        self.island = QPushButton()
        self.island.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.island.setStyleSheet("""
            background-color: black;
            border-bottom-left-radius: 15px; 
            border-bottom-right-radius: 15px;
        """)

    def open_island(self):
        self.anim = QPropertyAnimation(self.window, b"size")
        self.anim.setDuration(200)
        self.anim.setStartValue(QSize(self.island_width, self.island_height))
        self.anim.setEndValue(QSize(self.island_width, self.island_height + 50))

        self.anim_close = QPropertyAnimation(self.window, b"size")
        self.anim_close.setDuration(200)
        self.anim_close.setStartValue(QSize(self.island_width, self.island_height + 50))
        self.anim_close.setEndValue(QSize(self.island_width, self.island_height))

        if not self.is_open:
            self.anim.start()
            self.is_open = True

        else:
            self.anim_close.start()
            self.is_open = False

    def main_menu(self):
        self.qr_btn = QPushButton(self.window)
        self.qr_btn.setGeometry(10, 25, 35, 35)
        self.qr_btn.setStyleSheet("""
            border-radius: 5px;
            background-color: white;
        """)
        self.qr_btn.setIcon(QIcon("icons/icon_qr.png"))

        self.music_btn = QPushButton(self.window)
        self.music_btn.setGeometry(50, 25, 35, 35)
        self.music_btn.setStyleSheet("""
            border-radius: 5px;
            background-color: white; 
        """)
        self.music_btn.setIcon(QIcon("icons/music_icn.png"))

        self.buffer_btn = QPushButton(self.window)
        self.buffer_btn.setGeometry(90, 25, 35, 35)
        self.buffer_btn.setStyleSheet("""
                    border-radius: 5px;
                    background-color: white; 
                """)
        self.buffer_btn.setIcon(QIcon("icons/buffer.png"))

        self.all_menu_btn = self.music_btn, self.qr_btn, self.buffer_btn

    def qr_menu(self):
        self.line_qr = QLineEdit(self.window)
        self.line_qr.setPlaceholderText("enter text:")
        self.line_qr.setGeometry(10, 25, 150, 25)
        self.line_qr.setStyleSheet("""
                        background-color: black;
                        color: white;
                        border: 1px solid white;
                        border-radius: 5px;
                    """)

        self.snd_btn_qr = QPushButton("create", self.window)
        self.snd_btn_qr.setGeometry(165, 25, 40, 25)
        self.snd_btn_qr.setStyleSheet("""
                        background-color: green;
                        border: 1px solid green;
                        border-radius: 5px;
                        color: white;
                    """)

        self.close_btn_qr = QPushButton(self.window)
        self.close_btn_qr.setGeometry(210, 25, 25, 25)
        self.close_btn_qr.setStyleSheet("""
                        background-color: white;
                        border: 1px solid white;
                        border-radius: 5px;
                    """)
        self.close_btn_qr.setIcon(QIcon("icons/close_icn.png"))

        self.all_qr_menu_btn = self.close_btn_qr, self.snd_btn_qr, self.line_qr

        for a in self.all_qr_menu_btn:
            a.hide()

    def qr_menu_open(self):
        for a in self.all_menu_btn:
            a.hide()

        for a in self.all_qr_menu_btn:
            a.show()

    def qr_menu_close(self):
        for a in self.all_qr_menu_btn:
            a.hide()

        for a in self.all_menu_btn:
            a.show()

    def qr_generate(self):
        self.txt = self.line_qr.text()
        self.img = qrcode.make(self.txt)

        self.line_qr.clear()

        self.buffer = io.BytesIO()
        self.img.save(self.buffer, format="PNG")

        self.qr_window = QLabel()
        self.qr_window.setWindowTitle("QR")
        self.qr_window.setWindowIcon(QIcon("icons/icon_qr.png"))

        self.pixmap = QPixmap()
        self.pixmap.loadFromData(self.buffer.getvalue())

        self.qr_window.setPixmap(self.pixmap)
        self.qr_window.resize(300, 300)
        self.qr_window.show()

    def player_patch_menu(self):
        self.patch_line = QLineEdit(self.window)
        self.patch_line.setPlaceholderText("enter folder patch:")
        self.patch_line.setGeometry(10, 25, 150, 25)

        self.m_ready_btn = QPushButton("send", self.window)
        self.m_ready_btn.setGeometry(165, 25, 40, 25)

        self.close_m_btn = QPushButton(self.window)
        self.close_m_btn.setGeometry(210, 25, 30, 25)

        self.close_m_btn.setStyleSheet("""
            background-color: white;
            border: 1px solid white;
            border-radius: 5px;
        """)
        self.close_m_btn.setIcon(QIcon("icons/close_icn.png"))

        self.patch_line.setStyleSheet("""
            background-color: black;
            color: white;
            border: 1px solid white;
            border-radius: 5px;
        """)

        self.m_ready_btn.setStyleSheet("""
            background-color: green;
            border: 1px solid green;
            border-radius: 5px;
            color: white;
        """)

        self.AllPlayerPatchBtn = self.patch_line, self.m_ready_btn, self.close_m_btn

        for a in self.AllPlayerPatchBtn:
            a.hide()

    def player_menu(self):
        self.play_btn = QPushButton(self.window)
        self.play_btn.setGeometry(110, 25, 30, 30)
        self.play_btn.setIcon(QIcon("icons/play.png"))
        self.play_btn.setStyleSheet("""
            background-color:white;
            border: 1px solid white;
            border-radius: 5px;
        """)

        self.next_btn = QPushButton(self.window)
        self.next_btn.setGeometry(150, 25, 30, 30)
        self.next_btn.setIcon(QIcon("icons/next.png"))
        self.next_btn.setStyleSheet("""
            background-color:white;
            border: 1px solid white;
            border-radius: 5px;
        """)

        self.previous_btn = QPushButton(self.window)
        self.previous_btn.setGeometry(70, 25, 30, 30)
        self.original = QImage("icons/next.png")

        self.mirror = self.original.mirrored(True, False)

        self.pixmap = QPixmap.fromImage(self.mirror)

        self.previous_btn.setIcon(QIcon(self.pixmap))
        self.previous_btn.setStyleSheet("""
            background-color:white;
            border: 1px solid white;
            border-radius: 5px;
        """)

        self.m_name = QPushButton(self.window)
        self.m_name.setGeometry(10, 5, 230, 15)
        self.m_name.setStyleSheet("""
            background-color: darkblue;
            color:white;
            border-radius:5px;
        """)

        self.close_music_btn = QPushButton(self.window)
        self.close_music_btn.setGeometry(10, 25, 30, 30)
        self.close_music_btn.setStyleSheet("""
            background-color: white;
            border: 1px solid white;
            border-radius: 5px;
        """)
        self.close_music_btn.setIcon(QIcon("icons/close_icn.png"))

        self.AllPlayerBtn = self.close_music_btn, self.play_btn, self.previous_btn, self.next_btn, self.m_name

        for a in self.AllPlayerBtn:
            a.hide()

    def open_player_patch_menu(self):
        if self.patch == None:
            for a in self.all_menu_btn:
                a.hide()

            for a in self.AllPlayerPatchBtn:
                a.show()
        else:
            self.open_player()

    def close_player_patch_menu(self):
        for a in self.all_menu_btn:
            a.show()

        for a in self.AllPlayerPatchBtn:
            a.hide()

    def open_player(self):
        for a in self.all_menu_btn:
            a.hide()

        for a in self.AllPlayerBtn:
            a.show()

    def save_patch(self):
        if self.patch_line.text() != "" and Path(self.patch_line.text()).exists():
            self.patch = self.patch_line.text()
            self.close_player_patch_menu()
            self.open_player()

            for m in Path(str(self.patch)).iterdir():
                self.all_track.append(m)

            self.max_n = len(self.all_track)
            self.set_track_name()

            self.file_url = QUrl.fromLocalFile(str(self.all_track[self.n]))
            self.player.setSource(self.file_url)

        else:
            self.patch_line.clear()

    def close_player(self):
        for a in self.AllPlayerBtn:
            a.hide()

        for a in self.all_menu_btn:
            a.show()

        self.play_btn.setIcon(QIcon("icons/play.png"))
        self.player_st = False

        self.player.pause()

    def set_track_name(self):
        self.m_name.setText(self.all_track[self.n].name)

    def play(self):
        if not self.player_st:
            self.play_btn.setIcon(QIcon("icons/stop.png"))

            self.player.play()

            self.player_st = True

        else:
            self.player.pause()

            self.play_btn.setIcon(QIcon("icons/play.png"))

            self.player_st = False

    def next_track(self):
        if self.n != self.max_n - 1:
            self.n += 1

            self.set_track_name()

            self.file_url = QUrl.fromLocalFile(str(self.all_track[self.n]))
            self.player.setSource(self.file_url)

            if self.player_st:
                self.player.play()

            else:
                self.player.stop()

        else:
            self.n = 0

            self.set_track_name()

            self.file_url = QUrl.fromLocalFile(str(self.all_track[self.n]))
            self.player.setSource(self.file_url)

            if self.player_st:
                self.player.play()

            else:
                self.player.stop()

    def previous_track(self):
        if self.n != 0:
            self.n -= 1

            self.set_track_name()

            self.file_url = QUrl.fromLocalFile(str(self.all_track[self.n]))
            self.player.setSource(self.file_url)

            if self.player_st:
                self.player.play()

            else:
                self.player.stop()

        else:
            self.n = self.max_n - 1

            self.set_track_name()

            self.file_url = QUrl.fromLocalFile(str(self.all_track[self.n]))
            self.player.setSource(self.file_url)

            if self.player_st:
                self.player.play()

            else:
                self.player.stop()

    def buffer_menu(self):
        self.pre_last_copy = QPushButton(self.window)
        self.pre_last_copy.setGeometry(10, 25, 200, 15)
        self.pre_last_copy.setText(self.pre_last_copy_txt)

        self.last_copy = QPushButton(self.window)
        self.last_copy.setGeometry(10, 45, 200, 15)
        self.last_copy.setText(self.last_copy_txt)

        self.exit_buffer_menu = QPushButton(self.window)
        self.exit_buffer_menu.setGeometry(215, 25, 25, 35)

        self.exit_buffer_menu.setIcon(QIcon("icons/close_icn.png"))

        self.all_buffer_btn = self.pre_last_copy, self.last_copy, self.exit_buffer_menu
        self.all_buffer_cop = self.pre_last_copy, self.last_copy

        for a in self.all_buffer_cop:
            a.setStyleSheet("""
                border-radius: 5px;
                background-color: darkblue;
                color: white;
            """)

        self.exit_buffer_menu.setStyleSheet("""
            border-radius: 5px;
            background-color: lightgray;
            color: black;
        """)

        for a in self.all_buffer_btn:
            a.hide()

    def open_buffer_menu(self):
        for a in self.all_menu_btn:
            a.hide()

        for a in self.all_buffer_btn:
            a.show()

    def close_buffer_menu(self):
        for a in self.all_menu_btn:
            a.show()

        for a in self.all_buffer_btn:
            a.hide()

    def update_buffer_history(self):
        self.text = self.clipboard.text()
        self.pre = self.last_copy_txt

        if self.pre != self.text:
            self.last_copy_txt = self.text

            self.pre_last_copy.setText(self.pre)
            self.last_copy.setText(self.last_copy_txt)

    def savePre_from_buff(self):
        self.clipboard.setText(self.pre_last_copy.text())

    def saveLast_from_buff(self):
        self.clipboard.setText(self.last_copy.text())

if __name__ == "__main__":
    set_win_app_id()
    MainWindow()
