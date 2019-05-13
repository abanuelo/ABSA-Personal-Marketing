import os
import nltk
from nltk.tokenize import word_tokenize

# Keywords used for determing aspect based sentiment
completed_words = ['completed', 'performed', 'complete', 'perform', 'finished', 'finish', 'performing', 'completing', 'finishing']
recommend_words = ['rec', 'recommend', 'recommended', 'recommending', 'need', 'needs', 'recommendations', 'recommendation', 'requires', 'required', 'require']
declined_words = ['declined', 'deferred', 'dec', 'decline', 'defer', 'declining', 'deferring']

#Another aspect based sentiment is to find verbs and find their past
#or present tenses to determine seniment

#Simple Naive Sentiment Analysis Using Keywords and verb tensens
def sentimentAnalysis(n_gram_sentence, result):
    split_sentence = n_gram_sentence.split(' ')
    text = word_tokenize(n_gram_sentence)
    token_sentence = nltk.pos_tag(text)

    present_verbs = 0
    past_verbs = 0

    for d in declined_words:
        if d in split_sentence:
            result.write('-1' + '\n')
            result.write('True: ' + '\n')
            return
    for r in recommend_words: 
        if r in split_sentence:
            result.write('0' + '\n')
            result.write('True: ' + '\n')
            return
    for c in completed_words:
        if c in split_sentence:
            result.write('1' + '\n')
            result.write('True: ' + '\n')
            return
    
    for item in token_sentence:
        if item[1] == 'VBD' or item[1] == 'VBN':
            past_verbs += 1
        if item[1] == 'VB' or item[1] == 'VBG' or item[1] == 'VBP' or item[1] == 'VBZ':
            present_verbs += 1

    if present_verbs >= past_verbs:
        result.write('1' + '\n')
        result.write('True: ' + '\n')
        return
    else:
        result.write('1' + '\n')
        result.write('True: ' + '\n')
        return
    return
        

def readInData():
    file = open('kmeans_ngrams.txt', 'r')
    result = open('kmeans_ngrams_result.txt', 'w')

    readNextLine = False
    firstLineRead = True

    keyword = ""
    n_gram_sentence = ""

    for line in file:
        result.write(line)
        if (line == '-'*100 + '\n'):
            readNextLine = False
        
        if readNextLine:
            if firstLineRead:
                keyword = line.strip('\n')
                firstLineRead = False
            else:
                n_gram_sentence = line.strip('\n')
                firstLineRead = True
                sentimentAnalysis(n_gram_sentence, result)

        if (line == '.'*100 + '\n'):
            readNextLine = True

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
                false_negative += 1
            continue_calc = False
        if line == '0' + '\n' or line == '1' + '\n' or line == '-1' + '\n':
            absa_result = int(line.strip('\n'))
        if line == "True: " + '1' + '\n' or line == "True: " + '0' + '\n' or line == "True: " + '-1' + '\n': 
            true_result = int(line.strip.('\n').split(' ')[1])
            continue_calc = True
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)
    F1 = 2*((precision*recall)/(precision + recall))
    print("F1 Score Using Kmeans-ABSA: ", F1)
    return

    
if __name__ == '__main__':
    readInData()
    f1Metrics()
