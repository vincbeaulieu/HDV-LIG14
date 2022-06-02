
import pandas as pd
import csv
import os

# Return Pandas DataFrame and save output to CSV
def dataset_to_csv(filepath, dataset):
    dataframe = pd.DataFrame(dataset)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    dataframe.to_csv(filepath, index=False, header=False)
    return dataframe

# Read saved files and return 1D list
def reader(filepath):
    lines = []
    with open(filepath, 'r') as file:
        for line in file:
            lines.append(line[:-1])

    return lines

# Read saved files and return 2D list
def csv_reader(filepath,delimiter=','):
    table = []
    with open(filepath, newline='') as file:
        rows = csv.reader(file, delimiter=delimiter)
        for row in rows:
            table.append(row)
            
    return table

# Merge groups of n rows together. 
def merge(lines,n):
    index = 0
    tmp_flat = []
    flat_array = []
    for line in lines:
        if index == 0:
            tmp_flat = line.split(",")
        elif index % n != 0:
            tmp_flat = [*tmp_flat, *line.split(",")] 
        else:
            flat_array.append(tmp_flat)
            tmp_flat = line.split(",")
        index += 1
    flat_array.append(tmp_flat)
    return flat_array

def test():
    print("Testing Toolbox...")

    my_dataset = [10,20,30,40]
    filepath = 'python/test/my_dataset.csv'

    print("\nToolbox test :: Export dataset to csv :: return: Pandas Dataframe")
    my_dataframe = dataset_to_csv(filepath,my_dataset)
    print(my_dataframe)

    print("\nToolbox test :: File Reader :: return: List")
    my_file = reader(filepath)
    print(my_file)

    print("\nToolbox test :: Row Merger :: test_param = in groups of 2 :: return: List")
    my_file = merge(my_file,2)
    print(my_file)

    print("\nToolbox test :: CSV Reader :: return: List of Lists")
    my_dataset = [[10,20,30,40],[5,15,25,35]]
    filepath = 'python/test/my_csvdata.csv'
    my_dataframe = dataset_to_csv(filepath,my_dataset)
    my_csv = csv_reader(filepath)
    print(my_csv)

    pass