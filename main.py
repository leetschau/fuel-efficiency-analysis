#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 12:13:11 2017

@author: leo

This script is the implementation of chapter 7 "Driving Visual Analyses with Automobile Data" 
of "Practical Data Science Cookbook" by Tony Ojeda, etc.
"""
#%%  Section Analyzing automobile fuel efficiency over time with Python
# -------------------------------------------
import pandas as pd
import numpy as np

vehicles = pd.read_csv("vehicles.csv")

column_names = vehicles.columns.values
column_names[[22, 23, 70, 71, 72, 73]]
len(vehicles)
len(vehicles.columns)
vehicles.columns
len(pd.unique(vehicles.year))
min(vehicles.year)
max(vehicles.year)
pd.value_counts(vehicles.fuelType1)
pd.value_counts(vehicles.trany)
vehicles["trany2"] = vehicles.trany.str[0]
pd.value_counts(vehicles.trany2)

#%% step 1 ~ 4 on Page 202
from ggplot import ggplot, aes, geom_point, xlab, ylab, ggtitle

grouped = vehicles.groupby("year")
averaged = grouped['comb08', 'highway08', 'city08'].agg([np.mean])
averaged.columns = ['comb08_mean', 'highway08_mean', 'city08_mean']
averaged['year'] = averaged.index

print(ggplot(averaged, aes('year', 'comb08_mean')) +
      geom_point(color='steelblue') +
      xlab('Year') +
      ylab('Average MPG') +
      ggtitle('All cars'))

#%% step 5
criteria1 = vehicles.fuelType1.isin(['Regular Gasoline', 'Prenium Gasoline', 'Midgrade Gasoline'])
criteria2 = vehicles.fuelType2.isnull()
criteria3 = vehicles.atvType != 'Hybrid'
vehicles_non_hybrid = vehicles[criteria1 & criteria2 & criteria3]
len(vehicles_non_hybrid)

#%% step 6
grouped = vehicles_non_hybrid.groupby(['year'])
averaged = grouped['comb08'].agg([np.mean])
print(averaged)

#%% step 7 ~ 9
pd.unique(vehicles_non_hybrid.displ)

criteria = vehicles_non_hybrid.displ.notnull()
vehicles_non_hybrid = vehicles_non_hybrid[criteria]
vehicles_non_hybrid.displ = vehicles_non_hybrid.displ.astype('float')

criteria = vehicles_non_hybrid.comb08.notnull()
vehicles_non_hybrid = vehicles_non_hybrid[criteria]
vehicles_non_hybrid.comb08 = vehicles_non_hybrid.comb08.astype('float')

print(ggplot(vehicles_non_hybrid, aes('displ', 'comb08')) +
      geom_point(color='steelblue') +
      xlab('Engine Displacement') +
      ylab('Average MPG') +
      ggtitle('Gasoline cars'))

#%% step 10
grouped_by_year = vehicles_non_hybrid.groupby(['year'])
avg_grouped_by_year = grouped_by_year['displ', 'comb08'].agg([np.mean])

#%% step 11
avg_grouped_by_year['year'] = avg_grouped_by_year.index
melted_avg_grouped_by_year = pd.melt(avg_grouped_by_year, id_vars='year')

from ggplot import facet_wrap
p = ggplot(aes(x='year', y='value', color='variable_0'), data=melted_avg_grouped_by_year)
p + geom_point() + facet_wrap('variable_0')


#%%  Section Investigating the makes and models of automobiles with Python
# ------ step 1, 2 ------------------
pd.unique(vehicles_non_hybrid.cylinders)
vehicles_non_hybrid.cylinders = vehicles_non_hybrid.cylinders.astype('float')
pd.unique(vehicles_non_hybrid.cylinders)
vehicles_non_hybrid_4 = vehicles_non_hybrid[(vehicles_non_hybrid.cylinders == 4.0)]

#%% step 3
import matplotlib.pyplot as plt
%matplotlib inline

grouped_by_year_4_cylinder = vehicles_non_hybrid_4.groupby(['year']).make.nunique()
fig = grouped_by_year_4_cylinder.plot()
fig.set_xlabel('Year')
fig.set_ylabel('Number of 4-Cylinder Makes')
print(fig)

#%% step 4
grouped_by_year_4_cylinder = vehicles_non_hybrid_4.groupby(['year'])
unique_makes = []
for name, group in grouped_by_year_4_cylinder:
    unique_makes.append(set(pd.unique(group['make'])))
unique_makes = reduce(set.intersection, unique_makes)
print(unique_makes)

#%% step 5, 6, 7
boolean_mask = []
for index, row in vehicles_non_hybrid_4.iterrows():
    make = row['make']
    boolean_mask.append(make in unique_makes)
df_common_makes = vehicles_non_hybrid_4[boolean_mask]

df_common_makes_grouped = df_common_makes.groupby(['year', 'make']).agg(np.mean).reset_index()

from ggplot import geom_line
ggplot(aes(x='year', y='comb08'), data = df_common_makes_grouped) + geom_line() + facet_wrap('make')
