# Cat-Dogs-Classifier
This Repository contains the implementation of Cat vs Dogs classifier.  
Dataset - [LINK](https://www.kaggle.com/c/dogs-vs-cats)

#### Implementation Pipeline
* Loading and splitting the dataset randomly into Train, test dataset 
* Loading the Resnet18 architecture ( change last layer of model for nu,ber of classes  = 2)
* Initialization of loss_criteria, optimizer and scheduler( leanring rate decay)
* Train model and calculate its accuracy on test dataset
