import os

import FreeCADGui
from FreeCAD import Console
from osecore.app.cut_list import write_dict_list_to_csv
from PySide import QtGui

from .cut_list_task_panel_base import CutListTaskPanelBase


class SaveCutListAsCsvTaskPanel(CutListTaskPanelBase):

    def __init__(self, cut_list_table_rows, columns, note=None):
        title = 'Save Cut List as CSV'
        super(SaveCutListAsCsvTaskPanel, self).__init__(
            title, cut_list_table_rows, columns, note)
        self.cut_list_table_rows = cut_list_table_rows
        self.columns = columns

        path_to_default_file = find_available_path_to_default_file()
        self.path_to_default_file = path_to_default_file
        self.save_file_name = self.path_to_default_file

        row = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel(self.form)
        self.label.setObjectName('filenameLabel')
        self.set_label_text()
        row.addWidget(self.label)
        file_select_button = QtGui.QPushButton('Select Other File')
        file_select_button.clicked.connect(self.handle_file_select)
        row.addWidget(file_select_button)
        self.layout.addLayout(row)

    def handle_file_select(self):
        csv_filter = 'csv(*.csv)'
        save_file_name = QtGui.QFileDialog.getSaveFileName(
            self.form,
            'Select File',
            self.path_to_default_file,
            csv_filter)[0]
        if save_file_name != '':
            self.save_file_name = save_file_name
            self.set_label_text()

    def set_label_text(self):
        filename = os.path.basename(self.save_file_name)
        last_dir = os.path.split(os.path.dirname(self.save_file_name))[-1]
        display_text = os.path.join('...', last_dir, filename)
        self.label.setText('<b>File:</b> ' + display_text)

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        Console.PrintMessage(
            'Saving cut list as "{}".\n'.format(self.save_file_name))
        write_dict_list_to_csv(
            self.cut_list_table_rows,
            self.columns,
            self.save_file_name)
        FreeCADGui.Control.closeDialog()


def find_available_path_to_default_file():
    default_filename_template = 'cutlist{}.csv'
    path_to_desktop = os.path.expanduser('~/Desktop')
    path_to_default_file_template = os.path.join(
        path_to_desktop, default_filename_template)
    path_to_default_file = path_to_default_file_template.format('')
    if os.path.exists(path_to_default_file):
        i = 1
        while os.path.exists(path_to_default_file):
            path_to_default_file = path_to_default_file_template.format(i)
            i += 1
    return path_to_default_file
