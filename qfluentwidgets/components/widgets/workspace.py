# coding:utf-8
from typing import Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter

from ...common.icon import FluentIcon, FluentIconBase
from .button import TransparentToolButton
from .tab_view import TabWidget, TabCloseButtonDisplayMode


class WorkspaceTabWidget(QWidget):
    """ Multi-tab workspace with optional split panes """

    tabAdded = Signal(int)
    splitChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.primaryTabs = self.__createTabWidget()
        self.secondaryTabs = self.__createTabWidget()
        self.secondaryTabs.hide()

        self.splitButton = TransparentToolButton(FluentIcon.LAYOUT, self)
        self.closeSplitButton = TransparentToolButton(FluentIcon.CLOSE, self)

        self.vBoxLayout = QVBoxLayout(self)
        self.toolbarLayout = QHBoxLayout()
        self.__initWidget()

    def __initWidget(self):
        self.splitter.addWidget(self.primaryTabs)
        self.splitter.addWidget(self.secondaryTabs)
        self.splitter.setSizes([1, 1])

        self.splitButton.setToolTip(self.tr('Split workspace'))
        self.closeSplitButton.setToolTip(self.tr('Close split'))
        self.closeSplitButton.hide()

        self.toolbarLayout.setContentsMargins(0, 0, 0, 0)
        self.toolbarLayout.addStretch(1)
        self.toolbarLayout.addWidget(self.splitButton)
        self.toolbarLayout.addWidget(self.closeSplitButton)

        self.vBoxLayout.setSpacing(8)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.toolbarLayout)
        self.vBoxLayout.addWidget(self.splitter)

        self.splitButton.clicked.connect(lambda: self.setSplitVisible(True))
        self.closeSplitButton.clicked.connect(lambda: self.setSplitVisible(False))

    def __createTabWidget(self):
        tabs = TabWidget(self)
        tabs.setTabsClosable(True)
        tabs.setMovable(True)
        tabs.setScrollable(True)
        tabs.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ON_HOVER)
        tabs.tabCloseRequested.connect(tabs.removeTab)
        return tabs

    def addTab(self, widget: QWidget, label: str, icon: Union[QIcon, str, FluentIconBase] = None,
               routeKey=None, pane=0):
        """ add a tab to the primary or secondary pane """
        tabs = self.secondaryTabs if pane == 1 else self.primaryTabs
        if pane == 1:
            self.setSplitVisible(True)

        index = tabs.addTab(widget, label, icon, routeKey)
        tabs.setCurrentIndex(index)
        self.tabAdded.emit(index)
        return index

    def setTabDirty(self, index: int, dirty=True, pane=0):
        """ mark a tab as dirty by appending an asterisk """
        tabs = self.secondaryTabs if pane == 1 else self.primaryTabs
        text = tabs.tabText(index)
        if not text:
            return

        if dirty and not text.endswith('*'):
            tabs.setTabText(index, text + '*')
        elif not dirty and text.endswith('*'):
            tabs.setTabText(index, text[:-1])

    def setSplitVisible(self, visible=True):
        """ show or hide secondary tab pane """
        self.secondaryTabs.setVisible(visible)
        self.closeSplitButton.setVisible(visible)
        self.splitChanged.emit(visible)

    def isSplitVisible(self):
        return self.secondaryTabs.isVisible()
