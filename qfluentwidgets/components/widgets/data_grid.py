# coding:utf-8
from typing import Callable, Iterable, List, Sequence, Tuple, Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidgetItem, QHeaderView

from .button import PushButton, ToolButton
from .combo_box import ComboBox
from .line_edit import SearchLineEdit
from .table_view import TableWidget
from .label import CaptionLabel
from .state_widget import EmptyStateWidget, LoadingOverlay
from ...common.icon import FluentIcon


DataGridColumn = Union[str, Tuple[str, str]]
DataGridRow = Union[dict, Sequence[object]]
DataGridAction = Tuple[str, Callable[[DataGridRow], None]]


class DataGridWidget(QWidget):
    """ Production-oriented data grid widget """

    rowActivated = Signal(object)
    pageChanged = Signal(int)
    filtered = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.columns = []  # type: List[Tuple[str, str]]
        self.rows = []  # type: List[DataGridRow]
        self.filteredRows = []  # type: List[DataGridRow]
        self.rowActions = []  # type: List[DataGridAction]
        self._page = 1
        self._pageSize = 10
        self._searchText = ''

        self.searchLineEdit = SearchLineEdit(self)
        self.pageSizeComboBox = ComboBox(self)
        self.tableWidget = TableWidget(self)
        self.emptyState = EmptyStateWidget(self.tr('No records'), self.tr('Try changing the search or filters.'), self)
        self.loadingOverlay = LoadingOverlay(self.tableWidget)
        self.previousButton = ToolButton(FluentIcon.LEFT_ARROW, self)
        self.nextButton = ToolButton(FluentIcon.RIGHT_ARROW, self)
        self.pageLabel = CaptionLabel(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.toolbarLayout = QHBoxLayout()
        self.footerLayout = QHBoxLayout()

        self.__initWidget()

    def __initWidget(self):
        self.searchLineEdit.setPlaceholderText(self.tr('Search'))
        self.searchLineEdit.setClearButtonEnabled(True)

        self.pageSizeComboBox.addItems(['10', '25', '50'])
        self.pageSizeComboBox.setCurrentIndex(0)
        self.pageSizeComboBox.setFixedWidth(92)

        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setBorderVisible(True)
        self.tableWidget.setBorderRadius(8)
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.setWordWrap(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

        self.emptyState.setIcon(FluentIcon.SEARCH)
        self.emptyState.hide()

        self.vBoxLayout.setSpacing(12)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.toolbarLayout.setContentsMargins(0, 0, 0, 0)
        self.footerLayout.setContentsMargins(0, 0, 0, 0)

        self.toolbarLayout.addWidget(self.searchLineEdit)
        self.toolbarLayout.addStretch(1)
        self.toolbarLayout.addWidget(CaptionLabel(self.tr('Rows'), self))
        self.toolbarLayout.addWidget(self.pageSizeComboBox)

        self.footerLayout.addStretch(1)
        self.footerLayout.addWidget(self.previousButton)
        self.footerLayout.addWidget(self.pageLabel)
        self.footerLayout.addWidget(self.nextButton)

        self.vBoxLayout.addLayout(self.toolbarLayout)
        self.vBoxLayout.addWidget(self.tableWidget)
        self.vBoxLayout.addWidget(self.emptyState)
        self.vBoxLayout.addLayout(self.footerLayout)

        self.searchLineEdit.textChanged.connect(self.setSearchText)
        self.pageSizeComboBox.currentTextChanged.connect(lambda text: self.setPageSize(int(text)))
        self.previousButton.clicked.connect(self.previousPage)
        self.nextButton.clicked.connect(self.nextPage)
        self.tableWidget.itemDoubleClicked.connect(lambda item: self.rowActivated.emit(item.data(Qt.UserRole)))

        self.__refresh()

    def setColumns(self, columns: Iterable[DataGridColumn]):
        """ set grid columns

        `columns` can be `['Name', 'Email']` or `[('name', 'Name'), ('email', 'Email')]`.
        """
        normalized = []
        for column in columns:
            if isinstance(column, tuple):
                normalized.append((column[0], column[1]))
            else:
                normalized.append((column, column))

        self.columns = normalized
        self.__refresh()

    def setRows(self, rows: Iterable[DataGridRow]):
        """ set grid rows """
        self.rows = list(rows)
        self._page = 1
        self.__refresh()

    def setRowActions(self, actions: Iterable[DataGridAction]):
        """ set row action buttons """
        self.rowActions = list(actions)
        self.__refresh()

    def setPageSize(self, size: int):
        """ set page size """
        self._pageSize = max(1, size)
        self._page = 1
        self.__refresh()

    def setSearchText(self, text: str):
        """ set search text """
        self._searchText = text.strip().lower()
        self._page = 1
        self.__refresh()

    def setLoading(self, isLoading: bool):
        """ show or hide loading overlay """
        self.loadingOverlay.setLoading(isLoading)

    def currentPage(self):
        return self._page

    def pageCount(self):
        if not self.filteredRows:
            return 1

        return (len(self.filteredRows) + self._pageSize - 1) // self._pageSize

    def nextPage(self):
        if self._page >= self.pageCount():
            return

        self._page += 1
        self.__populateTable()
        self.pageChanged.emit(self._page)

    def previousPage(self):
        if self._page <= 1:
            return

        self._page -= 1
        self.__populateTable()
        self.pageChanged.emit(self._page)

    def __refresh(self):
        self.filteredRows = self.__filteredRows()
        self.filtered.emit(len(self.filteredRows))
        self.__populateTable()

    def __filteredRows(self):
        if not self._searchText:
            return list(self.rows)

        return [row for row in self.rows if self._searchText in self.__searchText(row)]

    def __searchText(self, row: DataGridRow):
        values = [self.__cellValue(row, key) for key, _ in self.columns]
        return ' '.join(str(v).lower() for v in values)

    def __cellValue(self, row: DataGridRow, key: str):
        if isinstance(row, dict):
            return row.get(key, '')

        try:
            return row[int(key)]
        except (ValueError, IndexError, TypeError):
            return ''

    def __visibleRows(self):
        start = (self._page - 1) * self._pageSize
        return self.filteredRows[start:start + self._pageSize]

    def __populateTable(self):
        headers = [title for _, title in self.columns]
        if self.rowActions:
            headers.append(self.tr('Actions'))

        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)

        rows = self.__visibleRows()
        self.tableWidget.setRowCount(len(rows))

        for rowIndex, row in enumerate(rows):
            for columnIndex, (key, _) in enumerate(self.columns):
                item = QTableWidgetItem(str(self.__cellValue(row, key)))
                item.setData(Qt.UserRole, row)
                self.tableWidget.setItem(rowIndex, columnIndex, item)

            if self.rowActions:
                self.tableWidget.setCellWidget(rowIndex, len(self.columns), self.__createActionWidget(row))

        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setSortingEnabled(True)

        hasRows = bool(rows)
        self.tableWidget.setVisible(hasRows)
        self.emptyState.setVisible(not hasRows)
        self.previousButton.setEnabled(self._page > 1)
        self.nextButton.setEnabled(self._page < self.pageCount())
        self.pageLabel.setText(self.tr('Page {0} of {1}').format(self._page, self.pageCount()))

    def __createActionWidget(self, row: DataGridRow):
        widget = QWidget(self.tableWidget)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addStretch(1)

        for text, callback in self.rowActions:
            button = PushButton(text, widget)
            button.clicked.connect(lambda checked=False, r=row, cb=callback: cb(r))
            layout.addWidget(button)

        return widget
