"""
Script to generate CSV files,
documenting the custom properties of model objects in a tabular format.

Assumptions:
    * Assumes models will be exported from __init__.py
      of ose3dprinter.app.model package
    * Assumes model class names end with a "Model" suffix (e.g. "FrameModel").
    * Assumes models classes only have one required argument in the constructor
      which is the Part::FeaturePython document object.
"""

from __future__ import print_function

import importlib
import os
from collections import OrderedDict

import FreeCAD as App
from osecore.app.cut_list import write_dict_list_to_csv


def main():
    model_module_name = 'ose3dprinter.app.model'

    model_module = importlib.import_module(model_module_name)
    models = [a for a in dir(model_module) if a.endswith('Model')]
    for model in models:
        class_ = getattr(model_module, model)

        document = App.newDocument()

        feature_python = document.addObject(
            'Part::FeaturePython', 'FeaturePython')
        feature_python_attrs = [x for x in dir(feature_python)]

        obj = document.addObject('Part::FeaturePython', 'FeaturePython')
        class_(obj)
        custom_obj_attrs = [x for x in dir(
            obj) if x not in feature_python_attrs]

        columns = ['Name', 'Type', 'Default Value', 'Description']
        rows = build_rows(custom_obj_attrs, obj)

        path_to_script = os.path.dirname(os.path.abspath(__file__))

        file = os.path.join(path_to_script, 'pages',
                            '{}PropertyTable.csv'.format(model))

        print('Writing {}'.format(file))

        write_dict_list_to_csv(rows, columns, file)


def build_rows(custom_obj_attrs, obj):
    rows = []
    for attr in custom_obj_attrs:
        description = obj.getDocumentationOfProperty(attr)
        property_type = obj.getTypeIdOfProperty(attr)
        human_readable_property = property_type.replace('App::Property', '')
        default_value = getattr(obj, attr)
        rows.append(OrderedDict([
            ('Name', '**{}**'.format(pascal_case_to_human_readable(attr))),
            ('Type', '``{}``'.format(human_readable_property)),
            ('Default Value', default_value),
            ('Description', description)
        ]))
    return rows


def pascal_case_to_human_readable(str):
    words = [[str[0]]]

    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)

    return ' '.join([''.join(word) for word in words])


if __name__ == '__main__':
    main()
