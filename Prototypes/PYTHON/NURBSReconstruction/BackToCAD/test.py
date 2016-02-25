import csv

from NURBSToSTEPAllraised import export_step

def parse_csv_into_matrix(csv_path, out_type):
    """
    parses a csv file into a list(list(out_type))
    :param csv_path: path to the file to be parsed
    :param out_type: defines the expected type. e.g. int or float
    :return: list(list(out_type)) holding content of csv
    """
    print "Parsing file at " + csv_path + "..."
    matrix = []
    with open(csv_path) as csvfile:
        idxreader = csv.reader(csvfile, delimiter=',')
        for row in idxreader:
            new_row = []
            for idx in row:
                new_row.append(out_type(float(idx)))
            matrix.append(new_row)
    print "File parsed."

    return matrix


def parse_all_from_folder(folder_path):
    """
    Parses a list holding all vertices and a list holding the indices of the vertices contributing to each patch from
    .csv input files. The input folder is defined above in the configuration.
    :param folder_path: path to folder holding the relevant csv fildes.
    :return: two list of vertices and vertex ids respectively
    """
    nurbs_idx = parse_csv_into_matrix(folder_path + '/NURBSPatchIndices.csv', int)
    nurbs_pts = parse_csv_into_matrix(folder_path + '/NURBSPatchPoints.csv', float)
    return nurbs_idx, nurbs_pts

nurbs_idx, nurbs_pts = parse_all_from_folder('./data')
export_step('blabla.step', nurbs_idx, nurbs_pts)