# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import DataGridWidget, InfoBar, InfoBarPosition, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('DataGrid')
        self.resize(860, 560)

        self.dataGrid = DataGridWidget(self)
        self.dataGrid.setColumns([
            ('title', self.tr('Title')),
            ('artist', self.tr('Artist')),
            ('album', self.tr('Album')),
            ('year', self.tr('Year')),
            ('duration', self.tr('Duration')),
        ])
        self.dataGrid.setRows(self.songInfos())
        self.dataGrid.setRowActions([(self.tr('Open'), self.openRow)])

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.dataGrid)
        self.vBoxLayout.setContentsMargins(24, 24, 24, 24)

    def openRow(self, row):
        InfoBar.info(
            title=row['title'],
            content=self.tr('Opening {0} by {1}.').format(row['title'], row['artist']),
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setTheme(Theme.AUTO)
    w = Demo()
    w.show()
    app.exec()
