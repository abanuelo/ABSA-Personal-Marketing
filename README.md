# ABSA-Personal-Marketing
Will apply several techniques such as ngrams bag of words, lstm neural networks, and GRU layers for aspect based sentiment analysis for personal marketing. The goal of this task is to provide insight to what automobile tasks were completed, declined, or recommended during automobile mechanic reports. That information can then be used to send personalized marketing to the customer based on their recommended and declined jobs. For more details please navigate to the documentation folder or the wiki for this repo. Any questions or concern on the information, please reach out at: abanuelo@stanford.edu

## Results of Models

### Ngrams Bag of Words - Baseline Method 1
Ngrams bag-of-words ABSA is generating an overall accuracy of 0.34. Lenient Baseline. 

### Content Attention Based Aspect Based Sentiment Analysis (CABASC) - Method 2
CABASC model currently performs at 60% accuracy averaged across all servicing categories included in this report. For more information of servicing categories please see data CSV files.

For more information about the architecture of the neural network, please see Technical Report in documentation. 

### Attention Based Long Term Short Term Memory (ATAE-LSTM) - Method 3
ATAE-LSTM model currently performs at 80% accuracy averaged across all servicing categories included in this report. For more information of servicing categories please see data CSV files.

Please take note that, fine-tuning of model has been performed and a model was trained on each servicing category. To test individual servicing categories please see wiki for more details. 

For more information about the architecture of the neural network, please see Technical Report in documentation.
