# coding:utf-8
from typing import Callable, List, Tuple, Union

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout

from .button import PrimaryPushButton, PushButton
from .card_widget import SimpleCardWidget
from .label import BodyLabel, CaptionLabel, StrongBodyLabel, SubtitleLabel


Validator = Callable[[object], Union[bool, str, Tuple[bool, str], None]]


class ValidationSummary(SimpleCardWidget):
    """ Validation summary widget """

    def __init__(self, title='', parent=None):
        super().__init__(parent=parent)
        self.titleLabel = StrongBodyLabel(title or self.tr('Review the highlighted fields'), self)
        self.messageLabel = BodyLabel('', self)
        self.vBoxLayout = QVBoxLayout(self)

        self.messageLabel.setWordWrap(True)
        self.messageLabel.setTextColor(QColor(196, 43, 28), QColor(255, 153, 164))
        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(16, 14, 16, 14)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.messageLabel)
        self.hide()

    def setMessages(self, messages: List[str]):
        """ set validation messages """
        self.messageLabel.setText('\n'.join(messages))
        self.setVisible(bool(messages))


class FormField(QWidget):
    """ Form field with label, helper text and validation state """

    valueChanged = Signal(object)

    def __init__(self, label='', widget: QWidget = None, required=False, helperText='', parent=None):
        super().__init__(parent=parent)
        self._required = required
        self.validators = []  # type: List[Validator]

        self.label = StrongBodyLabel(self)
        self.requiredLabel = CaptionLabel('*', self)
        self.control = widget or QWidget(self)
        self.helperLabel = CaptionLabel(helperText, self)
        self.errorLabel = CaptionLabel('', self)

        self.vBoxLayout = QVBoxLayout(self)
        self.labelLayout = QHBoxLayout()

        self.__initWidget(label)
        self.__connectValueChanged()

    def __initWidget(self, label):
        self.setLabel(label)
        self.requiredLabel.setTextColor(QColor(196, 43, 28), QColor(255, 153, 164))
        self.requiredLabel.setVisible(self._required)
        self.helperLabel.setWordWrap(True)
        self.helperLabel.setTextColor(QColor(96, 96, 96), QColor(200, 200, 200))
        self.errorLabel.setWordWrap(True)
        self.errorLabel.setTextColor(QColor(196, 43, 28), QColor(255, 153, 164))
        self.errorLabel.hide()

        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLayout.setSpacing(4)
        self.labelLayout.setContentsMargins(0, 0, 0, 0)
        self.labelLayout.addWidget(self.label, 0, Qt.AlignLeft)
        self.labelLayout.addWidget(self.requiredLabel, 0, Qt.AlignLeft)
        self.labelLayout.addStretch(1)

        self.vBoxLayout.addLayout(self.labelLayout)
        self.vBoxLayout.addWidget(self.control)
        self.vBoxLayout.addWidget(self.helperLabel)
        self.vBoxLayout.addWidget(self.errorLabel)

    def __connectValueChanged(self):
        for signalName in ('textChanged', 'currentTextChanged', 'valueChanged', 'checkedChanged', 'stateChanged'):
            signal = getattr(self.control, signalName, None)
            if signal:
                signal.connect(lambda value=None: self.valueChanged.emit(self.value()))
                break

    def setLabel(self, label: str):
        """ set field label """
        self.label.setText(label)

    def setHelperText(self, text: str):
        """ set helper text """
        self.helperLabel.setText(text)
        self.helperLabel.setVisible(bool(text))

    def setRequired(self, isRequired: bool):
        """ set whether the field is required """
        self._required = isRequired
        self.requiredLabel.setVisible(isRequired)

    def isRequired(self):
        return self._required

    def addValidator(self, validator: Validator):
        """ add a field validator """
        self.validators.append(validator)

    def value(self):
        """ return the current control value """
        for name in ('text', 'currentText', 'value', 'isChecked'):
            getter = getattr(self.control, name, None)
            if getter:
                return getter()

        return None

    def validate(self):
        """ validate field and return `(isValid, message)` """
        value = self.value()
        if self.isRequired() and (value is None or str(value).strip() == ''):
            message = self.tr('This field is required.')
            self.setError(message)
            return False, message

        for validator in self.validators:
            result = validator(value)
            if result is None or result is True:
                continue

            if result is False:
                message = self.tr('The value is invalid.')
            elif isinstance(result, tuple):
                valid, message = result
                if valid:
                    continue
            else:
                message = str(result)

            self.setError(message)
            return False, message

        self.clearError()
        return True, ''

    def setError(self, message: str):
        """ set error message """
        self.errorLabel.setText(message)
        self.errorLabel.setVisible(bool(message))
        if hasattr(self.control, 'setError'):
            self.control.setError(bool(message))

    def clearError(self):
        """ clear error message """
        self.setError('')


class FormSection(SimpleCardWidget):
    """ Section container for form fields """

    def __init__(self, title='', content='', parent=None):
        super().__init__(parent=parent)
        self.titleLabel = SubtitleLabel(title, self)
        self.contentLabel = BodyLabel(content, self)
        self.fields = []  # type: List[FormField]

        self.vBoxLayout = QVBoxLayout(self)
        self.__initWidget()

    def __initWidget(self):
        self.contentLabel.setWordWrap(True)
        self.contentLabel.setTextColor(QColor(96, 96, 96), QColor(200, 200, 200))
        self.contentLabel.setVisible(bool(self.contentLabel.text()))

        self.vBoxLayout.setSpacing(14)
        self.vBoxLayout.setContentsMargins(20, 18, 20, 20)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)

    def addField(self, field: FormField):
        """ add a form field """
        self.fields.append(field)
        self.vBoxLayout.addWidget(field)
        return field


class FormWidget(QWidget):
    """ Form widget with validation summary and action row """

    submitted = Signal(dict)
    canceled = Signal()
    validationFailed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.fields = []  # type: List[FormField]
        self.summary = ValidationSummary(parent=self)
        self.submitButton = PrimaryPushButton(self.tr('Submit'), self)
        self.cancelButton = PushButton(self.tr('Cancel'), self)

        self.vBoxLayout = QVBoxLayout(self)
        self.actionLayout = QHBoxLayout()
        self.__initWidget()

    def __initWidget(self):
        self.vBoxLayout.setSpacing(14)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.summary)
        self.vBoxLayout.addStretch(1)

        self.actionLayout.setContentsMargins(0, 2, 0, 0)
        self.actionLayout.addStretch(1)
        self.actionLayout.addWidget(self.cancelButton)
        self.actionLayout.addWidget(self.submitButton)
        self.vBoxLayout.addLayout(self.actionLayout)

        self.submitButton.clicked.connect(self.submit)
        self.cancelButton.clicked.connect(self.canceled.emit)

    def addField(self, field: FormField):
        """ add a field to the form """
        self.fields.append(field)
        self.vBoxLayout.insertWidget(self.vBoxLayout.count() - 2, field)
        return field

    def addSection(self, section: FormSection):
        """ add a section and register its fields """
        for field in section.fields:
            if field not in self.fields:
                self.fields.append(field)

        self.vBoxLayout.insertWidget(self.vBoxLayout.count() - 2, section)
        return section

    def validate(self):
        """ validate all fields and return whether the form is valid """
        messages = []
        for field in self.fields:
            isValid, message = field.validate()
            if not isValid:
                messages.append(f'{field.label.text()}: {message}')

        self.summary.setMessages(messages)
        if messages:
            self.validationFailed.emit(messages)

        return not messages

    def values(self):
        """ return field values by label """
        return {field.label.text(): field.value() for field in self.fields}

    def submit(self):
        """ validate and emit submitted values """
        if self.validate():
            self.submitted.emit(self.values())
