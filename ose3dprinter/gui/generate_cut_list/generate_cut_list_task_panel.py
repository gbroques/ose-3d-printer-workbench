from PySide import QtCore, QtGui


class GenerateCutListTaskPanel(object):
    """Abstract base class for cut list task panels.

    Handles building cut list table and initializing layout.
    """

    def __init__(self, title, cut_list_table_rows, columns):
        self.cut_list_table_rows = cut_list_table_rows
        self.columns = columns

        self.form = QtGui.QWidget()
        self.form.setWindowTitle(title)
        self.layout = QtGui.QVBoxLayout(self.form)
        row = QtGui.QHBoxLayout()
        table = build_cut_list_table_widget(cut_list_table_rows, columns)
        self.layout.addLayout(row)
        row.addWidget(table)

        row2 = QtGui.QHBoxLayout()
        note = QtGui.QLabel(self.form)
        note.setObjectName('note')
        note.setText('<b>Note:</b> X and Z Rod lengths adjusted by +4" and -1" respectively.')
        note.setWordWrap(True)
        row2.addWidget(note)
        self.layout.addLayout(row2)

    def accept(self):
        """
        Executed upon clicking "OK" file_select_button in FreeCAD Tasks panel.
        """
        raise NotImplementedError('Must implement method accept()')


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
