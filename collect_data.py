import pandas as pd
import numpy as np
import math
import os

'''
Author: Armando Banuelos (abanuelo)
Created: 5-22-19

This python script allows us to collect the formated data within the './data/' folder
such as ABSA.csv, AirFilter.csv, etc using pandas pd
'''

#Method will import data and write the lines to a single file named info.txt
def importData(f, list_of_files): 
    for csv_file in list_of_files:
        df = pd.read_csv(csv_file)
        text = df['text']
        labels = df['label']

        for i in range(0, len(labels)):
            if (math.isnan(labels[i])==False):
                text_to_separate = text[i].split('|')
                word_to_analyze = text_to_separate[1]
                sentence = text_to_separate[0]
                f.writelines(sentence + '\n')
                f.writelines(word_to_analyze + '\n')
                f.writelines(str(int(labels[i])) + '\n')
            else:
                text_to_separate = text[i].split('|')
                word_to_analyze = text_to_separate[1]
                sentence = text_to_separate[0]
                f.writelines(sentence + '\n')
                f.writelines(word_to_analyze + '\n')
                f.writelines(str(2) + '\n')

    
#Will read through the list of files, format them appropriately, and write them to info.txt
if  __name__ == "__main__":
    f1 = open('./atae-lstm-cabasc/airconditioner.txt','w')
    curr_file = ['./data/AirConditioner.csv'] #'./data/ABS.csv', './data/Airbag.csv', './data/Ball-Joint.csv', './data/CabinAirFilter.csv', './data/MR-OIL.csv'
    path = './atae-lstm-cabasc/airconditioner.txt'
    importData(f1, curr_file)
    
    last_line = 0
    with open(path, 'r') as f1:
        content = f1.readlines()
        last_line = len(content)
    count = 1
    with open(path, 'w') as f1:
        for line in content:
            if count == last_line:
                f1.writelines(line.rstrip('\n'))
            else:
                f1.writelines(line)
            count += 1

    f2 = open("./atae-lstm-cabasc/abs.txt", 'w')
    curr_file = ['./data/ABS.csv']
    path = "./atae-lstm-cabasc/abs.txt"
    importData(f2, curr_file)

    last_line = 0
    with open(path, 'r') as f2:
        content = f2.readlines()
        last_line = len(content)
    count = 1
    with open(path, 'w') as f2:
        for line in content:
            if count == last_line:
                f2.writelines(line.rstrip('\n'))
            else:
                f2.writelines(line)
            count += 1

    f3 = open("./atae-lstm-cabasc/airbag.txt", 'w')
    curr_file = ['./data/Airbag.csv']
    path = "./atae-lstm-cabasc/airbag.txt"
    importData(f3, curr_file)

    last_line = 0
    with open(path, 'r') as f3:
        content = f3.readlines()
        last_line = len(content)
    count = 1
    with open(path, 'w') as f3:
        for line in content:
            if count == last_line:
                f3.writelines(line.rstrip('\n'))
            else:
                f3.writelines(line)
            count += 1

    f4 = open("./atae-lstm-cabasc/balljoint.txt", 'w')
    curr_file = ['./data/Ball-Joint.csv']
    path = "./atae-lstm-cabasc/balljoint.txt"
    importData(f4, curr_file)

    last_line = 0
    with open(path, 'r') as f4:
        content = f4.readlines()
        last_line = len(content)
    count = 1
    with open(path, 'w') as f4:
        for line in content:
            if count == last_line:
                f4.writelines(line.rstrip('\n'))
            else:
                f4.writelines(line)
            count += 1

    f5 = open("./atae-lstm-cabasc/cabinairfilter.txt", 'w')
    curr_file = ['./data/CabinAirFilter.csv']
    path = "./atae-lstm-cabasc/cabinairfilter.txt"
    importData(f5, curr_file)

    last_line = 0
    with open(path, 'r') as f5:
        content = f5.readlines()
        last_line = len(content)
    count = 1
    with open(path, 'w') as f5:
        for line in content:
            if count == last_line:
                f5.writelines(line.rstrip('\n'))
            else:
                f5.writelines(line)
            count += 1


    f6 = open("./atae-lstm-cabasc/oil.txt", 'w')
    curr_file = ['./data/MR-OIL.csv']
    path = "./atae-lstm-cabasc/oil.txt"
    importData(f6, curr_file)

    last_line = 0
    with open(path, 'r') as f6:
        content = f6.readlines()
        last_line = len(content)
    count = 1
    with open(path, 'w') as f6:
        for line in content:
            if count == last_line:
                f6.writelines(line.rstrip('\n'))
            else:
                f6.writelines(line)
            count += 1

