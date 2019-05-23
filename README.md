# ABSA-Personal-Marketing
Will apply several techniques such as kmeans clustering and lstm neural networks for aspect based sentiment analysis for personal marketing. The goal of this task is to provide insight to what automobile tasks were completed, declined, or recommended during inspections. That information can then be used to send personalized marketing to the customer based on their recommended and declined jobs. Any questions or concern on the information, please reach out at: abanuelo@stanford.edu

## Update as of 5-22-19

### Kmeans ABSA Method 1
Current kmeans ABSA Script is up and ready to run! Go into the kmeans-absa folder and you will see the script.py. You can see the logic of the algorithm within the script. To run, please go to your command line / power shell and input: 'python3 script.py'. Right now, kmeans ABSA is generating F1-score to about 0.9 and overall accuracy of 0.87. Improvements in process. 

### ATAE-LSTM Method 2
Current attention based LSTM for aspect-level sentiment analysis (ATAE-LSTM) script is up and ready to run as well! In order to run this script there are other steps that need to be done prior to running the script. Complete the following steps below:

1. Download the following two pretrained word vectors: glove.42B.300d.zip and glove.twitter.27B.zip. Unzip the files and place them within the lstm-atae folder. Link for download can be located here: https://github.com/stanfordnlp/GloVe#download-pre-trained-word-vectors
2. Install pretrained bert neural network. To do so run the following on your command line / power shell: 'pip3 install pytorch-pretrained-bert'.

Now you should be ready to run the script. To do so, open up your command line / power shell and input: 'python3 script.py'. As of now, the ATAE-LSTM is generating F1-score of about 0.85 and overall accuracy of 0.93. However on keywords that the model has not trained on, it substantially overfits data. Improvements in process.

For more information about the architecture of the neural network, please visit: https://aclweb.org/anthology/D16-1058
