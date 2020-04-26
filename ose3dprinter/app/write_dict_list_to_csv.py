import csv

from FreeCAD import Console


def write_dict_list_to_csv(dict_list, columns, filename):
    try:
        with open(filename, 'w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            for row in dict_list:
                writer.writerow(row)
    except IOError as e:
        Console.PrintError(str(e))
