import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'new york': 'new_york_city.csv',
              'washington dc': 'washington.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hey, great to see you! Let's solve some US bikeshare data misteries together! We'll have so much fun xD")

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    cities = ('chicago', 'new york city', 'new york', 'washington', 'washington dc')
    while True:
        city = input('\nWould you like to see data for Chicago, New York City, or Washington?\n').lower()
        if city not in cities:
            print('\nPlease try again. Choose Chicago, New York City or Washington\n')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    
    months = ('january', 'february', 'march', 'april', 'may', 'june', 'all')
    while True:
        month = input('\nPlease type name of month you would like to filter data by. You can choose from: January, Febrary, March, April, May or June. If you do not wish to filter data in this way please enter "all".\n').lower()
        if month not in months:
            print('\nPlease try again. Choose January, Febrary, March, April, May, June or all\n')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)

    days = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all')
    while True:
        day = input('\nPlease type name of day of the week you would like to filter data by. You can choose from: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday. If you do not wish to filter data in this way please enter "all".\n').lower()
        if day not in days:
            print('\nPlease try again. Choose Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all\n')
            continue
        else:
            break

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
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

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

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    common_month = df['month'].mode()[0]
    print('Most common month is: {}'.format(common_month))

    # display the most common day of week

    common_day = df['day_of_week'].mode()[0]
    print('Most common day of the week is: {}'.format(common_day))

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print('Most common starting hour is: {}'.format(common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    common_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station is: {}'.format(common_start_station))

    # display most commonly used end station

    common_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station is: {}'.format(common_end_station))

    # display most frequent combination of start station and end station trip

    df['Most Frequent Trip'] = df['Start Station'] + ' to ' + df['End Station']
    most_common_trip = df['Most Frequent Trip'].mode()[0]
    print('Most common trip is: {}'.format(most_common_trip))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time

    total_travel_time = df['Trip Duration'].sum()

    total_travel_time_s = int(total_travel_time%60)
    total_travel_time_m = int(total_travel_time//60%60)
    total_travel_time_h = int(total_travel_time//3600%60)
    total_travel_time_d = int(total_travel_time//24//3600)
    
    print('Total travel time: {} days, {} hours, {} minutes {} seconds'.format(total_travel_time_d, total_travel_time_h, total_travel_time_m, total_travel_time_s))

    # display mean travel time

    mean_travel_time = df['Trip Duration'].mean()

    mean_travel_time_s = int(mean_travel_time%60)
    mean_travel_time_m = int(mean_travel_time//60%60)
    mean_travel_time_h = int(mean_travel_time//3600%60)

    print('Average travel time: {} hours, {} minutes {} seconds'.format(mean_travel_time_h, mean_travel_time_m, mean_travel_time_s))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_type_count = df['User Type'].value_counts()
    print('\nNumber of users based on their account type:\n', user_type_count)

    # Display counts of gender

    try:
        gender_count = df['Gender'].value_counts()
        print('\nNumber of male and female users:\n', gender_count)
    except KeyError:
        print('\nNumber of male and female users: Data not available.')


    # Display earliest, most recent, and most common year of birth

    try:
        yob_min = int(df['Birth Year'].min())
        print('\nEarliest year of birth: {}'.format(yob_min))
    except KeyError:
        print('\nEarliest year of birth: Data not available.')

    try:
        yob_max = int(df['Birth Year'].max())
        print('Most recent year of birth: {}'.format(yob_max))
    except KeyError:
        print('Most recent year of birth: Data not available.')

    try:
        birth_mode = int(df['Birth Year'].mode()[0])
        print('Most common year of birth: {}'.format(birth_mode))
    except KeyError:
        print('Most common year of birth: Data not available.')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_raw_data(df):
    user_decision = input('\nWould you like to view the first 5 lines of raw data? yes or no:\n').lower()
    if user_decision != 'no' and user_decision != 'n' and user_decision != 'yes' and user_decision != 'y':
        print('\nPlease try again\n')
        display_raw_data(df)
    elif user_decision == 'yes' or user_decision == 'y':
        i = 0
        while i < df['Start Time'].count():
            print(df.iloc[i:i+5])
            i += 5
            another_five = input('\nWould you like to view another 5 lines of raw data? yes or no:\n').lower()
            if another_five != 'yes' and another_five != 'y':
                break
                
                
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()