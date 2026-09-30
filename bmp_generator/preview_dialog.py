# -*- coding: utf-8 -*-
# 预览对话框 —— 生成前展示缩略图供用户确认

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QScrollArea, QWidget,
                             QProgressBar, QApplication)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage

from bmp_generator.core import get_generator
from PIL import Image as PILImage


class PreviewWorker(QThread):
    thumbnail_ready = pyqtSignal(int, object)  # (index, PIL Image)
    preview_finished = pyqtSignal()

    def __init__(self, jobs, parent=None):
        super(PreviewWorker, self).__init__(parent)
        self._jobs = jobs

    def run(self):
        for idx, (name, params, extras) in enumerate(self._jobs):
            gen_fn = get_generator(name)
            if gen_fn:
                try:
                    if name == u"灰阶过渡":
                        img = gen_fn(params, None, _preview=True,
                                     r_checked=extras.get("r_checked", True),
                                     g_checked=extras.get("g_checked", True),
                                     b_checked=extras.get("b_checked", True))
                    else:
                        img = gen_fn(params, None, _preview=True)
                    if img:
                        self.thumbnail_ready.emit(idx, img)
                except Exception as e:
                    print("Preview error for %s: %s" % (name, e))
        self.preview_finished.emit()


class PreviewDialog(QDialog):
    generate_requested = pyqtSignal()

    def __init__(self, jobs, name_map, parent=None):
        super(PreviewDialog, self).__init__(parent)
        self._jobs = jobs
        self._name_map = name_map
        self.setWindowTitle(u"图片预览")
        self.setMinimumSize(640, 420)
        self.resize(680, 500)

        layout = QVBoxLayout(self)

        scroll = QScrollArea(self)
        scroll.setWidgetResizable(True)
        self._grid_widget = QWidget()
        self._grid = QGridLayout(self._grid_widget)
        self._grid.setSpacing(10)
        scroll.setWidget(self._grid_widget)
        layout.addWidget(scroll)

        self._progress = QProgressBar(self)
        self._progress.setRange(0, len(jobs))
        self._progress.setValue(0)
        layout.addWidget(self._progress)

        btn_layout = QHBoxLayout()
        self._gen_btn = QPushButton(u"开始生成", self)
        self._cancel_btn = QPushButton(u"关闭", self)
        btn_layout.addStretch()
        btn_layout.addWidget(self._gen_btn)
        btn_layout.addWidget(self._cancel_btn)
        layout.addLayout(btn_layout)

        self._gen_btn.clicked.connect(self.accept)
        self._cancel_btn.clicked.connect(self.reject)

        self._labels = []
        for idx, (name, params, _) in enumerate(jobs):
            display = self._name_map.get(name, name)
            label_w = QLabel(display, self._grid_widget)
            label_w.setAlignment(Qt.AlignCenter)
            label_w.setMinimumSize(130, 130)
            label_w.setStyleSheet("border: 1px solid gray; padding: 4px;")
            self._labels.append(label_w)
            self._grid.addWidget(label_w, idx // 4, idx % 4)

        self._worker = PreviewWorker(jobs, self)
        self._worker.thumbnail_ready.connect(self._on_thumbnail)
        self._worker.preview_finished.connect(self._on_finished)
        self._worker.start()

    def _on_thumbnail(self, idx, pil_img):
        pil_img = pil_img.convert("RGB")
        data = pil_img.tobytes("raw", "RGB")
        qimg = QImage(data, pil_img.width, pil_img.height, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg).scaled(
            120, 120, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self._labels[idx].setPixmap(pixmap)
        self._progress.setValue(self._progress.value() + 1)

    def _on_finished(self):
        self._progress.setValue(len(self._jobs))
