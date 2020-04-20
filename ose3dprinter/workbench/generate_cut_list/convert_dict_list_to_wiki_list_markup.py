from functools import reduce


def convert_dict_list_to_wiki_list_markup(dict_list):
    return reduce(row_to_list_item, dict_list, '')


def row_to_list_item(table_markup, row):
    list_item_template = u"* ['''{}'''] {} \u2014 {}\n"
    return table_markup + list_item_template.format(
        row['Quantity'], row['Description'], row['Length'])
