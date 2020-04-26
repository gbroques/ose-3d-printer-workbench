import FreeCAD as App
import FreeCADGui as Gui
import Part
from ose3dprinter.app.model.frame.angle_frame_connector import \
    AngleFrameConnector
from ose3dprinter.app.model.frame.corner import Corner
from PySide import QtGui


class AngleFrameConnectorTaskPanel:

    def __init__(self):
        self.form = QtGui.QWidget()
        self.form.setWindowTitle('Make Angle Frame Connector')
        layout = QtGui.QVBoxLayout(self.form)

        # ---------
        # | Width |
        # ---------
        row1 = QtGui.QHBoxLayout()
        layout.addLayout(row1)

        self.create_label('widthLabel', 'Slot Width', row1)
        default_width = 38.1  # 1.5 inch
        self.widthInputField = self.create_input_field(
            'width', default_width, row1)

        # -------------
        # | Thickness |
        # -------------
        row2 = QtGui.QHBoxLayout()
        layout.addLayout(row2)

        self.create_label('thicknessLabel', 'Slot Thickness', row2)
        default_thickness = 3.175  # 1/8 inch
        self.thicknessInputField = self.create_input_field(
            'thickness', default_thickness, row2)

        # ---------------
        # | Orientation |
        # ---------------
        row3 = QtGui.QHBoxLayout()
        layout.addLayout(row3)

        self.create_label('orientationLabel', 'Orientation', row3)
        self.orientationComboBox = QtGui.QComboBox(self.form)
        self.orientationComboBox.setObjectName('orientation')
        corner_options = get_corner_combo_box_options()
        self.orientationComboBox.addItems(corner_options)
        size_policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.orientationComboBox.setSizePolicy(size_policy)
        self.orientationComboBox.setMinimumWidth(110)
        row3.addWidget(self.orientationComboBox)

        # -------------
        # | Set Screw |
        # -------------
        row4 = QtGui.QHBoxLayout()
        layout.addLayout(row4)

        self.create_label('setScrewLabel', 'Add Set Screw (M6)', row4)
        self.setScrewCheckbox = QtGui.QCheckBox(self.form)
        self.setScrewCheckbox.setObjectName('setScrew')
        size_policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.setScrewCheckbox.setSizePolicy(size_policy)
        self.setScrewCheckbox.setMinimumWidth(110)
        row4.addWidget(self.setScrewCheckbox)

        # -------------
        # | Filleting |
        # -------------
        row5 = QtGui.QHBoxLayout()
        layout.addLayout(row5)

        self.create_label('filletLabel', 'Add Filleting', row5)
        self.filletCheckbox = QtGui.QCheckBox(self.form)
        self.filletCheckbox.setObjectName('fillet')
        self.filletCheckbox.setChecked(True)
        size_policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        self.filletCheckbox.setSizePolicy(size_policy)
        self.filletCheckbox.setMinimumWidth(110)
        row5.addWidget(self.filletCheckbox)

    def create_input_field(self, name, default_value, layout):
        ui_loader = Gui.UiLoader()
        input_field = ui_loader.createWidget('Gui::InputField')
        input_field.setObjectName(name)
        size_policy = QtGui.QSizePolicy(
            QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        input_field.setSizePolicy(size_policy)
        input_field.setMinimumWidth(110)
        input_field.installEventFilter(self.form)
        input_field.setText(App.Units.Quantity(
            default_value, App.Units.Length).UserString)
        layout.addWidget(input_field)
        return input_field

    def create_label(self, name, text, layout):
        label = QtGui.QLabel(self.form)
        label.setObjectName(name)
        label.setText(text)
        layout.addWidget(label)
        return label

    def accept(self):
        """
        Executed upon clicking "OK" button in FreeCAD Tasks panel.
        """
        width = self.widthInputField.property('quantity').Value
        thickness = self.thicknessInputField.property('quantity').Value
        orientation_text = self.orientationComboBox.currentText()
        orientation = title_case_to_snake_case(orientation_text)
        with_set_screw = self.setScrewCheckbox.isChecked()
        with_filleting = self.filletCheckbox.isChecked()

        connector = AngleFrameConnector.make(
            width, thickness, orientation, with_set_screw, with_filleting)
        Part.show(connector)
        Gui.Control.closeDialog()


def get_corner_combo_box_options():
    corners = [getattr(Corner, x)
               for x in dir(Corner) if not x.startswith('__')]
    return map(snake_case_to_title_case, corners)


def snake_case_to_title_case(string):
    return ' '.join(w.capitalize() for w in string.split('_'))


def title_case_to_snake_case(string):
    return '_'.join(w.lower() for w in string.split(' '))
