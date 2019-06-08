# ABSA-Personal-Marketing
Will apply several techniques such as kmeans clustering and lstm neural networks for aspect based sentiment analysis for personal marketing. The goal of this task is to provide insight to what automobile tasks were completed, declined, or recommended during inspections. That information can then be used to send personalized marketing to the customer based on their recommended and declined jobs. Any questions or concern on the information, please reach out at: abanuelo@stanford.edu

## Information to Run Models

### Bag of Words Baseline Method 1
Current kmeans ABSA Script is up and ready to run! Go into the bag-of-words folder and you will see the script.py. You can see the logic of the algorithm within the script. To run, please go to your command line / power shell and input: 'python3 script.py'. Right now, bag-of-words ABSA is generating F1-score to about 0.7 and overall accuracy of 0.6. Improvements in process. 

### ATAE-LSTM Method 2
Current attention based LSTM for aspect-level sentiment analysis (ATAE-LSTM) script is up and ready to run as well! In order to run this script there are other steps that need to be done prior to running the script. Complete the following steps below:

1. Download the following two pretrained word vectors: glove.42B.300d.zip and glove.twitter.27B.zip. Unzip the files and place them within the lstm-atae folder. Link for download can be located here: https://github.com/stanfordnlp/GloVe#download-pre-trained-word-vectors
2. Install pretrained bert neural network. To do so run the following on your command line / power shell: 'pip3 install pytorch-pretrained-bert'.

Now you should be ready to run the script. To do so, open up your command line / power shell and input: 'python3 script.py'. As of now, the ATAE-LSTM is generating F1-score of about 0.76 and overall accuracy of 0.8. However on keywords that the model has not trained on, it substantially overfits data. Improvements in process.

For more information about the architecture of the neural network, please visit: https://aclweb.org/anthology/D16-1058

### CABASC Method 3
Current CABASC model is ready to run. Please. Its script is still in the process of being constructed.
