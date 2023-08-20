#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import xlsxwriter

class Viz :
    
    dataset = None
    def set_dataset(self,df):
        self.dataset = df
   

    def scatter_plot(self):
        df = self.dataset
        plt.figure(figsize=(9, 4))
        df_normal = df[df['Abnormality'] == 0]
        plt.scatter(df_normal['latitude'], df_normal['longitude'], 
                    s = 70,
                    alpha = 0.7,
                    c = '#3d3d3d')

        df_abnormal = df[df['Abnormality'] == 1]
        plt.scatter(df_abnormal['latitude'], df_abnormal['longitude'], 
                    s = 70,
                    alpha = 0.7,
                    c = '#F22613')

        plt.xlabel('Latitude',
                   weight='bold',
                   size=10)

        plt.ylabel('Longitude',
                   weight='bold',
                   size=10)
        return plt    
        
    def get_pivot_count_airline(self):
        count_airlines = pd.DataFrame(self.dataset)
        count_airlines = count_airlines.groupby('airline_icao')
        count_airlines = count_airlines['airline_icao'].count()
        
                
        count_airlines = pd.DataFrame(count_airlines)
        count_airlines[''] = count_airlines.index
        count_airlines = count_airlines.reset_index(drop = True)
        column_to_move = count_airlines.pop('')
        count_airlines.insert(0, '', column_to_move)
        
        count_airlines=count_airlines.set_axis(['Airline icao' ,
                                                'Count of Flight'] ,
                                               axis ='columns')
        
        return count_airlines
    
    def get_pivot_count_aircraft(self):
        count_aircraft = pd.DataFrame(self.dataset)
        count_aircraft = count_aircraft.groupby('aircraft_code')
        count_aircraft = count_aircraft['aircraft_code'].count()
        
        count_aircraft = pd.DataFrame(count_aircraft)
        count_aircraft[''] = count_aircraft.index
        count_aircraft = count_aircraft.reset_index(drop = True)
        column_to_move = count_aircraft.pop('')
        count_aircraft.insert(0, '', column_to_move)
                  
        count_aircraft= count_aircraft.set_axis(['Aircraft code' ,
                                                 'Count of Flight'] ,
                                                axis ='columns')
        
        return count_aircraft
    
    def get_pivot_airline_of_all(self):
        df = pd.DataFrame(self.dataset)
        df = df.groupby(['airline_icao','Abnormality'])['Abnormality'].aggregate('count').unstack()
        df = df.fillna(0)
        
        df.columns.name = None
        df[''] = df.index
        df = df.reset_index(drop = True)
        column_to_move = df.pop('')
        df.insert(0, '', column_to_move)
                  
        df=df.set_axis(['Airline icao' ,
                        'Count of normal',
                        'Count of abnormal',],
                        axis ='columns')
        
        total_normal= sum(df['Count of normal'])
        total_abnormal= sum(df['Count of abnormal'])
        
        df['Percentage normal of all normal data (%)'] = round((df['Count of normal']/total_normal)*100, 2)
        df['Percentage abnormal of all abnormal data (%)'] = round((df['Count of abnormal']/total_abnormal)*100,2)
        return df

    def get_pivot_airline_of_self(self):
        df = pd.DataFrame(self.dataset)
        df = df.groupby(['airline_icao','Abnormality'])['Abnormality'].aggregate('count').unstack()
        df = df.fillna(0)
        
        df.columns.name = None
        df[''] = df.index
        df = df.reset_index(drop = True)
        column_to_move = df.pop('')
        df.insert(0, '', column_to_move)
        
        df=df.set_axis(['Airline icao' ,
                        'Count of normal',
                        'Count of abnormal'],
                        axis ='columns')

        df['Percentage normal of airline data (%)'] = round((df['Count of normal']/(df['Count of abnormal']+df['Count of normal']))*100,2)
        df['Percentage abnormal of airline data (%)'] = round((df['Count of abnormal']/(df['Count of abnormal']+df['Count of normal']))*100,2)
        return df
    
    def get_pivot_aircraft_of_all(self):
        
        df = pd.DataFrame(self.dataset)
        df = df.groupby(['aircraft_code','Abnormality'])['Abnormality'].aggregate('count').unstack()
        df = df.fillna(0)
        
        df.columns.name = None
        df[''] = df.index
        df = df.reset_index(drop = True)
        column_to_move = df.pop('')
        df.insert(0, '', column_to_move)

        df = df.set_axis(['Aircraft_code',
                        'Count of normal',
                        'Count of abnormal',],
                        axis ='columns')

        total_normal= sum(df['Count of normal'])
        total_abnormal= sum(df['Count of abnormal'])
        
        df['Percentage normal of all normal data (%)'] = round((df['Count of normal']/total_normal)*100, 2)
        df['Percentage abnormal of all abnormal data (%)'] = round((df['Count of abnormal']/total_abnormal)*100,2)
        return df
    
    def get_pivot_aircraft_of_self(self):
        df = pd.DataFrame(self.dataset)
        df = df.groupby(['aircraft_code','Abnormality'])['Abnormality'].aggregate('count').unstack()
        df = df.fillna(0)
        
        df.columns.name = None
        df[''] = df.index
        df = df.reset_index(drop = True)
        column_to_move = df.pop('')
        df.insert(0, '', column_to_move)
        
        df=df.set_axis(['Aircraft_code',
                        'Count of normal',
                        'Count of abnormal',],
                        axis ='columns')

        df['Percentage normal of aircraft data (%)'] = round((df['Count of normal']/(df['Count of abnormal']+df['Count of normal']))*100,2)
        df['Percentage abnormal of aircraft data (%)'] = round((df['Count of abnormal']/(df['Count of abnormal']+df['Count of normal']))*100,2)
        return df
    
    def histogram(self,df):
        plt.figure(figsize=(8, 4))
        plt.bar(df.iloc[:,[0]].squeeze(),
        df.iloc[:,[1]].squeeze(),
        width = 0.5)

        plt.xlabel(str(df.columns[0]),
                   weight='bold',
                   size=10)

        plt.ylabel('Count',
                   weight='bold',
                   size=10)
        return plt
    
    def adjustExcel(self,df,heatmap,path):
        writer = pd.ExcelWriter(path) 
        heatmap.to_excel(writer, index=False, na_rep='NaN')
        for column in df:
            column_length = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets['Sheet1'].set_column(col_idx, col_idx, column_length)

        writer.close()
        
    
    def heatmap(self,df):
        df = df.style.background_gradient(
            cmap='Greens',
            subset= str(df.columns[3])).background_gradient(
                                     cmap='Reds',
                                     subset= str(df.columns[4])).format(precision=2)
        return df