# coding:utf-8
import os
import sys

from PySide6.QtCore import Qt, QTranslator
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from app.common.config import cfg
from app.view.main_window import MainWindow


def setQtPlatformFallback():
    """Avoid selecting Wayland when no Wayland display is available."""
    if sys.platform != "linux":
        return

    platform = os.environ.get("QT_QPA_PLATFORM", "").lower()
    if platform and platform != "wayland":
        return

    if os.environ.get("WAYLAND_DISPLAY"):
        return

    if os.environ.get("DISPLAY"):
        os.environ["QT_QPA_PLATFORM"] = "xcb"
    elif platform == "wayland":
        os.environ["QT_QPA_PLATFORM"] = "offscreen"


setQtPlatformFallback()

# enable dpi scale
if cfg.get(cfg.dpiScale) != "Auto":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)


# internationalization
locale = cfg.get(cfg.language).value
translator = FluentTranslator(locale)
galleryTranslator = QTranslator()
galleryTranslator.load(locale, "gallery", ".", ":/gallery/i18n")

app.installTranslator(translator)
app.installTranslator(galleryTranslator)

# create main window
w = MainWindow()
w.show()

app.exec()
