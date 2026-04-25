# coding: utf-8
from typing import List
from PySide6.QtCore import Qt, Signal, QEasingCurve, QUrl, QSize, QTimer, QDateTime
from PySide6.QtGui import QIcon, QDesktopServices, QColor, QShortcut, QKeySequence
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QFrame, QWidget, QVBoxLayout,
                               QTextBrowser, QPlainTextEdit, QPushButton, QLabel)

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen, SystemThemeListener, isDarkTheme)
from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .basic_input_interface import BasicInputInterface
from .date_time_interface import DateTimeInterface
from .dialog_interface import DialogInterface
from .layout_interface import LayoutInterface
from .icon_interface import IconInterface
from .material_interface import MaterialInterface
from .menu_interface import MenuInterface
from .navigation_view_interface import NavigationViewInterface
from .scroll_interface import ScrollInterface
from .status_info_interface import StatusInfoInterface
from .setting_interface import SettingInterface
from .text_interface import TextInterface
from .view_interface import ViewInterface
from .production_interface import ProductionInterface
from .analysis_interface import AnalysisInterface
from ..common.config import ZH_SUPPORT_URL, EN_SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource


class MainWindow(FluentWindow):

    def __init__(self):
        super().__init__()
        self.initWindow()

        # create system theme listener
        self.themeListener = SystemThemeListener(self)

        # create sub interface
        self.homeInterface = HomeInterface(self)
        self.iconInterface = IconInterface(self)
        self.basicInputInterface = BasicInputInterface(self)
        self.dateTimeInterface = DateTimeInterface(self)
        self.dialogInterface = DialogInterface(self)
        self.layoutInterface = LayoutInterface(self)
        self.menuInterface = MenuInterface(self)
        self.materialInterface = MaterialInterface(self)
        self.navigationViewInterface = NavigationViewInterface(self)
        self.scrollInterface = ScrollInterface(self)
        self.statusInfoInterface = StatusInfoInterface(self)
        self.settingInterface = SettingInterface(self)
        self.textInterface = TextInterface(self)
        self.viewInterface = ViewInterface(self)
        self.productionInterface = ProductionInterface(self)
        self.analysisInterface = AnalysisInterface(self)

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)

        self.chatPanel = CopilotChatPanel(self)
        self.chatPanel.hide()
        self.widgetLayout.addWidget(self.chatPanel)
        self.toggleChatShortcut = QShortcut(QKeySequence("Ctrl+Shift+I"), self)
        self.toggleChatShortcut.activated.connect(self.toggleCopilotChat)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

        # start theme listener
        self.themeListener.start()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        self.addSubInterface(self.iconInterface, Icon.EMOJI_TAB_SYMBOLS, t.icons)
        self.navigationInterface.addSeparator()

        pos = NavigationItemPosition.SCROLL
        self.addSubInterface(self.basicInputInterface, FIF.CHECKBOX,t.basicInput, pos)
        self.addSubInterface(self.dateTimeInterface, FIF.DATE_TIME, t.dateTime, pos)
        self.addSubInterface(self.dialogInterface, FIF.MESSAGE, t.dialogs, pos)
        self.addSubInterface(self.layoutInterface, FIF.LAYOUT, t.layout, pos)
        self.addSubInterface(self.materialInterface, FIF.PALETTE, t.material, pos)
        self.addSubInterface(self.menuInterface, Icon.MENU, t.menus, pos)
        self.addSubInterface(self.navigationViewInterface, FIF.MENU, t.navigation, pos)
        self.addSubInterface(self.scrollInterface, FIF.SCROLL, t.scroll, pos)
        self.addSubInterface(self.statusInfoInterface, FIF.CHAT, t.statusInfo, pos)
        self.addSubInterface(self.textInterface, Icon.TEXT, t.text, pos)
        self.addSubInterface(self.viewInterface, Icon.GRID, t.view, pos)
        self.addSubInterface(self.productionInterface, FIF.DEVELOPER_TOOLS, self.tr('Production'), pos)
        self.addSubInterface(self.analysisInterface, FIF.ROBOT, self.tr('Analysis'), pos)

        # add custom widget to bottom
        self.navigationInterface.addItem(
            routeKey='price',
            icon=Icon.PRICE,
            text=t.price,
            onClick=self.onSupport,
            selectable=False,
            tooltip=t.price,
            position=NavigationItemPosition.BOTTOM
        )

        self.navigationInterface.addItem(
            routeKey='copilotChat',
            icon=FIF.ROBOT,
            text=self.tr('AI Chat'),
            onClick=self.toggleCopilotChat,
            selectable=False,
            tooltip=self.tr('AI Chat (Ctrl+Shift+I)'),
            position=NavigationItemPosition.BOTTOM
        )

        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(960, 780)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        language = cfg.get(cfg.language).value
        if language.name() == "zh_CN":
            QDesktopServices.openUrl(QUrl(ZH_SUPPORT_URL))
        else:
            QDesktopServices.openUrl(QUrl(EN_SUPPORT_URL))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def closeEvent(self, e):
        self.themeListener.terminate()
        self.themeListener.deleteLater()
        super().closeEvent(e)

    def _onThemeChangedFinished(self):
        super()._onThemeChangedFinished()

        # retry
        if self.isMicaEffectEnabled():
            QTimer.singleShot(100, lambda: self.windowEffect.setMicaEffect(self.winId(), isDarkTheme()))

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)

    def toggleCopilotChat(self):
        if self.chatPanel.isHidden():
            self.chatPanel.show()
            self.chatPanel.addSystemTip(self.stackedWidget.currentWidget())
            return

        self.chatPanel.hide()


class CopilotChatPanel(QFrame):
    """A lightweight copilot-style chat panel for the gallery demo."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('copilotChatPanel')
        self.setMinimumWidth(300)
        self.setMaximumWidth(420)
        self.setFixedWidth(340)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(12, 12, 12, 12)
        self.vBoxLayout.setSpacing(10)

        headerLabel = QLabel(self.tr('Copilot Chat'), self)
        headerLabel.setStyleSheet('font-size: 16px; font-weight: 600;')

        self.chatHistory = QTextBrowser(self)
        self.chatHistory.setOpenExternalLinks(True)

        self.promptEdit = QPlainTextEdit(self)
        self.promptEdit.setPlaceholderText(self.tr('Ask about the current page, controls, or example usage...'))
        self.promptEdit.setFixedHeight(92)

        self.sendButton = QPushButton(self.tr('Send'), self)
        self.clearButton = QPushButton(self.tr('Clear'), self)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.sendButton)

        self.vBoxLayout.addWidget(headerLabel)
        self.vBoxLayout.addWidget(self.chatHistory, 1)
        self.vBoxLayout.addWidget(self.promptEdit)
        self.vBoxLayout.addLayout(buttonLayout)

        self.sendButton.clicked.connect(self.sendMessage)
        self.clearButton.clicked.connect(self.chatHistory.clear)
        self.promptEdit.textChanged.connect(self._syncSendButtonState)
        self._syncSendButtonState()

        self._appendMessage(self.tr('assistant'), self.tr('Hi! I can explain widgets and suggest what to explore next.'))

    def addSystemTip(self, currentInterface: QWidget):
        if not currentInterface:
            return

        route = currentInterface.objectName().replace('Interface', '')
        tip = self.tr('You are browsing the <b>{}</b> section. Ask me for guided examples.').format(route)
        self._appendMessage(self.tr('system'), tip)

    def _syncSendButtonState(self):
        self.sendButton.setEnabled(bool(self.promptEdit.toPlainText().strip()))

    def sendMessage(self):
        content = self.promptEdit.toPlainText().strip()
        if not content:
            return

        self._appendMessage(self.tr('you'), content)
        self.promptEdit.clear()
        self._appendMessage(self.tr('assistant'), self._buildAssistantReply(content))

    def _buildAssistantReply(self, content: str) -> str:
        question = content.lower()
        current = self.window().stackedWidget.currentWidget()
        currentName = current.objectName().replace('Interface', '') if current else self.tr('home')

        if 'layout' in question:
            return self.tr('Try opening the Layout section. It shows spacing, containers and page composition patterns.')

        if 'dialog' in question or 'popup' in question:
            return self.tr('The Dialogs page demonstrates message boxes, flyouts and teaching tips with Fluent style.')

        if 'next' in question or 'what should i do' in question:
            return self.tr('Since you are in <b>{}</b>, compare it with Production and Analysis to see real-world patterns.').format(currentName)

        return self.tr('I can help with widget discovery, navigation and demo walkthroughs. You are currently in <b>{}</b>.').format(currentName)

    def _appendMessage(self, role: str, content: str):
        timestamp = QDateTime.currentDateTime().toString('HH:mm')
        self.chatHistory.append(f"<p><b>{role}</b> <span style='color:gray'>[{timestamp}]</span><br>{content}</p>")
