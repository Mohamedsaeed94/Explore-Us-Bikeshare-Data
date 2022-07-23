#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time
import pandas as pd
import numpy as np


# In[2]:


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


# In[3]:


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    while True:
        city = input('enter city name [chicago - new york city - washington]: ').lower()
        month = input('enter [all] for all months or choose specific month from [jan - feb - mar - apr - may - jun]: ').lower()
        day = input('enter [all] for all days or choose specific day number from [1 to 31]: ')
        
        if month not in ['all', 'jan', 'mar', 'may'] and day == '31':
            print('Month have only 30 days, Renter right value.')
            continue
        if month == 'feb' and day > '28':
            print('febraury have only 28 days, renter right value.')
            continue
        if city in CITY_DATA.keys() and month in ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'all'] and (day == 'all' or day in list(map(str,range(1,32)))):
        
            break
        else:
            print('Please Checkback Entered Values')


    print('-'*40)
    return city, month, day


# In[4]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'], dayfirst = True)
    df['month'] = df['Start Time'].dt.month
    df['day_num'] = df['Start Time'].dt.day
    df['day'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.strftime("%I %p")
    
    targeted_months = [1, 2, 3, 4, 5, 6]
    df.query('month == @targeted_months', inplace = True)
    month_dic = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6}
    
      #first condition:
    if month == 'all' and day == 'all':
        df = df
    #second condition:    
    elif month != 'all' and day == 'all':
        month_in = month_dic.get(month) 
        df.query('month == @month_in', inplace = True)
        
    #third condition:
    elif month == 'all' and day != 'all':
        day_in = int(day)
        df.query('day_num == @day_in', inplace = True)
        
    #fourth condition:
    elif month != 'all' and day != 'all':
        month_in = month_dic.get(month)
        day_in = int(day)
        df.query('month == @month_in', inplace = True)
        df.query('day_num == @day_in', inplace = True)
        
    return df


# In[5]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    month_dic = {'jan':1, 'feb':2, 'mar':3, 'apr':4, 'may':5, 'jun':6}
    
    month = df['month'].mode()[0]
    month_count = df['month'].value_counts().loc[month] 
    day = df['day'].mode()[0]
    day_count = df['day'].value_counts().loc[day]
    hour = df['hour'].mode()[0]
    hour_count = df['hour'].value_counts().loc[hour]
    for m,n in month_dic.items():
        if month == n:
            month = m  
            
    print('*Popular time of travels:\n Most common month is {} with count {}.\n Most common day is {} with count {}.\n Most common hour is {} with count {}.'.format(month, month_count, day,day_count, hour, hour_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[6]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    start = df['Start Station'].mode()[0]
    start_count = df['Start Station'].value_counts().loc[start]
    end = df['End Station'].mode()[0]
    end_count = df['End Station'].value_counts().loc[end]
    df['combination'] = df['Start Station'] + ', ' + df['End Station']
    combination = df['combination'].mode()[0]
    combination_count = df['combination'].value_counts().loc[combination]
    print('*Popular stations and trips for data provided:\n Most common start station is {} with count {}.\n Most common end station is {} with count {}.'
          '\n Most common trip is {} with count {}.'.format(start, start_count, end, end_count, combination, combination_count))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    


# In[7]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    total = df['Trip Duration'].sum() / 60
    average = df['Trip Duration'].mean() / 60
    count = df['Trip Duration'].count()
    print('*Trip duration statistics for {} rides provided:\n Total travel time is {} minutes.\n Average travel time is {} minutes.'.format(count, round(total,2), round(average,3)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[8]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    user_type = df['User Type'].value_counts().iloc[:2].to_string()
    if 'Gender' and 'Birth Year' in df.columns:
        df.dropna()
        gender = df['Gender'].value_counts().iloc[:2].to_string()
        earliest = int(df['Birth Year'].min())
        recent = int(df['Birth Year'].max())
        common = int(df['Birth Year'].mode()[0])
    else:
        gender = earliest = recent = common = '[NO available information]'
        
    print('*User info statistics: \n Count of each user type:\n {} \n Count of each gender:\n {} \n Earliest year of birth is {}.\n Most recent year of birth is {}.\n '
    'Most common year of birth is {}.'.format(user_type, gender, earliest, recent, common))
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[9]:


def display_data(df):
    """Display 5 raws of rows of raw Data"""
    
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
    start_loc = 0
    while view_data.lower() == 'yes':
        print(df.iloc[start_loc : start_loc+5])
        start_loc += 5
        print('-'*40)
        view_data = input("Do you wish to continue?: ").lower()


# In[10]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


# In[11]:


if __name__ == "__main__":
    main()


# In[ ]:




