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
                        
        #f.writelines("-"*100 + '\n')  

#Will read through the list of files, format them appropriately, and write them to info.txt
if  __name__ == "__main__":
    f = open('info.txt','a')
    list_of_files = ['./data/AirConditioner.csv', './data/ABS.csv', './data/Airbag.csv', './data/Ball-Joint.csv', './data/CabinAirFilter.csv']
    importData(f, list_of_files)
    close(f)