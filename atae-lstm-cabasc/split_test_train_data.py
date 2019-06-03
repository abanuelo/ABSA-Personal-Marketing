import os
import numpy as np
import math 

#Method will be used to distribute data to allocated areas
def distributeData(f, train, test):
    line_count = 0
    writeToTest = False
    for line in f:
        #reset line_count one we have iterated over values
        if line_count == 3:
            line_count = 0
        #Check to see if we are at sentence, keyword, or sentiment analysis
        if (line_count == 0):
            split_decision = np.random.randint(low=1, high=100, size=1)
            if (split_decision[0] <= 20):
                test.writelines(line)
                writeToTest = True
            else:
                train.writelines(line)
                writeToTest = False
        elif (line_count == 1) or (line_count == 2):
            if writeToTest:
                test.writelines(line)
            else:
                train.writelines(line)
        line_count += 1

if __name__ == '__main__':
    #Open the files, train and test will hold data to pass into attenion-based lstm
    #Note: Change created to create test and training data for each category type
    f1 = open('abs.txt', 'r')
    train = open('./datasets/semeval14/ABS_Train.xml.seg', 'w')
    test = open('./datasets/semeval14/ABS_Test_Gold.xml.seg', 'w')
    #Function will allocate a 80/20 split train/test for data
    distributeData(f1, train, test)
    
    f2 = open("airbag.txt", 'r')
    train = open('./datasets/semeval14/Airbag_Train.xml.seg', 'w')
    test = open('./datasets/semeval14/Airbag_Test_Gold.xml.seg', 'w')
    distributeData(f2, train, test)

    f3 = open("airconditioner.txt", 'r')
    train = open('./datasets/semeval14/AirConditioner_Train.xml.seg', 'w')
    test = open('./datasets/semeval14/AirConditioner_Test_Gold.xml.seg', 'w')
    distributeData(f3, train, test)

    f4 = open("balljoint.txt", 'r')
    train = open('./datasets/semeval14/Balljoint_Train.xml.seg', 'w')
    test = open('./datasets/semeval14/Balljoint_Test_Gold.xml.seg', 'w')
    distributeData(f4, train, test)

    f5 = open('cabinairfilter.txt', 'r')
    train = open('./datasets/semeval14/CabinAirFilter_Train.xml.seg', 'w')
    test = open('./datasets/semeval14/CabinAirFilter_Test_Gold.xml.seg', 'w')
    distributeData(f5, train, test)

    f6 = open("oil.txt", 'r')
    train = open('./datasets/semeval14/Oil_Train.xml.seg', 'w')
    test = open('./datasets/semeval14/Oil_Test_Gold.xml.seg', 'w')
    distributeData(f6, train, test)


