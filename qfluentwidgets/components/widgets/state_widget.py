# coding:utf-8
from typing import Union

from PySide6.QtCore import Qt, Signal, Property, QPropertyAnimation, QEvent
from PySide6.QtGui import QColor, QIcon, QPainter, QPainterPath, QLinearGradient
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy

from ...common.icon import FluentIcon, FluentIconBase
from ...common.style_sheet import isDarkTheme, themeColor
from .button import PushButton
from .icon_widget import IconWidget
from .label import BodyLabel, CaptionLabel, SubtitleLabel
from .progress_ring import IndeterminateProgressRing


class EmptyStateWidget(QWidget):
    """ Empty state widget

    Constructors
    ------------
    * EmptyStateWidget(`parent`: QWidget = None)
    * EmptyStateWidget(`title`: str, `content`: str = '', `parent`: QWidget = None)
    """

    actionClicked = Signal()

    def __init__(self, title='', content='', parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(FluentIcon.DOCUMENT, self)
        self.titleLabel = SubtitleLabel(title, self)
        self.contentLabel = BodyLabel(content, self)
        self.actionButton = PushButton(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.buttonLayout = QHBoxLayout()

        self.__initWidget()

    def __initWidget(self):
        self.iconWidget.setFixedSize(56, 56)
        self.contentLabel.setWordWrap(True)
        self.contentLabel.setAlignment(Qt.AlignCenter)
        self.contentLabel.setTextColor(QColor(96, 96, 96), QColor(200, 200, 200))
        self.actionButton.hide()
        self.actionButton.clicked.connect(self.actionClicked)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(24, 24, 24, 24)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignCenter)
        self.vBoxLayout.addSpacing(4)
        self.vBoxLayout.addLayout(self.buttonLayout)

        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonLayout.addStretch(1)
        self.buttonLayout.addWidget(self.actionButton)
        self.buttonLayout.addStretch(1)

        self.setMinimumHeight(180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def setIcon(self, icon: Union[str, QIcon, FluentIconBase]):
        """ set the state icon """
        self.iconWidget.setIcon(icon)

    def setTitle(self, title: str):
        """ set title text """
        self.titleLabel.setText(title)

    def setContent(self, content: str):
        """ set content text """
        self.contentLabel.setText(content)

    def setActionText(self, text: str):
        """ set action button text """
        self.actionButton.setText(text)
        self.actionButton.setVisible(bool(text))


class ErrorStateWidget(EmptyStateWidget):
    """ Error state widget """

    def __init__(self, title='', content='', parent=None):
        super().__init__(title, content, parent)
        self.setIcon(FluentIcon.CANCEL)
        self.iconWidget.setFixedSize(52, 52)


class LoadingOverlay(QWidget):
    """ Loading overlay widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.ring = IndeterminateProgressRing(self)
        self.titleLabel = SubtitleLabel(self.tr('Loading'), self)
        self.contentLabel = CaptionLabel('', self)

        self.vBoxLayout = QVBoxLayout(self)
        self.__initWidget()

        if parent:
            parent.installEventFilter(self)
            self.resize(parent.size())

    def __initWidget(self):
        self.setAttribute(Qt.WA_StyledBackground)
        self.setAutoFillBackground(False)
        self.ring.setFixedSize(48, 48)
        self.contentLabel.setAlignment(Qt.AlignCenter)
        self.contentLabel.setTextColor(QColor(96, 96, 96), QColor(200, 200, 200))

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.setContentsMargins(24, 24, 24, 24)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.ring, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignCenter)

        self.hide()

    def setTitle(self, title: str):
        """ set title text """
        self.titleLabel.setText(title)

    def setContent(self, content: str):
        """ set content text """
        self.contentLabel.setText(content)

    def setLoading(self, isLoading: bool):
        """ set whether the overlay is visible and spinning """
        self.setVisible(isLoading)
        if isLoading:
            self.raise_()
            self.ring.start()
        else:
            self.ring.stop()

    def isLoading(self):
        return self.isVisible()

    def eventFilter(self, obj, e):
        if obj is self.parent() and e.type() == QEvent.Resize:
            self.resize(obj.size())

        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(32, 32, 32, 120) if isDarkTheme() else QColor(255, 255, 255, 210))
        painter.drawRect(self.rect())


class SkeletonWidget(QWidget):
    """ Skeleton loading placeholder """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._shimmerPosition = -0.4
        self._rowCount = 3
        self._animated = True

        self.ani = QPropertyAnimation(self, b'shimmerPosition', self)
        self.ani.setStartValue(-0.4)
        self.ani.setEndValue(1.4)
        self.ani.setDuration(1400)
        self.ani.setLoopCount(-1)

        self.setMinimumSize(240, 96)
        self.start()

    def getShimmerPosition(self):
        return self._shimmerPosition

    def setShimmerPosition(self, value: float):
        self._shimmerPosition = value
        self.update()

    def rowCount(self):
        return self._rowCount

    def setRowCount(self, count: int):
        self._rowCount = max(1, count)
        self.update()

    def start(self):
        """ start shimmer animation """
        self._animated = True
        if self.ani.state() != QPropertyAnimation.Running:
            self.ani.start()

    def stop(self):
        """ stop shimmer animation """
        self._animated = False
        self.ani.stop()
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        baseColor = QColor(255, 255, 255, 28) if isDarkTheme() else QColor(0, 0, 0, 18)
        highlightColor = QColor(themeColor())
        highlightColor.setAlpha(34 if isDarkTheme() else 24)

        x, y = 8, 8
        avatar = min(56, max(36, self.height() - 32))
        painter.setBrush(baseColor)
        painter.drawRoundedRect(x, y, avatar, avatar, 8, 8)

        left = x + avatar + 16
        right = self.width() - 8
        rowHeight = 12
        rowGap = max(12, (avatar - self._rowCount * rowHeight) // max(1, self._rowCount - 1))

        path = QPainterPath()
        for i in range(self._rowCount):
            width = max(16, right - left)
            if i == self._rowCount - 1:
                width = int(width * 0.62)

            rectY = y + i * (rowHeight + rowGap)
            path.addRoundedRect(left, rectY, width, rowHeight, 6, 6)

        painter.setBrush(baseColor)
        painter.drawPath(path)

        if self._animated:
            gradient = QLinearGradient(0, 0, self.width(), 0)
            p = self._shimmerPosition
            gradient.setColorAt(max(0, min(1, p - 0.18)), QColor(0, 0, 0, 0))
            gradient.setColorAt(max(0, min(1, p)), highlightColor)
            gradient.setColorAt(max(0, min(1, p + 0.18)), QColor(0, 0, 0, 0))

            painter.setBrush(gradient)
            painter.drawRoundedRect(x, y, avatar, avatar, 8, 8)
            painter.drawPath(path)

    shimmerPosition = Property(float, getShimmerPosition, setShimmerPosition)
