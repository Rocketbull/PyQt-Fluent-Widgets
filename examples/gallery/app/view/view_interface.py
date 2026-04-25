# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QFrame, QTreeWidgetItem, QHBoxLayout, QVBoxLayout, QTreeWidgetItemIterator,
                               QTableWidgetItem, QListWidgetItem, QWidget)
from qfluentwidgets import (TreeWidget, TableWidget, ListWidget, HorizontalFlipView, DataGridWidget,
                            InfoBar, InfoBarPosition, WorkspaceTabWidget, ChartWidget, ChartType,
                            MetricCard, FluentIcon, BodyLabel)

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.style_sheet import StyleSheet


class ViewInterface(GalleryInterface):
    """ View interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.view,
            subtitle="qfluentwidgets.components.widgets",
            parent=parent
        )
        self.setObjectName('viewInterface')

        # list view
        self.addExampleCard(
            title=self.tr('A simple ListView'),
            widget=ListFrame(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/list_view/demo.py'
        )

        # table view
        self.addExampleCard(
            title=self.tr('A simple TableView'),
            widget=TableFrame(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/table_view/demo.py'
        )

        # data grid
        self.addExampleCard(
            title=self.tr('A searchable DataGrid'),
            widget=DataGridFrame(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/data_grid/demo.py',
            stretch=1
        )

        # analysis workspace
        self.addExampleCard(
            title=self.tr('A model analysis workspace'),
            widget=AnalysisWorkspaceFrame(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/analysis_workspace/demo.py',
            stretch=1
        )

        # tree view
        frame = TreeFrame(self)
        self.addExampleCard(
            title=self.tr('A simple TreeView'),
            widget=frame,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/tree_view/demo.py'
        )

        frame = TreeFrame(self, True)
        self.addExampleCard(
            title=self.tr('A TreeView with Multi-selection enabled'),
            widget=frame,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/tree_view/demo.py'
        )

        # flip view
        w = HorizontalFlipView(self)
        w.addImages([
            ":/gallery/images/Shoko1.jpg",
            ":/gallery/images/Shoko2.jpg",
            ":/gallery/images/Shoko3.jpg",
            ":/gallery/images/Shoko4.jpg",
        ])
        self.addExampleCard(
            title=self.tr('Flip view'),
            widget=w,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/flip_view/demo.py'
        )


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)


class ListFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listWidget = ListWidget(self)
        self.addWidget(self.listWidget)

        stands = [
            self.tr("Star Platinum"), self.tr("Hierophant Green"),
            self.tr("Made in Haven"), self.tr("King Crimson"),
            self.tr("Silver Chariot"), self.tr("Crazy diamond"),
            self.tr("Metallica"), self.tr("Another One Bites The Dust"),
            self.tr("Heaven's Door"), self.tr("Killer Queen"),
            self.tr("The Grateful Dead"), self.tr("Stone Free"),
            self.tr("The World"), self.tr("Sticky Fingers"),
            self.tr("Ozone Baby"), self.tr("Love Love Deluxe"),
            self.tr("Hermit Purple"), self.tr("Gold Experience"),
            self.tr("King Nothing"), self.tr("Paper Moon King"),
            self.tr("Scary Monster"), self.tr("Mandom"),
            self.tr("20th Century Boy"), self.tr("Tusk Act 4"),
            self.tr("Ball Breaker"), self.tr("Sex Pistols"),
            self.tr("D4C • Love Train"), self.tr("Born This Way"),
            self.tr("SOFT & WET"), self.tr("Paisley Park"),
            self.tr("Wonder of U"), self.tr("Walking Heart"),
            self.tr("Cream Starter"), self.tr("November Rain"),
            self.tr("Smooth Operators"), self.tr("The Matte Kudasai")
        ]
        for stand in stands:
            self.listWidget.addItem(QListWidgetItem(stand))

        self.setFixedSize(300, 380)


class TreeFrame(Frame):

    def __init__(self, parent=None, enableCheck=False):
        super().__init__(parent)
        self.tree = TreeWidget(self)
        self.addWidget(self.tree)

        item1 = QTreeWidgetItem([self.tr('JoJo 1 - Phantom Blood')])
        item1.addChildren([
            QTreeWidgetItem([self.tr('Jonathan Joestar')]),
            QTreeWidgetItem([self.tr('Dio Brando')]),
            QTreeWidgetItem([self.tr('Will A. Zeppeli')]),
        ])
        self.tree.addTopLevelItem(item1)

        item2 = QTreeWidgetItem([self.tr('JoJo 3 - Stardust Crusaders')])
        item21 = QTreeWidgetItem([self.tr('Jotaro Kujo')])
        item21.addChildren([
            QTreeWidgetItem(['空条承太郎']),
            QTreeWidgetItem(['空条蕉太狼']),
            QTreeWidgetItem(['阿强']),
            QTreeWidgetItem(['卖鱼强']),
            QTreeWidgetItem(['那个无敌的男人']),
        ])
        item2.addChild(item21)
        self.tree.addTopLevelItem(item2)
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)

        self.setFixedSize(300, 380)

        if enableCheck:
            it = QTreeWidgetItemIterator(self.tree)
            while(it.value()):
                it.value().setCheckState(0, Qt.Unchecked)
                it += 1


class TableFrame(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(5)
        self.setRowCount(60)
        self.setHorizontalHeaderLabels([
            self.tr('Title'), self.tr('Artist'), self.tr('Album'),
            self.tr('Year'), self.tr('Duration')
        ])

        songInfos = [
            ['かばん', 'aiko', 'かばん', '2004', '5:04'],
            ['爱你', '王心凌', '爱你', '2004', '3:39'],
            ['星のない世界', 'aiko', '星のない世界/横顔', '2007', '5:30'],
            ['横顔', 'aiko', '星のない世界/横顔', '2007', '5:06'],
            ['秘密', 'aiko', '秘密', '2008', '6:27'],
            ['シアワセ', 'aiko', '秘密', '2008', '5:25'],
            ['二人', 'aiko', '二人', '2008', '5:00'],
            ['スパークル', 'RADWIMPS', '君の名は。', '2016', '8:54'],
            ['なんでもないや', 'RADWIMPS', '君の名は。', '2016', '3:16'],
            ['前前前世', 'RADWIMPS', '人間開花', '2016', '4:35'],
            ['恋をしたのは', 'aiko', '恋をしたのは', '2016', '6:02'],
            ['夏バテ', 'aiko', '恋をしたのは', '2016', '4:41'],
            ['もっと', 'aiko', 'もっと', '2016', '4:50'],
            ['問題集', 'aiko', 'もっと', '2016', '4:18'],
            ['半袖', 'aiko', 'もっと', '2016', '5:50'],
            ['ひねくれ', '鎖那', 'Hush a by little girl', '2017', '3:54'],
            ['シュテルン', '鎖那', 'Hush a by little girl', '2017', '3:16'],
            ['愛は勝手', 'aiko', '湿った夏の始まり', '2018', '5:31'],
            ['ドライブモード', 'aiko', '湿った夏の始まり', '2018', '3:37'],
            ['うん。', 'aiko', '湿った夏の始まり', '2018', '5:48'],
            ['キラキラ', 'aikoの詩。', '2019', '5:08', 'aiko'],
            ['恋のスーパーボール', 'aiko', 'aikoの詩。', '2019', '4:31'],
            ['磁石', 'aiko', 'どうしたって伝えられないから', '2021', '4:24'],
            ['食べた愛', 'aiko', '食べた愛/あたしたち', '2021', '5:17'],
            ['列車', 'aiko', '食べた愛/あたしたち', '2021', '4:18'],
            ['花の塔', 'さユり', '花の塔', '2022', '4:35'],
            ['夏恋のライフ', 'aiko', '夏恋のライフ', '2022', '5:03'],
            ['あかときリロード', 'aiko', 'あかときリロード', '2023', '4:04'],
            ['荒れた唇は恋を失くす', 'aiko', '今の二人をお互いが見てる', '2023', '4:07'],
            ['ワンツースリー', 'aiko', '今の二人をお互いが見てる', '2023', '4:47'],
        ]
        songInfos += songInfos
        for i, songInfo in enumerate(songInfos):
            for j in range(5):
                self.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.setFixedSize(625, 440)
        self.resizeColumnsToContents()


class DataGridFrame(DataGridWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(440)
        self.setColumns([
            ('title', self.tr('Title')),
            ('artist', self.tr('Artist')),
            ('album', self.tr('Album')),
            ('year', self.tr('Year')),
            ('duration', self.tr('Duration')),
        ])
        self.setRows(self.songInfos())
        self.setRowActions([(self.tr('Open'), self.openRow)])

    def openRow(self, row):
        InfoBar.info(
            title=row['title'],
            content=self.tr('Opening {0} by {1}.').format(row['title'], row['artist']),
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self.window()
        )

    def songInfos(self):
        rows = [
            ('かばん', 'aiko', 'かばん', '2004', '5:04'),
            ('爱你', '王心凌', '爱你', '2004', '3:39'),
            ('星のない世界', 'aiko', '星のない世界/横顔', '2007', '5:30'),
            ('横顔', 'aiko', '星のない世界/横顔', '2007', '5:06'),
            ('秘密', 'aiko', '秘密', '2008', '6:27'),
            ('シアワセ', 'aiko', '秘密', '2008', '5:25'),
            ('二人', 'aiko', '二人', '2008', '5:00'),
            ('スパークル', 'RADWIMPS', '君の名は。', '2016', '8:54'),
            ('なんでもないや', 'RADWIMPS', '君の名は。', '2016', '3:16'),
            ('前前前世', 'RADWIMPS', '人間開花', '2016', '4:35'),
            ('恋をしたのは', 'aiko', '恋をしたのは', '2016', '6:02'),
            ('夏バテ', 'aiko', '恋をしたのは', '2016', '4:41'),
            ('もっと', 'aiko', 'もっと', '2016', '4:50'),
            ('問題集', 'aiko', 'もっと', '2016', '4:18'),
            ('半袖', 'aiko', 'もっと', '2016', '5:50'),
        ]
        rows = rows + rows
        return [
            {'title': title, 'artist': artist, 'album': album, 'year': year, 'duration': duration}
            for title, artist, album, year, duration in rows
        ]


class AnalysisWorkspaceFrame(WorkspaceTabWidget):

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
        vBoxLayout = QVBoxLayout(self)
        cardLayout = QHBoxLayout()

        for title, value, caption in [
            (self.tr('Accuracy'), '94.8%', self.tr('+1.6%')),
            (self.tr('F1 Score'), '0.923', self.tr('macro avg')),
            (self.tr('Latency'), '18 ms', self.tr('p95')),
        ]:
            cardLayout.addWidget(MetricCard(title, value, caption, self))

        chart = ChartWidget(self)
        chart.setTitle(self.tr('Training loss'))
        chart.setAxisLabels(self.tr('Epoch'), self.tr('Loss'))
        chart.setCategories([str(i) for i in range(1, 9)])
        chart.setSeries(self.tr('train'), [0.84, 0.62, 0.48, 0.39, 0.33, 0.29, 0.25, 0.23])
        chart.addSeries(self.tr('validation'), [0.88, 0.68, 0.54, 0.45, 0.40, 0.36, 0.34, 0.32])

        vBoxLayout.addLayout(cardLayout)
        vBoxLayout.addWidget(chart, 1)
        vBoxLayout.setContentsMargins(0, 0, 0, 0)


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
        ])

        vBoxLayout = QVBoxLayout(self)
        vBoxLayout.addWidget(grid)
        vBoxLayout.setContentsMargins(0, 0, 0, 0)


class ConfusionPage(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        chart = ChartWidget(self)
        chart.setChartType(ChartType.BAR)
        chart.setTitle(self.tr('Prediction counts'))
        chart.setCategories([self.tr('Class A'), self.tr('Class B'), self.tr('Class C')])
        chart.setSeries(self.tr('correct'), [420, 318, 280])
        chart.addSeries(self.tr('incorrect'), [28, 36, 42])

        label = BodyLabel(self.tr('Split tabs keep model metrics and error analysis side by side.'), self)
        label.setWordWrap(True)

        vBoxLayout = QVBoxLayout(self)
        vBoxLayout.addWidget(label)
        vBoxLayout.addWidget(chart, 1)
        vBoxLayout.setContentsMargins(0, 0, 0, 0)
