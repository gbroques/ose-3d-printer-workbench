from PySide import QtCore, QtGui


class CutListTaskPanelBase:
    """Base class for cut list task panels.

    Handles building cut list table and initializing layout.
    """

    def __init__(self, title, cut_list_table_rows, columns, note=None):
        self.cut_list_table_rows = cut_list_table_rows
        self.columns = columns

        self.form = QtGui.QWidget()
        self.form.setWindowTitle(title)
        self.layout = QtGui.QVBoxLayout(self.form)
        row = QtGui.QHBoxLayout()
        table = build_cut_list_table_widget(cut_list_table_rows, columns)
        self.layout.addLayout(row)
        row.addWidget(table)

        if note is not None:
            row2 = QtGui.QHBoxLayout()
            note_label = QtGui.QLabel(self.form)
            note_label.setObjectName('note_label')
            note_text = '<b>Note:</b> {}'.format(note)
            note_label.setText(note_text)
            note_label.setWordWrap(True)
            row2.addWidget(note_label)
            self.layout.addLayout(row2)

    def accept(self):
        """
        Executed upon clicking "OK" file_select_button in FreeCAD Tasks panel.
        """
        raise NotImplementedError('Sub class must implement accept() method.')


def build_cut_list_table_widget(cut_list_table_rows, columns):
    num_rows = len(cut_list_table_rows)
    num_columns = len(columns)
    table = QtGui.QTableWidget(num_rows, num_columns)
    table.setHorizontalHeaderLabels(columns)

    for row_index, row in enumerate(cut_list_table_rows):
        for column_index, value in enumerate(row.values()):
            item = QtGui.QTableWidgetItem(value)
            # make table cell not editable
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            item.setToolTip(value)
            table.setItem(row_index, column_index, item)

    header = table.horizontalHeader()
    header.setResizeMode(QtGui.QHeaderView.Stretch)
    return table
