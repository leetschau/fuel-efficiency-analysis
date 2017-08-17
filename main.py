#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 12:13:11 2017

@author: leo
"""
#%%
import pandas as pd
import numpy as np
#from ggplot import *
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

print(ggplot(averaged,
             aes('year', 'comb08_mean'))
                 + geom_point(color='steelblue')
                 + xlab('Year') + ylab('Average MPG') + ggtitle('All cars'))

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
