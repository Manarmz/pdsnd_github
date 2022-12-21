import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Let\'s start by filtering the data \n')
    print('*'*40)
    print('Choose one of below cities \nChicago | New York City | Washington\n')
    city = input('Type city name here: ').lower()
    while city not in CITY_DATA.keys():
        city = input ("Invalid input. \nPlease choose between chicago, new york city OR washington: ").lower()
    print('\nFetching data for {}...'.format(city.title()))
    print('-'*40)
    
    # get user input for month (all, january, february, ... , june)
    print('Choose one of below months or type \'all\' to skip filter\nJanuary | February | March | April | May | June\n')
    month = input('Type here: ').lower()
    while month not in ['all', 'january', 'february', 'march', 'april', 'may', 'june']:
        month = input ("Invalid input. \nPlease choose between January to june or type all: ").lower()
    print('\nFetching data in {}...'.format(month.title()))
    print('-'*40)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('Choose one of below days or type \'all\' to skip filter\nSunday | Monday | Tuesday | Wednesday | Thursday | Friday | Saturday\n')
    day = input('Type here: ').lower()
    while day not in ['all', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']:
        day = input ("Invalid input. \nPlease choose any day in the week or type all: ").lower()
    print('\nFetching data for {}...'.format(day.title()))
    
    print('-'*40)
    return city, month, day

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    # Q1 popular times of travel
    print('\n#1 Popular times of travel:\n')
    start_time = time.time()

    # Q1.1 the most common month
    common_month = df['month'].mode()[0]

    print('most common month:', common_month)

    # Q1.2 most common day of week
    common_day_of_week = df['day_of_week'].mode()[0]

    print('most common day of week:', common_day_of_week)

    # Q1.3 most common hour of day
    common_hour_of_day = df['hour'].mode()[0]

    print('most common hour of day:', common_hour_of_day)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    # Q2 Popular stations and trip
    print('\n#2 Popular stations and trip:\n')
    start_time = time.time()

    # Q2.1 most common start station
    common_start_station = df['Start Station'].mode()[0]

    print('most common start station:', common_start_station)

    # Q2.2 most common end station
    common_end_station = df['End Station'].mode()[0]

    print('most common end station:', common_end_station)

    # Q2.3 most common trip from start to end (i.e., most frequent combination of start station and end station)
    combined=df.groupby(['Start Station','End Station'])
    common_combination_station = combined.size().sort_values(ascending = False).head(1)
    print('most common trip from start to end:\n', common_combination_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    # Q3 Trip duration
    print('\nTrip duration:\n')
    start_time = time.time()

    # Q3.1 total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('total travel time:', total_travel_time)

    # Q3.2 average travel time
    average_travel_time = df['Trip Duration'].mean()

    print('average travel time:', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""
    # Q4 User info
    print('\nUser Stats:\n')
    start_time = time.time()

    # Q4.1 counts of each user type
    print('counts of each user type:')
    print(df['User Type'].value_counts())
    if city != 'washington':
        # Q4.2 counts of each gender (only available for NYC and Chicago)
        print('counts of each gender:')
        print(df['Gender'].value_counts())
        # Q4.3 earliest, most recent, most common year of birth (only available for NYC and Chicago)
        print('Birth Year Stats:')
        most_common_year = df['Birth Year'].mode()[0]
        print('most common year:',most_common_year)
        most_recent_year = df['Birth Year'].max()
        print('most recent year:',most_recent_year)
        earliest_year = df['Birth Year'].min()
        print('earliest year:',earliest_year)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_row_data(df):
    row = 0
    while True:
        raw_data = input("would you like see the raw data? Enter yes or no.\n").lower() 
        if raw_data == "yes":
            print( df.iloc[ row : row + 6] )
            row += 6
        elif raw_data == "no":
            break
        else:
            print("Invalid input. Please enter yes or no.")
   
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        show_row_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print('Thank you for using US Bikeshare Data Exploration Program.. See you later!')
            break


if __name__ == "__main__":
	main()