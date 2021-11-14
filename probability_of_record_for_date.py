# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 12:15:06 2021
"""
import pandas as pd

#%%
data = pd.read_csv("torquatus.csv", sep=",", encoding=('UTF-8'))

#%%e
data['Day'] = data['start_date'].str.slice(8) 
data['start_date'] = pd.to_datetime(data['start_date'])

#%%%
'''
Calculate how many observations of birds in the span (2000 - 2020) on a specific date.
 
'''
period_start_year, period_end_year = int(2000),int(2020) #Or min/max of data[start_date] year
search_date = "2022-10-25"
search_mon_day = search_date[4:] #the date
dates = []
year = period_start_year

# List all possible dates between start_year and end_year (incl. end year)
while year < period_end_year+1:
    dates.append(str(str(year)+search_mon_day))
    year = year + 1
    
obs_per_day_sum = data.groupby(data['start_date']).sum() # Total number of individuals per day
obs_per_day_count = data.groupby(data['start_date']).count() # Total number of observations per day

freq = pd.DataFrame(columns = ["date"],data = dates) #Create a data frame
freq.set_index('date', inplace = True)

#Join the sums and counts to the df of dates
freq= freq.join(obs_per_day_sum['observed_individuals'],lsuffix="_Sum") 
freq = freq.join(obs_per_day_count['observed_individuals'],lsuffix="_Count")

observed_individuals_on_day = freq['observed_individuals_Count'].count() #How many observations on the date during the years
pr_thrush = round(observed_individuals_on_day / len(freq) * 100,0) # Divide number of days with observations with the total number of days
print("There is a {}% chance that a ringed ouzel will be reported on the {} based on historical records for that day!".format(pr_thrush,search_date))