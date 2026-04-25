# coding:utf-8
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (EmptyStateWidget, ErrorStateWidget, SkeletonWidget, LoadingOverlay,
                            FormWidget, FormSection, FormField, LineEdit, ComboBox, DataGridWidget,
                            PushButton, SimpleCardWidget, FluentIcon)

from .gallery_interface import GalleryInterface


class ProductionInterface(GalleryInterface):
    """ Production widgets interface """

    def __init__(self, parent=None):
        super().__init__(
            title=self.tr('Production'),
            subtitle='qfluentwidgets.components.widgets',
            parent=parent
        )
        self.setObjectName('productionInterface')

        self.addExampleCard(
            self.tr('Reusable empty, error and loading states'),
            StateSurfaceDemo(self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/state_widget/demo.py',
            stretch=1
        )

        self.addExampleCard(
            self.tr('A validated form section'),
            FormSurfaceDemo(self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/basic_input/form/demo.py',
            stretch=1
        )

        self.addExampleCard(
            self.tr('A searchable, paginated data grid'),
            DataGridSurfaceDemo(self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/view/data_grid/demo.py',
            stretch=1
        )


class StateSurfaceDemo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)

        emptyState = EmptyStateWidget(
            self.tr('No runs selected'),
            self.tr('Choose an experiment run to inspect metrics and predictions.'),
            self
        )
        emptyState.setIcon(FluentIcon.ROBOT)
        emptyState.setActionText(self.tr('Browse runs'))

        errorState = ErrorStateWidget(
            self.tr('Analysis failed'),
            self.tr('The report could not be generated from the selected dataset.'),
            self
        )
        errorState.setActionText(self.tr('Retry'))

        skeletonCard = SimpleCardWidget(self)
        skeletonLayout = QVBoxLayout(skeletonCard)
        skeleton = SkeletonWidget(skeletonCard)
        skeleton.setFixedHeight(120)
        loadingButton = PushButton(self.tr('Show loading overlay'), skeletonCard)
        overlay = LoadingOverlay(skeletonCard)
        overlay.setTitle(self.tr('Computing'))
        overlay.setContent(self.tr('Preparing feature importance'))
        loadingButton.clicked.connect(lambda: overlay.setLoading(not overlay.isLoading()))
        skeletonLayout.addWidget(skeleton)
        skeletonLayout.addWidget(loadingButton)

        self.hBoxLayout.addWidget(emptyState)
        self.hBoxLayout.addWidget(errorState)
        self.hBoxLayout.addWidget(skeletonCard)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSpacing(12)


class FormSurfaceDemo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.form = FormWidget(self)
        self.form.submitButton.setText(self.tr('Create run'))
        self.form.cancelButton.hide()

        section = FormSection(self.tr('Experiment'), self.tr('Capture the minimum metadata for a model run.'), self)

        nameEdit = LineEdit(self)
        nameEdit.setPlaceholderText(self.tr('churn-baseline-v2'))
        section.addField(FormField(self.tr('Run name'), nameEdit, required=True, parent=self))

        ownerEdit = LineEdit(self)
        ownerEdit.setPlaceholderText(self.tr('owner@example.com'))
        ownerField = FormField(self.tr('Owner'), ownerEdit, required=True, parent=self)
        ownerField.addValidator(lambda value: '@' in value or self.tr('Enter an email address.'))
        section.addField(ownerField)

        modelCombo = ComboBox(self)
        modelCombo.addItems(['Logistic regression', 'Random forest', 'Gradient boosting'])
        modelCombo.setMinimumWidth(220)
        section.addField(FormField(self.tr('Model'), modelCombo, parent=self))

        self.form.addSection(section)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.form)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)


class DataGridSurfaceDemo(DataGridWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(420)
        self.setColumns([
            ('run', self.tr('Run')),
            ('model', self.tr('Model')),
            ('accuracy', self.tr('Accuracy')),
            ('status', self.tr('Status')),
        ])
        self.setRows([
            {'run': 'baseline-001', 'model': 'Logistic regression', 'accuracy': '91.2%', 'status': 'Complete'},
            {'run': 'forest-014', 'model': 'Random forest', 'accuracy': '93.5%', 'status': 'Complete'},
            {'run': 'boost-022', 'model': 'Gradient boosting', 'accuracy': '94.8%', 'status': 'Complete'},
            {'run': 'boost-023', 'model': 'Gradient boosting', 'accuracy': '94.9%', 'status': 'Running'},
            {'run': 'linear-032', 'model': 'Linear SVM', 'accuracy': '90.6%', 'status': 'Failed'},
        ])
