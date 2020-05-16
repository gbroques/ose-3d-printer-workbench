def convert_dict_list_to_wiki_table_markup(dict_list, columns):
    """
    See:
        https://www.mediawiki.org/wiki/Help:Tables#Wiki_table_markup_summary

    :param dict_list: list of dictionaries
    :type dict_list: List(Dict)
    :param columns: Columns of table
    :type columns: list of strings
    :return: wiki table markup
    :rtype: string
    """
    table = '{| class="wikitable"\n'
    row_separator = '|----\n'
    for column in columns:
        table += '!|{}\n'.format(column)
    table += row_separator
    for row in dict_list:
        for value in row.values():
            table += '|{}\n'.format(value)
        table += row_separator
    return table + '|}\n'
