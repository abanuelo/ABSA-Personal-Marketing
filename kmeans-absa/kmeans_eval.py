import os

'''
Author: Armando Banuelos (abanuelo)
Created: 5-13-19
For questions, please connect
'''

#method will handle dealing with f1-metrics
def f1Metrics():
    #Since we have the true and we also have the not-true labels determining
    #The precision and accuracy from thos results
    eval_data = open('kmeans_ngrams_eval.txt', 'r')
    false_positives = 0
    true_positives = 0
    false_negatives = 0
    continue_calc = True
    absa_result = 0
    true_result = 0
    for line in eval_data:
        #Checking to see if the calculation can be performed for F1 metrics
        if continue_calc:
            if absa_result == true_result:
                true_positives += 1
            elif (absa_result == 0 and true_result == 1) or (absa_result == -1 and true_result == 1):
                false_positives += 1 
            elif (absa_result == 1 and true_result == 0) or (absa_result == 1 and true_result == -1):
                false_negatives += 1
            continue_calc = False
        if line == '0' + '\n' or line == '1' + '\n' or line == '-1' + '\n':
            absa_result = int(line.strip('\n'))
        if line == "True: " + '1' + '\n' or line == "True: " + '0' + '\n' or line == "True: " + '-1' + '\n': 
            array_of_num = line.strip('\n').split(' ')
            true_result = int(array_of_num[1])
            continue_calc = True
    print("Total True Positives: ", true_positives)
    print("Total False Negatives: ", false_negatives)
    print("Total False Positives: ", false_positives)
    print("Total Training Examples: ", false_negatives + false_positives + true_positives)
    precision = true_positives / float(true_positives + false_positives)
    recall = true_positives / float(true_positives + false_negatives)
    print('-'*50)
    print("Precion: ", precision)
    print("Recall: ", recall)
    F1 = 2*((precision*recall)/(precision + recall))
    print('-'*50)
    print("F1 Score Using Kmeans-ABSA: ", F1)
    return

if __name__ == '__main__':
    f1Metrics()