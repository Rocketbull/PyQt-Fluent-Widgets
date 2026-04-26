# coding:utf-8
import hashlib
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QFile
from PySide6.QtGui import QIcon, QPixmap, QImageReader
from PySide6.QtWidgets import (
    QApplication, QFileDialog, QFrame, QGridLayout, QHeaderView, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMessageBox, QSplitter,
    QStackedWidget, QTableWidgetItem, QVBoxLayout, QWidget
)

from qfluentwidgets import (
    BodyLabel, CaptionLabel, CardWidget, ComboBox, FluentIcon as FIF,
    FluentWindow, InfoBar, InfoBarPosition, PrimaryPushButton, PushButton,
    SearchLineEdit, SmoothScrollArea, StrongBodyLabel, TableWidget, TitleLabel
)


IMAGE_SUFFIXES = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif', '.tif', '.tiff'}
LOCATION_HINTS = {
    'beijing', 'berlin', 'chicago', 'london', 'los-angeles', 'new-york',
    'paris', 'san-francisco', 'seattle', 'shanghai', 'tokyo', 'travel',
    'vacation', 'wedding'
}


@dataclass(frozen=True)
class Photo:
    path: Path
    folder: Path
    size: int
    modified: datetime
    width: int
    height: int

    @property
    def name(self):
        return self.path.name

    @property
    def suffix(self):
        return self.path.suffix.lower().lstrip('.').upper() or 'Unknown'

    @property
    def date_label(self):
        return self.modified.strftime('%Y-%m-%d')

    @property
    def month_label(self):
        return self.modified.strftime('%Y %B')

    @property
    def folder_label(self):
        return self.folder.name or str(self.folder)

    @property
    def location_label(self):
        parts = [p.lower().replace(' ', '-') for p in self.path.parts]
        for part in reversed(parts):
            if part in LOCATION_HINTS:
                return part.replace('-', ' ').title()
        return 'Unknown location'


class PhotoCard(CardWidget):
    """A compact thumbnail tile for one photo."""

    def __init__(self, photo: Photo, parent=None):
        super().__init__(parent)
        self.photo = photo
        self.setFixedSize(180, 214)

        self.imageLabel = QLabel(self)
        self.imageLabel.setFixedSize(156, 132)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setObjectName('thumbnail')

        pixmap = QPixmap(str(photo.path))
        if pixmap.isNull():
            self.imageLabel.setText('Preview')
        else:
            self.imageLabel.setPixmap(pixmap.scaled(
                self.imageLabel.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))

        self.nameLabel = StrongBodyLabel(photo.name, self)
        self.nameLabel.setFixedWidth(156)
        self.nameLabel.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.nameLabel.setToolTip(str(photo.path))

        self.metaLabel = CaptionLabel(
            f'{photo.date_label}  |  {photo.width}x{photo.height}', self
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        layout.addWidget(self.imageLabel, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.metaLabel)

        self.setStyleSheet("""
            PhotoCard { border-radius: 8px; }
            QLabel#thumbnail {
                border-radius: 6px;
                background: rgba(128, 128, 128, 24);
            }
        """)


class AlbumInterface(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.photos = []
        self.duplicateGroups = {}
        self.groupedPhotos = {}

        self.setObjectName('albumInterface')
        self.initWidgets()
        self.initLayout()
        self.connectSignals()
        self.refreshLibrary()

    def initWidgets(self):
        self.titleLabel = TitleLabel('Photo Album', self)
        self.subtitleLabel = CaptionLabel('Build a local photo library from one or more folders.', self)

        self.addFolderButton = PrimaryPushButton(FIF.ADD, 'Add folder', self)
        self.removeFolderButton = PushButton(FIF.REMOVE, 'Remove', self)
        self.scanButton = PushButton(FIF.SYNC, 'Scan', self)
        self.findDuplicatesButton = PushButton(FIF.SEARCH, 'Find duplicates', self)

        self.folderList = QListWidget(self)
        self.folderList.setMinimumWidth(260)
        self.folderList.setAlternatingRowColors(True)

        self.organizeComboBox = ComboBox(self)
        self.organizeComboBox.addItems(['Date', 'Month', 'Folder', 'Location', 'File type'])

        self.searchLineEdit = SearchLineEdit(self)
        self.searchLineEdit.setPlaceholderText('Search filename or folder')

        self.photoCountLabel = StrongBodyLabel('0 photos', self)
        self.duplicateCountLabel = CaptionLabel('0 duplicate candidates', self)

        self.groupList = QListWidget(self)
        self.groupList.setMinimumWidth(220)

        self.gridWidget = QWidget(self)
        self.gridLayout = QGridLayout(self.gridWidget)
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.gridLayout.setHorizontalSpacing(14)
        self.gridLayout.setVerticalSpacing(14)

        self.gridScrollArea = SmoothScrollArea(self)
        self.gridScrollArea.setWidget(self.gridWidget)
        self.gridScrollArea.setWidgetResizable(True)
        self.gridScrollArea.setFrameShape(QFrame.Shape.NoFrame)

        self.emptyLabel = BodyLabel('Add a folder and scan to populate the album.', self)
        self.emptyLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.emptyLabel)
        self.stack.addWidget(self.gridScrollArea)

        self.duplicatesTable = TableWidget(self)
        self.duplicatesTable.setColumnCount(5)
        self.duplicatesTable.setHorizontalHeaderLabels(['Delete', 'Group', 'File', 'Size', 'Path'])
        self.duplicatesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.duplicatesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.duplicatesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.duplicatesTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.duplicatesTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.duplicatesTable.verticalHeader().hide()
        self.duplicatesTable.setAlternatingRowColors(True)

        self.deleteButton = PushButton(FIF.DELETE, 'Delete checked duplicates', self)

    def initLayout(self):
        rootLayout = QVBoxLayout(self)
        rootLayout.setContentsMargins(24, 24, 24, 24)
        rootLayout.setSpacing(16)

        titleLayout = QVBoxLayout()
        titleLayout.setSpacing(2)
        titleLayout.addWidget(self.titleLabel)
        titleLayout.addWidget(self.subtitleLabel)

        commandLayout = QHBoxLayout()
        commandLayout.setSpacing(8)
        commandLayout.addWidget(self.addFolderButton)
        commandLayout.addWidget(self.removeFolderButton)
        commandLayout.addWidget(self.scanButton)
        commandLayout.addWidget(self.findDuplicatesButton)
        commandLayout.addStretch(1)
        commandLayout.addWidget(self.photoCountLabel)
        commandLayout.addWidget(self.duplicateCountLabel)

        filterLayout = QHBoxLayout()
        filterLayout.setSpacing(8)
        filterLayout.addWidget(BodyLabel('Organize by', self))
        filterLayout.addWidget(self.organizeComboBox)
        filterLayout.addWidget(self.searchLineEdit, 1)

        folderPanel = CardWidget(self)
        folderLayout = QVBoxLayout(folderPanel)
        folderLayout.setContentsMargins(14, 14, 14, 14)
        folderLayout.addWidget(StrongBodyLabel('Photo folders', folderPanel))
        folderLayout.addWidget(self.folderList, 1)

        groupPanel = CardWidget(self)
        groupLayout = QVBoxLayout(groupPanel)
        groupLayout.setContentsMargins(14, 14, 14, 14)
        groupLayout.addWidget(StrongBodyLabel('Groups', groupPanel))
        groupLayout.addWidget(self.groupList, 1)

        librarySplitter = QSplitter(Qt.Orientation.Horizontal, self)
        librarySplitter.addWidget(folderPanel)
        librarySplitter.addWidget(groupPanel)
        librarySplitter.addWidget(self.stack)
        librarySplitter.setStretchFactor(0, 0)
        librarySplitter.setStretchFactor(1, 0)
        librarySplitter.setStretchFactor(2, 1)

        duplicatePanel = CardWidget(self)
        duplicateLayout = QVBoxLayout(duplicatePanel)
        duplicateLayout.setContentsMargins(14, 14, 14, 14)
        duplicateLayout.setSpacing(10)
        duplicateHeader = QHBoxLayout()
        duplicateHeader.addWidget(StrongBodyLabel('Duplicate review', duplicatePanel))
        duplicateHeader.addStretch(1)
        duplicateHeader.addWidget(self.deleteButton)
        duplicateLayout.addLayout(duplicateHeader)
        duplicateLayout.addWidget(self.duplicatesTable)

        contentSplitter = QSplitter(Qt.Orientation.Vertical, self)
        contentSplitter.addWidget(librarySplitter)
        contentSplitter.addWidget(duplicatePanel)
        contentSplitter.setStretchFactor(0, 3)
        contentSplitter.setStretchFactor(1, 2)

        rootLayout.addLayout(titleLayout)
        rootLayout.addLayout(commandLayout)
        rootLayout.addLayout(filterLayout)
        rootLayout.addWidget(contentSplitter, 1)

    def connectSignals(self):
        self.addFolderButton.clicked.connect(self.addFolder)
        self.removeFolderButton.clicked.connect(self.removeSelectedFolder)
        self.scanButton.clicked.connect(lambda: self.scanFolders())
        self.findDuplicatesButton.clicked.connect(lambda: self.findDuplicates())
        self.deleteButton.clicked.connect(self.deleteCheckedDuplicates)
        self.organizeComboBox.currentTextChanged.connect(self.refreshLibrary)
        self.searchLineEdit.textChanged.connect(self.refreshLibrary)
        self.groupList.currentRowChanged.connect(self.refreshPhotoGrid)

    def folders(self):
        return [
            Path(self.folderList.item(i).text())
            for i in range(self.folderList.count())
        ]

    def addFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Choose a photo folder')
        if not folder:
            return

        path = Path(folder)
        if path in self.folders():
            return

        self.folderList.addItem(QListWidgetItem(str(path)))
        self.scanFolders()

    def removeSelectedFolder(self):
        for item in self.folderList.selectedItems():
            self.folderList.takeItem(self.folderList.row(item))
        self.scanFolders()

    def scanFolders(self, showInfo=True):
        photos = []
        for folder in self.folders():
            if not folder.exists():
                continue

            for path in folder.rglob('*'):
                if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
                    continue
                photo = self.readPhoto(path, folder)
                if photo:
                    photos.append(photo)

        self.photos = sorted(photos, key=lambda p: p.modified, reverse=True)
        self.duplicateGroups = {}
        self.refreshLibrary()
        self.refreshDuplicateTable()

        if showInfo:
            InfoBar.success(
                title='Scan complete',
                content=f'Indexed {len(self.photos)} photos from {len(self.folders())} folders.',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2200,
                parent=self.window()
            )

    def readPhoto(self, path: Path, root: Path):
        try:
            stat = path.stat()
            reader = QImageReader(str(path))
            size = reader.size()
            return Photo(
                path=path,
                folder=root,
                size=stat.st_size,
                modified=datetime.fromtimestamp(stat.st_mtime),
                width=max(size.width(), 0),
                height=max(size.height(), 0)
            )
        except OSError:
            return None

    def refreshLibrary(self):
        query = self.searchLineEdit.text().strip().lower() if hasattr(self, 'searchLineEdit') else ''
        photos = [
            p for p in self.photos
            if not query or query in p.name.lower() or query in str(p.path.parent).lower()
        ]

        grouped = defaultdict(list)
        mode = self.organizeComboBox.currentText() if hasattr(self, 'organizeComboBox') else 'Date'
        for photo in photos:
            grouped[self.groupKey(photo, mode)].append(photo)

        self.groupedPhotos = dict(sorted(grouped.items(), key=lambda item: item[0]))
        self.groupList.blockSignals(True)
        self.groupList.clear()
        for key, items in self.groupedPhotos.items():
            self.groupList.addItem(f'{key} ({len(items)})')
        self.groupList.blockSignals(False)

        if self.groupList.count():
            self.groupList.setCurrentRow(0)
        else:
            self.refreshPhotoGrid()

        self.photoCountLabel.setText(f'{len(self.photos)} photos')
        self.duplicateCountLabel.setText(f'{sum(len(v) - 1 for v in self.duplicateGroups.values())} duplicate candidates')

    def groupKey(self, photo: Photo, mode: str):
        if mode == 'Month':
            return photo.month_label
        if mode == 'Folder':
            return photo.folder_label
        if mode == 'Location':
            return photo.location_label
        if mode == 'File type':
            return photo.suffix
        return photo.date_label

    def refreshPhotoGrid(self):
        while self.gridLayout.count():
            item = self.gridLayout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        row = self.groupList.currentRow()
        keys = list(self.groupedPhotos)
        if row < 0 or row >= len(keys):
            self.stack.setCurrentWidget(self.emptyLabel)
            return

        photos = self.groupedPhotos[keys[row]]
        for index, photo in enumerate(photos[:120]):
            self.gridLayout.addWidget(PhotoCard(photo, self.gridWidget), index // 4, index % 4)

        if len(photos) > 120:
            moreLabel = CaptionLabel(f'{len(photos) - 120} more photos hidden in this demo grid.', self.gridWidget)
            self.gridLayout.addWidget(moreLabel, 30, 0, 1, 4)

        self.gridLayout.setRowStretch(31, 1)
        self.gridLayout.setColumnStretch(4, 1)
        self.stack.setCurrentWidget(self.gridScrollArea)

    def findDuplicates(self, showInfo=True):
        sizeGroups = defaultdict(list)
        for photo in self.photos:
            sizeGroups[photo.size].append(photo)

        duplicateGroups = defaultdict(list)
        for sameSizePhotos in sizeGroups.values():
            if len(sameSizePhotos) < 2:
                continue
            for photo in sameSizePhotos:
                digest = self.fileDigest(photo.path)
                if digest:
                    duplicateGroups[digest].append(photo)

        self.duplicateGroups = {
            digest: photos
            for digest, photos in duplicateGroups.items()
            if len(photos) > 1
        }
        self.refreshDuplicateTable()
        self.refreshLibrary()

        if showInfo:
            InfoBar.info(
                title='Duplicate scan complete',
                content=f'Found {sum(len(v) - 1 for v in self.duplicateGroups.values())} extra copies.',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2600,
                parent=self.window()
            )

    def fileDigest(self, path: Path):
        try:
            hasher = hashlib.sha256()
            with path.open('rb') as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except OSError:
            return ''

    def refreshDuplicateTable(self):
        self.duplicatesTable.setRowCount(0)
        row = 0
        for groupIndex, photos in enumerate(self.duplicateGroups.values(), start=1):
            for index, photo in enumerate(sorted(photos, key=lambda p: str(p.path))):
                self.duplicatesTable.insertRow(row)

                deleteItem = QTableWidgetItem()
                deleteItem.setFlags(deleteItem.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                deleteItem.setCheckState(
                    Qt.CheckState.Unchecked if index == 0 else Qt.CheckState.Checked
                )
                deleteItem.setData(Qt.ItemDataRole.UserRole, str(photo.path))
                self.duplicatesTable.setItem(row, 0, deleteItem)
                self.duplicatesTable.setItem(row, 1, QTableWidgetItem(str(groupIndex)))
                self.duplicatesTable.setItem(row, 2, QTableWidgetItem(photo.name))
                self.duplicatesTable.setItem(row, 3, QTableWidgetItem(self.formatSize(photo.size)))
                self.duplicatesTable.setItem(row, 4, QTableWidgetItem(str(photo.path)))
                row += 1

    def deleteCheckedDuplicates(self):
        paths = []
        for row in range(self.duplicatesTable.rowCount()):
            item = self.duplicatesTable.item(row, 0)
            if item and item.checkState() == Qt.CheckState.Checked:
                paths.append(Path(item.data(Qt.ItemDataRole.UserRole)))

        if not paths:
            InfoBar.warning(
                title='Nothing selected',
                content='Check duplicate rows before deleting.',
                orient=Qt.Orientation.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2200,
                parent=self.window()
            )
            return

        result = QMessageBox.question(
            self,
            'Delete duplicates',
            f'Move {len(paths)} checked duplicate files to the trash?'
        )
        if result != QMessageBox.StandardButton.Yes:
            return

        deleted = 0
        for path in paths:
            if self.moveToTrash(path):
                deleted += 1

        self.scanFolders(showInfo=False)
        self.findDuplicates(showInfo=False)
        InfoBar.success(
            title='Duplicates deleted',
            content=f'Moved {deleted} files to the trash.',
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2600,
            parent=self.window()
        )

    def moveToTrash(self, path: Path):
        result = QFile.moveToTrash(str(path))
        if isinstance(result, tuple):
            return bool(result[0])
        return bool(result)

    def formatSize(self, size):
        value = float(size)
        for unit in ('B', 'KB', 'MB', 'GB'):
            if value < 1024 or unit == 'GB':
                return f'{value:.1f} {unit}' if unit != 'B' else f'{int(value)} B'
            value /= 1024


class Window(FluentWindow):

    def __init__(self):
        super().__init__()
        self.albumInterface = AlbumInterface(self)
        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.addSubInterface(self.albumInterface, FIF.PHOTO, 'Photo album')

    def initWindow(self):
        self.resize(1180, 820)
        self.setMinimumSize(900, 640)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('Photo Album - PySide6-Fluent-Widgets')

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
