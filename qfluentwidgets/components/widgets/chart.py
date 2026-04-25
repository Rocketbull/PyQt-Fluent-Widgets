# coding:utf-8
from enum import Enum
from typing import Iterable, List, Sequence, Tuple

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QBrush
from PySide6.QtWidgets import QWidget, QVBoxLayout

from ...common.style_sheet import isDarkTheme, themeColor
from .card_widget import SimpleCardWidget
from .label import CaptionLabel, StrongBodyLabel, SubtitleLabel


class ChartType(Enum):
    """ Chart type """

    LINE = "line"
    BAR = "bar"
    SCATTER = "scatter"


class ChartWidget(QWidget):
    """ Lightweight dependency-free chart widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._type = ChartType.LINE
        self._series = []  # type: List[Tuple[str, List[float]]]
        self._categories = []  # type: List[str]
        self._title = ''
        self._xLabel = ''
        self._yLabel = ''
        self.setMinimumSize(320, 220)

    def setChartType(self, chartType: ChartType):
        """ set chart type """
        self._type = chartType
        self.update()

    def setTitle(self, title: str):
        """ set chart title """
        self._title = title
        self.update()

    def setAxisLabels(self, xLabel: str, yLabel: str):
        """ set axis labels """
        self._xLabel = xLabel
        self._yLabel = yLabel
        self.update()

    def setCategories(self, categories: Iterable[str]):
        """ set x-axis categories """
        self._categories = list(categories)
        self.update()

    def setSeries(self, name: str, values: Sequence[float]):
        """ replace chart data with one series """
        self._series = [(name, [float(v) for v in values])]
        self.update()

    def addSeries(self, name: str, values: Sequence[float]):
        """ add a chart series """
        self._series.append((name, [float(v) for v in values]))
        self.update()

    def clear(self):
        """ clear chart data """
        self._series.clear()
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.transparent)

        if not self._series:
            self.__drawEmpty(painter)
            return

        rect = self.rect().adjusted(52, 38, -22, -44)
        self.__drawGrid(painter, rect)

        if self._type == ChartType.BAR:
            self.__drawBars(painter, rect)
        elif self._type == ChartType.SCATTER:
            self.__drawScatter(painter, rect)
        else:
            self.__drawLines(painter, rect)

        self.__drawLabels(painter, rect)

    def __colors(self):
        return [
            QColor(themeColor()),
            QColor(16, 124, 16),
            QColor(196, 43, 28),
            QColor(135, 100, 184),
            QColor(0, 153, 188),
        ]

    def __bounds(self):
        values = [v for _, series in self._series for v in series]
        low, high = min(values), max(values)
        if low == high:
            low -= 1
            high += 1

        padding = (high - low) * 0.08
        return low - padding, high + padding

    def __point(self, rect: QRectF, index: int, value: float, count: int, low: float, high: float):
        x = rect.left() if count <= 1 else rect.left() + index * rect.width() / (count - 1)
        y = rect.bottom() - (value - low) * rect.height() / (high - low)
        return x, y

    def __drawGrid(self, painter: QPainter, rect: QRectF):
        gridColor = QColor(255, 255, 255, 36) if isDarkTheme() else QColor(0, 0, 0, 24)
        axisColor = QColor(255, 255, 255, 92) if isDarkTheme() else QColor(0, 0, 0, 88)
        painter.setPen(QPen(gridColor, 1))

        for i in range(5):
            y = rect.top() + i * rect.height() / 4
            painter.drawLine(rect.left(), y, rect.right(), y)

        painter.setPen(QPen(axisColor, 1.2))
        painter.drawLine(rect.left(), rect.top(), rect.left(), rect.bottom())
        painter.drawLine(rect.left(), rect.bottom(), rect.right(), rect.bottom())

    def __drawLines(self, painter: QPainter, rect: QRectF):
        low, high = self.__bounds()
        colors = self.__colors()

        for seriesIndex, (_, values) in enumerate(self._series):
            if not values:
                continue

            path = QPainterPath()
            for i, value in enumerate(values):
                x, y = self.__point(rect, i, value, len(values), low, high)
                if i == 0:
                    path.moveTo(x, y)
                else:
                    path.lineTo(x, y)

            color = colors[seriesIndex % len(colors)]
            painter.setPen(QPen(color, 2.4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawPath(path)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            for i, value in enumerate(values):
                x, y = self.__point(rect, i, value, len(values), low, high)
                painter.drawEllipse(QRectF(x - 3, y - 3, 6, 6))

    def __drawScatter(self, painter: QPainter, rect: QRectF):
        low, high = self.__bounds()
        colors = self.__colors()

        for seriesIndex, (_, values) in enumerate(self._series):
            color = colors[seriesIndex % len(colors)]
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            for i, value in enumerate(values):
                x, y = self.__point(rect, i, value, len(values), low, high)
                painter.drawEllipse(QRectF(x - 4, y - 4, 8, 8))

    def __drawBars(self, painter: QPainter, rect: QRectF):
        low, high = self.__bounds()
        low = min(0, low)
        colors = self.__colors()
        groupCount = max(len(series) for _, series in self._series)
        groupWidth = rect.width() / max(1, groupCount)
        barWidth = groupWidth / (len(self._series) + 1)

        for seriesIndex, (_, values) in enumerate(self._series):
            color = colors[seriesIndex % len(colors)]
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            for i, value in enumerate(values):
                x = rect.left() + i * groupWidth + seriesIndex * barWidth + barWidth * 0.5
                y = rect.bottom() - (value - low) * rect.height() / (high - low)
                baseY = rect.bottom() - (0 - low) * rect.height() / (high - low)
                top, height = min(y, baseY), abs(baseY - y)
                painter.drawRoundedRect(QRectF(x, top, barWidth * 0.72, max(1, height)), 4, 4)

    def __drawLabels(self, painter: QPainter, rect: QRectF):
        textColor = QColor(255, 255, 255, 210) if isDarkTheme() else QColor(0, 0, 0, 180)
        painter.setPen(textColor)

        if self._title:
            painter.drawText(self.rect().adjusted(12, 8, -12, -8), Qt.AlignTop | Qt.AlignHCenter, self._title)

        low, high = self.__bounds()
        painter.drawText(8, int(rect.top() + 6), f'{high:.2f}')
        painter.drawText(8, int(rect.bottom()), f'{low:.2f}')

        if self._xLabel:
            painter.drawText(self.rect().adjusted(0, 0, 0, -6), Qt.AlignBottom | Qt.AlignHCenter, self._xLabel)

        if self._categories:
            step = max(1, len(self._categories) // 4)
            for i in range(0, len(self._categories), step):
                x = rect.left() if len(self._categories) == 1 else rect.left() + i * rect.width() / (len(self._categories) - 1)
                painter.drawText(QRectF(x - 30, rect.bottom() + 6, 60, 18), Qt.AlignCenter, self._categories[i])

        self.__drawLegend(painter, rect)

    def __drawLegend(self, painter: QPainter, rect: QRectF):
        colors = self.__colors()
        x = rect.left()
        y = self.height() - 24
        for i, (name, _) in enumerate(self._series):
            color = colors[i % len(colors)]
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(QRectF(x, y + 5, 14, 6), 3, 3)
            painter.setPen(QColor(255, 255, 255, 210) if isDarkTheme() else QColor(0, 0, 0, 180))
            painter.drawText(QRectF(x + 20, y, 120, 18), Qt.AlignLeft | Qt.AlignVCenter, name)
            x += 128

    def __drawEmpty(self, painter: QPainter):
        color = QColor(255, 255, 255, 150) if isDarkTheme() else QColor(0, 0, 0, 120)
        painter.setPen(color)
        painter.drawText(self.rect(), Qt.AlignCenter, self.tr('No chart data'))


class MetricCard(SimpleCardWidget):
    """ Compact metric card """

    def __init__(self, title='', value='', caption='', parent=None):
        super().__init__(parent=parent)
        self.titleLabel = CaptionLabel(title, self)
        self.valueLabel = SubtitleLabel(value, self)
        self.captionLabel = CaptionLabel(caption, self)
        self.vBoxLayout = QVBoxLayout(self)

        self.titleLabel.setTextColor(QColor(96, 96, 96), QColor(200, 200, 200))
        self.captionLabel.setTextColor(QColor(96, 96, 96), QColor(200, 200, 200))
        self.vBoxLayout.setSpacing(4)
        self.vBoxLayout.setContentsMargins(16, 14, 16, 14)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.valueLabel)
        self.vBoxLayout.addWidget(self.captionLabel)
        self.setMinimumWidth(132)

    def setValue(self, value: str):
        """ set metric value """
        self.valueLabel.setText(value)
