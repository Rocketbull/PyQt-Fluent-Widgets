# coding:utf-8
import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (EmptyStateWidget, ErrorStateWidget, LoadingOverlay, SkeletonWidget,
                            PushButton, SimpleCardWidget, FluentIcon, setTheme, Theme)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('State widgets')
        self.resize(760, 520)

        self.emptyState = EmptyStateWidget(
            self.tr('No projects yet'),
            self.tr('Create a project to start organizing your workspace.'),
            self
        )
        self.emptyState.setIcon(FluentIcon.FOLDER)
        self.emptyState.setActionText(self.tr('Create project'))

        self.errorState = ErrorStateWidget(
            self.tr('Could not load data'),
            self.tr('Check your connection and try again.'),
            self
        )
        self.errorState.setActionText(self.tr('Retry'))

        self.skeleton = SkeletonWidget(self)
        self.skeleton.setFixedHeight(110)

        self.loadingCard = SimpleCardWidget(self)
        self.loadingCard.setFixedHeight(180)
        self.loadingButton = PushButton(self.tr('Show overlay'), self.loadingCard)
        self.loadingOverlay = LoadingOverlay(self.loadingCard)
        self.loadingOverlay.setTitle(self.tr('Syncing'))
        self.loadingOverlay.setContent(self.tr('Refreshing workspace data'))
        self.loadingButton.clicked.connect(self.showOverlay)

        self.vBoxLayout = QVBoxLayout(self)
        self.stateLayout = QHBoxLayout()
        self.loadingLayout = QVBoxLayout(self.loadingCard)

        self.stateLayout.addWidget(self.emptyState)
        self.stateLayout.addWidget(self.errorState)
        self.loadingLayout.addWidget(self.loadingButton, 0, Qt.AlignCenter)
        self.vBoxLayout.addLayout(self.stateLayout)
        self.vBoxLayout.addWidget(self.skeleton)
        self.vBoxLayout.addWidget(self.loadingCard)
        self.vBoxLayout.setContentsMargins(24, 24, 24, 24)

    def showOverlay(self):
        self.loadingOverlay.setLoading(True)
        QTimer.singleShot(2200, lambda: self.loadingOverlay.setLoading(False))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setTheme(Theme.AUTO)
    w = Demo()
    w.show()
    app.exec()
