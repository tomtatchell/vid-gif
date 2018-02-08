import sys
import vidgif
import pexpect
from os import path

from PyQt5.QtWidgets import (QWidget, QMainWindow, QProgressBar,
                             qApp, QMessageBox, QApplication, QLabel,
                             QSizePolicy, QGridLayout)
from PyQt5.QtGui import QPalette, QImage, QBrush
from PyQt5.QtCore import Qt, QSize


class BackgroundWidget(QWidget):
    def __init__(self):
        super(BackgroundWidget, self).__init__()
        palette = QPalette()
        oImage = QImage('BBLOGO.png')
        sImage = oImage.scaled(QSize(202, 233))
        palette.setBrush(QPalette.Background, QBrush(sImage))
        self.setAutoFillBackground(True)
        self.setPalette(palette)


class MainWindow(QMainWindow):
    # TODO: Add text elements to UI
    # TODO: Add GIF output name override
    # TODO: Add Output Resolution - either exact value or reduce by x amount
    # TODO: Add compression level options
    # TODO: Add go button
    # TODO: Add text to represent the video file dragged in
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setAcceptDrops(True)

    def initUI(self):
        self._widget = BackgroundWidget()
        self.setCentralWidget(self._widget)

        self.setWindowTitle('vid-gif')
        self.setGeometry(250, 100, 404, 466)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(101, 80, 200, 30)
        self.completed = 0



    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            e.acceptProposedAction()
        else:
            super(MainWindow, self).dragMoveEvent(e)

    def dragMoveEvent(self, e):
        super(MainWindow, self).dragMoveEvent(e)

    def dropEvent(self, e):
        if e.mimeData().hasFormat('text/uri-list'):
            if len(e.mimeData().urls()) == 1:
                src = e.mimeData().urls()[0].path()  # get the path
                if path.isfile(src):  # if it's a file
                    print("getting file info...")
                    src_w, src_h, src_fps, src_frames = vidgif.get_info(src)
                    print("got file info:\n"
                          "width: {w}\n"
                          "height: {h}\n"
                          "fps: {fps}\n"
                          "frames: {frames}".format(w=src_w, h=src_h, fps=src_fps, frames=src_frames))
                    print("generating palette...")
                    vidgif.palette_gen(src, src_w, src_fps)
                    print("generated palette")
                    cmd = 'ffmpeg -y -i {src} -i {path}/.palette.png -filter_complex ' \
                          'fps={fps},scale={scale}' \
                          ':-1:flags=lanczos[x];[x][1:v]paletteuse {gif_file_path}.gif'.format(
                            src=src, path=path.dirname(src),
                            fps=src_fps, scale=src_w,
                            gif_file_path=path.splitext(src)[0])
                    thread = pexpect.spawn(cmd)
                    print("starting conversion...")
                    cpl = thread.compile_pattern_list([
                        pexpect.EOF,
                        'frame= \s*\d+',
                        '(.+)',
                    ])
                    while True:
                        i = thread.expect_list(cpl, timeout=None)
                        if i == 0:  # EOF
                            print("the sub process exited")
                            break
                        elif i == 1:
                            frame_number_bytes = thread.match.group(0)
                            fn_str = frame_number_bytes.decode("utf-8")
                            formatted_fn = fn_str.rsplit('= ', 1)[1]
                            percentage = (int(formatted_fn.lstrip()) / int(src_frames)) * 100
                            print("frame: {} of {}  --  {}%".format(formatted_fn,
                                                                    src_frames,
                                                                    int(percentage)))
                            self.progress.setValue(percentage)
                            qApp.processEvents()
                    thread.close()
                    vidgif.housekeeping(src)
                    self.progress.setValue(0)
        else:
            super(MainWindow, self).dragMoveEvent(e)

    def mousePressEvent(self, event):
        self.offset = event.pos()

    def mouseMoveEvent(self, event):
        x = event.globalX()
        y = event.globalY()
        x_w = self.offset.x()
        y_w = self.offset.y()
        self.move(x - x_w, y - y_w)

    def closeEvent(self, e):
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            app.quit()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.closeEvent(e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec_()