import os
import nltk
from nltk.tokenize import word_tokenize

# Keywords used for determing aspect based sentiment
completed_words = ['completed', 'performed', 'complete', 'perform', 'finished', 'finish']
recommend_words = ['rec', 'recommend', 'recommended', 'recommending']
declined_words = ['declined', 'deferred', 'dec', 'decline']

#Another aspect based sentiment is to find verbs and find their past
#or present tenses to determine seniment

#Simple Naive Sentiment Analysis Using Keywords and verb tensens
def sentimentAnalysis(n_gram_sentence, result):
    split_sentence = n_gram_sentence.split(' ')
    text = word_tokenize(n_gram_sentence)
    token_sentence = nltk.pos_tag(text)

    present_verbs = 0
    past_verbs = 0

    for c in completed_words:
        if c in split_sentence:
            result.write('1' + '\n')
            return 
    for r in recommend_words: 
        if r in split_sentence:
            result.write('0' + '\n')
            return
    for d in declined_words:
        if d in split_sentence:
            result.write('-1' + '\n')
            return
    
    for item in token_sentence:
        if item[1] == 'VBD' or item[1] == 'VBN':
            past_verbs += 1
        if item[1] == 'VB' or item[1] == 'VBG' or item[1] == 'VBP' or item[1] == 'VBZ':
            present_verbs += 1

    if present_verbs >= past_verbs:
        result.write('0' + '\n')
        return
    else:
        result.write('1' + '\n')
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
        
    
if __name__ == '__main__':
    readInData()
