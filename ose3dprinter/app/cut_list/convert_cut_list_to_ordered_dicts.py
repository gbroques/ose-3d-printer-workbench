from collections import OrderedDict


def convert_cut_list_to_ordered_dicts(cut_list):
    return list(map(convert_cut_list_item_to_ordered_dict, cut_list))


def convert_cut_list_item_to_ordered_dict(cut_list_dict):
    return OrderedDict([
        ('Quantity', cut_list_dict['quantity']),
        ('Description', cut_list_dict['description']),
        ('Length', cut_list_dict['length'])
    ])
