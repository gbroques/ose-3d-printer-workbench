import FreeCADGui
from FreeCAD import Console
from osecore.app.cut_list import (convert_dict_list_to_wiki_list_markup,
                                  convert_dict_list_to_wiki_table_markup)
from PySide import QtGui

from .cut_list_task_panel_base import CutListTaskPanelBase


class CopyCutListToClipboardTaskPanel(CutListTaskPanelBase):

    def __init__(self, cut_list_table_rows, columns, note=None):
        title = 'Copy Cut List to Clipboard'
        super(CopyCutListToClipboardTaskPanel, self).__init__(
            title, cut_list_table_rows, columns, note)

        # Row 1 - Markup Format options
        row1 = QtGui.QVBoxLayout()

        # Table option
        self.table_option = QtGui.QRadioButton('Table', self.form)
        self.table_option.setChecked(True)
        row1.addWidget(self.table_option)

        # List option
        self.list_option = QtGui.QRadioButton('List', self.form)
        row1.addWidget(self.list_option)

        self.layout.addLayout(row1)

        # ----------------------------------

        # Row 2
        row2 = QtGui.QHBoxLayout()

        # Copy Status Label
        self.copyStatusLabel = QtGui.QLabel(self.form)
        self.copyStatusLabel.setObjectName('copyStatusLabel')
        self.copyStatusLabel.setText('<b>Status:</b> Not Copied')
        row2.addWidget(self.copyStatusLabel)

        # Copy to Clipboard button
        copy_to_clipboard_button = QtGui.QPushButton(
            'Copy to Clipboard')
        copy_to_clipboard_button.clicked.connect(self.handle_copy_to_clipboard)
        row2.addWidget(copy_to_clipboard_button)

        self.layout.addLayout(row2)

    def handle_copy_to_clipboard(self):
        clipboard = QtGui.QApplication.clipboard()
        table_markup = ''
        if self.table_option.isChecked():
            table_markup = convert_dict_list_to_wiki_table_markup(
                self.cut_list_table_rows, self.columns)
        elif self.list_option.isChecked():
            table_markup = convert_dict_list_to_wiki_list_markup(
                self.cut_list_table_rows)
        else:
            raise ValueError('Table or list option must be checked.')
        clipboard.setText(table_markup)
        self.copyStatusLabel.setText('<b>Status:</b> Copied!')
        Console.PrintMessage('Copied table markup to clipboard.\n')

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        self.handle_copy_to_clipboard()
        FreeCADGui.Control.closeDialog()
