# coding:utf-8
import sys
from hashlib import md5
from uuid import uuid1
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QStackedWidget, QVBoxLayout, QFrame,QLabel

from qfluentwidgets import (BreadcrumbBar, FlowLayout, setFont, setTheme,
                            Theme, LineEdit, PrimaryToolButton, SubtitleLabel,
                            FluentIcon, ScrollArea, SmoothScrollArea)


class ImageItem(QWidget):

    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.setObjectName(str(uuid1()))
        self.viewLayout = QVBoxLayout(self)
        self.imageBox = QLabel(self)
        self.imageBox.setFixedSize(155, 155)
        self.setStyleSheet('''
            QLabel {
                ''' 
                +f'''
                background: #7f{md5(str(uuid1()).encode('utf-8')).hexdigest()[:6]};
                '''
                +'''
                border-radius: 10px;
            }
        ''')
        self.viewLayout.addWidget(self.imageBox)
        self.setLayout(self.viewLayout)

    def apply(self, image):
        self.imageBox.setPixmap(image)

class ImageContainer(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.view = QFrame(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.scrollArea = SmoothScrollArea(self)
        self.hBoxLayout = QHBoxLayout(self.view)
        self.scrollWidget = QWidget(self.scrollArea)
        self.flowLayout = FlowLayout(self.scrollWidget, needAni=True, isTight=True)
        self._set_layout()
        
    def addWidget(self, widget):
        self.flowLayout.addWidget(widget)
        
    def clear(self):
        for i in reversed(range(self.flowLayout.count())):
            widget = self.flowLayout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
            else:
                layout = self.flowLayout.itemAt(i).layout()
                if layout:
                    layout.deleteLater()
                    
    def setSpacing(self, spacing):
        self.flowLayout.setSpacing(spacing)
        
    def _set_layout(self):
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setViewportMargins(0, 5, 0, 5)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.addWidget(self.view)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.scrollArea)
        # self.hBoxLayout.addWidget(self.infoPanel, 0, Qt.AlignRight)

        self.flowLayout.setVerticalSpacing(8)
        self.flowLayout.setHorizontalSpacing(8)
        self.flowLayout.setContentsMargins(8, 3, 8, 8)

        


# 瀑布流布局
class WaterfallLayout(ScrollArea):

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent)
        self.setStyleSheet('background:#0fffffff')
        self._layout = QVBoxLayout()
        self.scrollWidget = QWidget(self._layout.widget())
        
        # self.flowLayout = FlowLayout(self.scrollWidget,needAni=True, isTight=True)
        self.flowLayout = ImageContainer(self.scrollWidget)
        self.titleLabel = SubtitleLabel(kwargs.get('title', ''),
                                        self._layout.widget())
        self.scrollWidget.setStyleSheet('''
            QScrollArea {
                background-color: transparent;
                border: none;
            }
        ''')
        self.titleLabel.setFixedHeight(40)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        # self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        test = [ImageItem(self.flowLayout.flowLayout.widget()) for x in range(100)]
        for u in test:
            self.addWidget(u)

        self._layout.addWidget(self.titleLabel)
        self._layout.addWidget(self.scrollWidget, 1)
        self.scrollWidget.setStyleSheet('background:transparent;')
        # self.scrollWidget.setLayout(self.flowLayout)
        self.setLayout(self._layout)
        # self.setWidget(self._widget)

    def addWidget(self, widget):
        self.flowLayout.addWidget(widget)

    def clear(self):
        for i in reversed(range(self.vBoxLayout.count())):
            widget = self.flowLayout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
            else:
                layout = self.flowLayout.itemAt(i).layout()
                if layout:
                    layout.deleteLater()


class UI(QWidget):

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.setStyleSheet('UI{background:rgb(32,32,32)}')

        self.breadcrumbBar = BreadcrumbBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.lineEdit = LineEdit(self)
        self.addButton = PrimaryToolButton(FluentIcon.SEARCH, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.lineEditLayout = QHBoxLayout()

        self.addButton.clicked.connect(
            lambda: self.addInterface(self.lineEdit.text()))
        self.lineEdit.returnPressed.connect(
            lambda: self.addInterface(self.lineEdit.text()))
        self.lineEdit.setPlaceholderText(
            'Enter the character you\'re looking for...')

        # NOTE: adjust the size of breadcrumb item
        setFont(self.breadcrumbBar, 20)
        self.breadcrumbBar.setSpacing(20)
        self.breadcrumbBar.currentItemChanged.connect(self.switchInterface)

        self.addInterface('Home')

        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.vBoxLayout.addWidget(self.breadcrumbBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.addLayout(self.lineEditLayout)

        self.lineEditLayout.addWidget(self.lineEdit, 1)
        self.lineEditLayout.addWidget(self.addButton)
        self.resize(800, 600)

    def addInterface(self, text: str):
        if not text:
            return

        s = WaterfallLayout(parent=self.stackedWidget, title=text)
        s.setObjectName(str(uuid1()))
        self.lineEdit.clear()
        self.stackedWidget.addWidget(s)
        self.stackedWidget.setCurrentWidget(s)

        # !IMPORTANT: add breadcrumb item
        self.breadcrumbBar.addItem(s.objectName(), text)

    def switchInterface(self, objectName):
        self.stackedWidget.setCurrentWidget(
            self.findChild(WaterfallLayout, objectName))


def start_up():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = UI()
    w.setFixedSize(800, 600)
    w.show()
    app.exec_()


if __name__ == '__main__':
    start_up()
