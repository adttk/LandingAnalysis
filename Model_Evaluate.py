#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

class Model_Evaluate ():
    
    def __init__(self):
        self.df = None
        self.df_train = None
        self.df_test = None
        self.knn = None
        self.test_prediction = None
        
    def set_dataset(self,df):
        self.df = df
    
    def KNN(self, train, test, n):
        
        train = train/100
        test = test/100
        
        # split data
        df_train, df_test = train_test_split(self.df,train_size =train, test_size = test)

        # Model KNN
        knn = KNeighborsClassifier(n_neighbors = n,metric = 'euclidean') # n_neighbors = k
        knn.fit(df_train[['latitude', 'longitude']],df_train['Abnormality'])
        
        #set attribute
        self.df_train = df_train
        self.df_test = df_test
        self.knn = knn
        self.test_prediction = knn.predict(self.df_test[['latitude', 'longitude']])
        self.df_test['prediction'] = self.test_prediction
    
    def KnnEval(self):        

        accuracy = round(accuracy_score(self.df_test['Abnormality'], self.test_prediction),3)
        precision = round(precision_score(self.df_test['Abnormality'], self.test_prediction),3)
        recall = round(recall_score(self.df_test['Abnormality'], self.test_prediction),3)
        f1 = round(f1_score(self.df_test['Abnormality'], self.test_prediction),3)

        KNN_eval = ('Accuracy : '+ str(accuracy)+'\n'+
        'Precision : '+ str(precision)+'\n'+
        'Recall : '+ str(recall)+'\n'+
        'F1 Score: '+ str(f1))
        
        return KNN_eval
        
    def confusion_matrix(self):
        conf_matrix = confusion_matrix(self.df_test['Abnormality'], self.test_prediction)

        fig, ax = plt.subplots(figsize=(3.21, 2.71))
        ax.matshow(conf_matrix, cmap=plt.cm.Oranges, alpha=0.3)
        for i in range(conf_matrix.shape[0]):
            for j in range(conf_matrix.shape[1]):
                ax.text(x=i, y=j,s=conf_matrix[i, j], va='center', ha='center', size=12)

        plt.xlabel('Predictions', fontsize=12)
        plt.ylabel('Actuals', fontsize=12)
        plt.title('Confusion Matrix', fontsize=15)
        plt.savefig('Model_KNN dan Confusion matrix/Confusion_matrix/CM_.png')
        plt.close()
        return 'Model_KNN dan Confusion matrix/Confusion_matrix/CM_.png'
        
    

