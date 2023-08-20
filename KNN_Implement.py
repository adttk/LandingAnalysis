#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from Model_Evaluate import Model_Evaluate


class KNN_Implement():
    def __init__(self):
        self.df = pd.read_csv('Data Model/dataset.csv')
        self.unseen = None

    def set_unseen(self, df):
        self.unseen = df

    def FixModel(self):
        knn = KNeighborsClassifier(
            n_neighbors=5, metric='euclidean')  # n_neighbors = k
        knn.fit(self.df[['latitude', 'longitude']], self.df['Abnormality'])
        return knn

    def Predict(self):
        knn = self.FixModel()
        unseen_prediction = knn.predict(self.unseen[['latitude', 'longitude']])

        # Hasil prediksi
        df_prediction = self.unseen.copy()
        df_prediction['Abnormality'] = unseen_prediction
        df_prediction.to_csv(
            'Model_KNN dan Confusion matrix\KNN\prediction_unseen.csv')
        return df_prediction
