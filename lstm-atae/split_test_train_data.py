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
    f = open('./train_test_data.txt', 'r')
    train = open('./datasets/semeval14/Car_Train.xml.seg', 'w')
    test = open('./datasets/semeval14/Car_Test_Gold.xml.seg', 'w')
    #Function will allocate a 80/20 split train/test for data
    distributeData(f, train, test)
    #Close files to avoid memory leaks
    # close(f)
    # close(train)
    # close(test)

