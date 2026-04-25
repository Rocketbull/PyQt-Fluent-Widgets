# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout

from qfluentwidgets import (WorkspaceTabWidget, ChartWidget, ChartType, MetricCard, DataGridWidget,
                            BodyLabel, setTheme, Theme, FluentIcon)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Analysis workspace')
        self.resize(980, 640)

        self.workspace = WorkspaceTabWidget(self)
        self.workspace.addTab(MetricsPage(self), self.tr('Metrics'), FluentIcon.VIEW)
        self.workspace.addTab(DatasetPage(self), self.tr('Dataset'), FluentIcon.DOCUMENT)
        self.workspace.addTab(ConfusionPage(self), self.tr('Confusion'), FluentIcon.APPLICATION, pane=1)
        self.workspace.setTabDirty(0, True)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.workspace)
        self.vBoxLayout.setContentsMargins(24, 24, 24, 24)


class MetricsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QHBoxLayout()

        for title, value, caption in [
            (self.tr('Accuracy'), '94.8%', self.tr('+1.6% vs baseline')),
            (self.tr('F1 Score'), '0.923', self.tr('macro average')),
            (self.tr('Latency'), '18 ms', self.tr('p95 inference')),
            (self.tr('Samples'), '12.4k', self.tr('validation split')),
        ]:
            self.cardLayout.addWidget(MetricCard(title, value, caption, self))

        lossChart = ChartWidget(self)
        lossChart.setTitle(self.tr('Training loss'))
        lossChart.setAxisLabels(self.tr('Epoch'), self.tr('Loss'))
        lossChart.setCategories([str(i) for i in range(1, 11)])
        lossChart.setSeries(self.tr('train'), [0.84, 0.62, 0.48, 0.39, 0.33, 0.29, 0.25, 0.23, 0.21, 0.20])
        lossChart.addSeries(self.tr('validation'), [0.88, 0.68, 0.54, 0.45, 0.40, 0.36, 0.34, 0.32, 0.31, 0.30])

        self.vBoxLayout.addLayout(self.cardLayout)
        self.vBoxLayout.addWidget(lossChart, 1)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


class DatasetPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid = DataGridWidget(self)
        self.grid.setColumns([
            ('feature', self.tr('Feature')),
            ('type', self.tr('Type')),
            ('missing', self.tr('Missing')),
            ('importance', self.tr('Importance')),
        ])
        self.grid.setRows([
            {'feature': 'age', 'type': 'numeric', 'missing': '0.4%', 'importance': '0.18'},
            {'feature': 'income', 'type': 'numeric', 'missing': '2.1%', 'importance': '0.27'},
            {'feature': 'region', 'type': 'category', 'missing': '0.0%', 'importance': '0.09'},
            {'feature': 'tenure_days', 'type': 'numeric', 'missing': '0.0%', 'importance': '0.22'},
            {'feature': 'last_active', 'type': 'datetime', 'missing': '1.3%', 'importance': '0.14'},
            {'feature': 'plan', 'type': 'category', 'missing': '0.0%', 'importance': '0.10'},
        ])

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.grid)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


class ConfusionPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        chart = ChartWidget(self)
        chart.setChartType(ChartType.BAR)
        chart.setTitle(self.tr('Prediction counts'))
        chart.setCategories([self.tr('Class A'), self.tr('Class B'), self.tr('Class C')])
        chart.setSeries(self.tr('correct'), [420, 318, 280])
        chart.addSeries(self.tr('incorrect'), [28, 36, 42])

        label = BodyLabel(self.tr('Mock model analysis workspace with split tabs, metrics, charts and data grid.'), self)
        label.setWordWrap(True)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(label)
        self.vBoxLayout.addWidget(chart, 1)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setTheme(Theme.AUTO)
    w = Demo()
    w.show()
    app.exec()
