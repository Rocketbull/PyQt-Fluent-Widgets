# coding:utf-8
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from qfluentwidgets import (WorkspaceTabWidget, ChartWidget, ChartType, MetricCard,
                            DataGridWidget, BodyLabel, FluentIcon)

from .gallery_interface import GalleryInterface


class AnalysisInterface(GalleryInterface):
    """ Model and data analysis interface """

    def __init__(self, parent=None):
        super().__init__(
            title=self.tr('Analysis'),
            subtitle='qfluentwidgets.components.widgets',
            parent=parent
        )
        self.setObjectName('analysisInterface')

        self.addExampleCard(
            self.tr('A split workspace for model analysis'),
            AnalysisWorkspaceDemo(self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/analysis_workspace/demo.py',
            stretch=1
        )

        self.addExampleCard(
            self.tr('Dependency-free charts for metrics'),
            ChartGalleryDemo(self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/analysis_workspace/demo.py',
            stretch=1
        )


class AnalysisWorkspaceDemo(WorkspaceTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(460)
        self.addTab(MetricsPage(self), self.tr('Metrics'), FluentIcon.VIEW)
        self.addTab(DatasetPage(self), self.tr('Dataset'), FluentIcon.DOCUMENT)
        self.addTab(ConfusionPage(self), self.tr('Confusion'), FluentIcon.APPLICATION, pane=1)
        self.setTabDirty(0, True)


class MetricsPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = QHBoxLayout()

        for title, value, caption in [
            (self.tr('Accuracy'), '94.8%', self.tr('+1.6% vs baseline')),
            (self.tr('F1 Score'), '0.923', self.tr('macro average')),
            (self.tr('Latency'), '18 ms', self.tr('p95 inference')),
        ]:
            self.cardLayout.addWidget(MetricCard(title, value, caption, self))

        chart = ChartWidget(self)
        chart.setTitle(self.tr('Training loss'))
        chart.setAxisLabels(self.tr('Epoch'), self.tr('Loss'))
        chart.setCategories([str(i) for i in range(1, 9)])
        chart.setSeries(self.tr('train'), [0.84, 0.62, 0.48, 0.39, 0.33, 0.29, 0.25, 0.23])
        chart.addSeries(self.tr('validation'), [0.88, 0.68, 0.54, 0.45, 0.40, 0.36, 0.34, 0.32])

        self.vBoxLayout.addLayout(self.cardLayout)
        self.vBoxLayout.addWidget(chart, 1)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


class DatasetPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        grid = DataGridWidget(self)
        grid.setColumns([
            ('feature', self.tr('Feature')),
            ('type', self.tr('Type')),
            ('missing', self.tr('Missing')),
            ('importance', self.tr('Importance')),
        ])
        grid.setRows([
            {'feature': 'age', 'type': 'numeric', 'missing': '0.4%', 'importance': '0.18'},
            {'feature': 'income', 'type': 'numeric', 'missing': '2.1%', 'importance': '0.27'},
            {'feature': 'region', 'type': 'category', 'missing': '0.0%', 'importance': '0.09'},
            {'feature': 'tenure_days', 'type': 'numeric', 'missing': '0.0%', 'importance': '0.22'},
            {'feature': 'last_active', 'type': 'datetime', 'missing': '1.3%', 'importance': '0.14'},
        ])

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(grid)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


class ConfusionPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        label = BodyLabel(self.tr('Keep model metrics, data inspection and prediction analysis side by side.'), self)
        label.setWordWrap(True)

        chart = ChartWidget(self)
        chart.setChartType(ChartType.BAR)
        chart.setTitle(self.tr('Prediction counts'))
        chart.setCategories([self.tr('Class A'), self.tr('Class B'), self.tr('Class C')])
        chart.setSeries(self.tr('correct'), [420, 318, 280])
        chart.addSeries(self.tr('incorrect'), [28, 36, 42])

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(label)
        self.vBoxLayout.addWidget(chart, 1)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


class ChartGalleryDemo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)

        lineChart = ChartWidget(self)
        lineChart.setTitle(self.tr('ROC AUC by model'))
        lineChart.setCategories(['v1', 'v2', 'v3', 'v4'])
        lineChart.setSeries('baseline', [0.86, 0.87, 0.88, 0.89])
        lineChart.addSeries('candidate', [0.87, 0.90, 0.92, 0.94])

        scatterChart = ChartWidget(self)
        scatterChart.setChartType(ChartType.SCATTER)
        scatterChart.setTitle(self.tr('Residual sample'))
        scatterChart.setSeries('residual', [0.12, -0.04, 0.18, -0.11, 0.06, 0.02, -0.08, 0.13])

        self.hBoxLayout.addWidget(lineChart)
        self.hBoxLayout.addWidget(scatterChart)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
