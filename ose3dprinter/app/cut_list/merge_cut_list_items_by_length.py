from collections import OrderedDict
from itertools import groupby
from operator import itemgetter

from .pluralize import pluralize


def merge_cut_list_items_by_length(cut_list_rows):
    """Merge cut list items with same length.

    This will combine descriptions.

    Note, we also pluralize the 'Description' if needed,
    so rows should have the 'Description' in singular form.

    :param cut_list_rows: cut list rows
    :type cut_list_rows: list(dict)
    """
    merged_cut_list_rows = []
    rows_by_length = group_by_length(cut_list_rows)
    for length, rows in rows_by_length:
        row_list = list(rows)
        first_row = row_list[0]
        if len(row_list) == 1:
            merged_cut_list_rows.append(OrderedDict([
                ('Quantity', first_row['Quantity']),
                ('Description', get_potentially_pluralized_description(first_row)),
                ('Length', first_row['Length'])
            ]))
        else:  # multiple rows with same length
            merged_cut_list_rows.append(OrderedDict([
                ('Quantity', sum_quantities(row_list)),
                ('Description', concatenate_descriptions(row_list)),
                ('Length', first_row['Length'])
            ]))
    return merged_cut_list_rows


def group_by_length(cut_list_rows):
    rows_sorted_by_length = sorted(cut_list_rows, key=lambda r: r['Length'])
    return groupby(rows_sorted_by_length, key=itemgetter('Length'))


def sum_quantities(cut_list_rows):
    return str(sum([int(row['Quantity']) for row in cut_list_rows]))


def concatenate_descriptions(cut_list_rows):
    first_row = cut_list_rows[0]
    description = stringify_cut_list_row(first_row)
    if len(cut_list_rows) == 2:
        second_row = cut_list_rows[1]
        return description + ' & ' + stringify_cut_list_row(second_row)

    rows_excluding_first_and_last = cut_list_rows[1:-1]
    for row in rows_excluding_first_and_last:
        description += ', ' + stringify_cut_list_row(row)

    last_row = cut_list_rows[len(cut_list_rows) - 1]
    return description + ', & ' + stringify_cut_list_row(last_row)


def stringify_cut_list_row(cut_list_row):
    return '({}) {}'.format(
        cut_list_row['Quantity'],
        get_potentially_pluralized_description(cut_list_row)
    )


def get_potentially_pluralized_description(cut_list_row):
    description = cut_list_row['Description']
    if int(cut_list_row['Quantity']) <= 1:
        return description
    else:
        return pluralize(description)


def pluralize_last_word(phrase):
    words = phrase.split(' ')
    last_word = words[len(words) - 1]
    pluralized_last_word = pluralize(last_word)
    return ' '.join(words[:-1] + [pluralized_last_word])
