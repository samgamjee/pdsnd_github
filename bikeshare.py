import time
import datetime
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}


valid_city = CITY_DATA.keys()
valid_month = ['all','january','february','march','april','may','june','july','august','september','october','november','december']
valid_day = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
    print('Hello!Let\'s explore some US bikeshare data!')

    while True:
        city = str(input("We have some cool stats for Chicago, New York City and Washington cities. Pick up the city you're interested in:\n").lower())
        if city not in valid_city:
            print("Oops,please review your answer. Make sure you typed one of the cities listed.\n")
            continue
        else:
            month = str(input("Would you like to see data for a specific month? If yes,type the month name (ie.january).You can also type 'all' and no month filter will apply:\n").lower())
        while True:
            if month not in valid_month:
                print("Oops,please review your answer. Eiter type a specific month name(ie.march) or 'all' if no month filter applies.\n")
                month = str(input("Would you like to see data for a specific month? If yes,type the month name (ie.january).If no month filter applies, type 'all':\n").lower())
                continue
            else:
                day = str(input("Finally,would you like to see data for a specific day? If yes, type the day name (ie.monday). You can also type 'all' and no day filter will apply\n").lower())

            while True:
                if day not in valid_day:
                    print("Oops,please review your answer. Eiter type a specific day name(ie.monday) or 'all' if no day filter applies.")
                    day = str(input("Finally,would you like to see data for a specific day? If yes, type the day name (ie.monday). You can also type 'all' and no day filter will apply\n").lower())
                    continue
                else:
                    print("\n***** We are all set!******\nLet'see what we've got for city:{}, month:{} and day:{}".format(city,month,day))
                    break
            break
        break
    print('-'*40)
    return city, month, day



def load_data(city,month,day):
    filename = ('{}.csv'.format(city).replace(" ","_"))
    df = pd.read_csv(filename)  # read csv already filtered for city
    #print(df.head()) # simple check that df returns data

# convert start time to date time
    df['Start Time'] = pd.to_datetime(df['Start Time'])

# extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour_of_day'] = df['Start Time'].dt.hour

# handle month and day filters
    if month != "all":
        months = valid_month
        month = months.index(month)
        df = df[(df['month'] == month)]
    if day != "all":
        df = df[(df['day_of_week'] == day.title())]

    return df


#df = load_data(city,month,day) -- check df returns data

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

        # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    popular_month_name = valid_month[popular_month]
    print("The most common month in dataset is {}".format(popular_month_name))


        # TO DO: display the most common day of week
    popular_day_name = df['day_of_week'].mode()[0]
    print("The most common day in dataset is {}".format(popular_day_name))


        # TO DO: display the most common start hour
    popular_start_hour = df['hour_of_day'].mode()[0]
    print("The most common trip starting hour is {}".format(popular_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("The most popular station in dataset to start a trip is {}".format(popular_start_station))

    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("The most popular station in dataset to terminate a trip is {}".format(popular_end_station))


    # TO DO: display most frequent combination of start station and end station trip
    popular_combo_start_end_station = (df['Start Station'] + '/' + df['End Station']).mode()[0]
    print("The most common combo start & end station is {}".format(popular_combo_start_end_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

        # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time_formatted = pd.to_timedelta(total_travel_time,unit='s')
    print("The total travel time is {}".format(total_travel_time_formatted))

    avg_travel_time = df['Trip Duration'].mean()
    avg_travel_time_formatted = pd.to_timedelta(avg_travel_time,unit='s')
    print("The average travel time is {}".format(avg_travel_time_formatted))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    print('\nCalculating User Stats by user type...\n')
    user_type_values = df['User Type'].fillna('not provided user type').value_counts().keys().tolist()
    user_type_counts = df['User Type'].fillna('not provided user type').value_counts().tolist()
    value_dict = dict(zip(user_type_values, user_type_counts))

    for key in value_dict.items():
        print('For', key[0], 'we count', key[1],'users')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

        # TO DO: Display counts of gender
    print('\nCalculating User Stats by user gender...\n')

    if 'Gender' in df.columns:
        gender_values = df['Gender'].fillna('not provided gender').value_counts().keys().tolist()
        gender_type_counts = df['Gender'].fillna('not provided gender').value_counts().tolist()
        gender_value_dict = dict(zip(gender_values, gender_type_counts))

        for key in gender_value_dict.items():
            print('For', key[0], 'we count', key[1],'users')
    else:
        print("Unfortunately,no Gender information is provided for this city")   

    if 'Birth Year' in df.columns:
        most_old_year_birth = df['Birth Year'].min()
        most_recent_year_birth = df['Birth Year'].max()
        most_common_year_birth = df['Birth Year'].mode()[0]

        print('\nThe earliest year of birth in dataset is:{}'
                '\nThe most recent year of birth in dataset is:{}'
                '\nThe most common year of birth in dataset is:{}'
                .format(int(most_old_year_birth),
                int(most_recent_year_birth),
                int(most_common_year_birth)))
    else:
        print('Unfortunately,no Birth year information is provided for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_raw(df):
    while True:
        preview_display = input ('Would you like to see a preview? either type "yes" or "no"\n')
        preview_lines = 5
        if preview_display.lower() == 'no':
            print('Ok, got it, let\'s stop here...')
            break
        if preview_display.lower() == 'yes':
            print(df.head(preview_lines))
            preview_lines += 5
            see_more = input('Wanna see more?\n')
        else:
            print('Oops,seems there is a glitch in your answer.Please make sure to enter yes/no\n')
        
        while True:
            if see_more.lower() =='no':
                print('Ok, got it, let\'s stop here...')
                return False
            else:
                print(df.head(preview_lines))
                preview_lines += 5
                see_more = input('Wanna see more?\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        display_raw(df)
        restart = input('\nWould you like to reset and see stats for another city? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()






















