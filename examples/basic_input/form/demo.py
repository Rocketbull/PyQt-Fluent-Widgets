# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import (FormWidget, FormSection, FormField, LineEdit, ComboBox,
                            CheckBox, InfoBar, InfoBarPosition, setTheme, Theme)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Form')
        self.resize(620, 520)

        self.form = FormWidget(self)
        self.profileSection = FormSection(
            self.tr('Profile'),
            self.tr('Form fields group labels, controls, helper text and validation state.'),
            self.form
        )

        nameEdit = LineEdit(self)
        nameEdit.setPlaceholderText(self.tr('Display name'))
        nameEdit.setClearButtonEnabled(True)
        nameField = FormField(self.tr('Name'), nameEdit, required=True, parent=self.form)
        nameField.setHelperText(self.tr('Use the name shown in the app header.'))

        emailEdit = LineEdit(self)
        emailEdit.setPlaceholderText('name@example.com')
        emailField = FormField(self.tr('Email'), emailEdit, required=True, parent=self.form)
        emailField.addValidator(lambda value: '@' in value or self.tr('Enter a valid email address.'))

        roleCombo = ComboBox(self)
        roleCombo.addItems([self.tr('Designer'), self.tr('Engineer'), self.tr('Product manager')])
        roleCombo.setMinimumWidth(220)
        roleField = FormField(self.tr('Role'), roleCombo, parent=self.form)

        termsCheckBox = CheckBox(self.tr('I agree to receive product updates.'), self)
        termsField = FormField(self.tr('Updates'), termsCheckBox, parent=self.form)

        self.profileSection.addField(nameField)
        self.profileSection.addField(emailField)
        self.profileSection.addField(roleField)
        self.profileSection.addField(termsField)

        self.form.addSection(self.profileSection)
        self.form.submitted.connect(self.onSubmitted)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.form)
        self.vBoxLayout.setContentsMargins(24, 24, 24, 24)

    def onSubmitted(self, values):
        InfoBar.success(
            title=self.tr('Saved'),
            content=self.tr('The form values passed validation.'),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setTheme(Theme.AUTO)
    w = Demo()
    w.show()
    app.exec()
