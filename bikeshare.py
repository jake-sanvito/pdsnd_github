import time
import pandas as pd
import numpy as np
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify either chicago, new york city and washington, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!\n')
    print('The data covers 6 months and three cities. You can only chose one city at a time:')
    print('Chicago, New York City or Washington DC. \n')
    print('If you wish to filter by a month and/or a day, enter the month and/or day when promted. ')
    print('Otherwise, just enter \'all\'.\n')

    city, month, day = "blank","blank","blank"
    month_list=['All','Jan','Feb','Mar', 'Apr','May','Jun']
    day_list = ['All','Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

    # get user input for city (chicago, new york city, washington). 
   
    while city.casefold() not in CITY_DATA:
        answer_city = input("Enter one of the following citiy names: Chicago, New York City or Washington : ")
        if answer_city.casefold() in CITY_DATA:
           city=answer_city.lower()
           break
        else:
            print('Please try again. There seems to have been a problem with your answer.')


    while month.casefold() not in (name.casefold() for name in month_list):
        answer_month = input(("Please enter a three letter abreviation for the month or All : "," ".join(month_list)," : "))
        if answer_month.casefold()  in (name.casefold() for name in month_list):  
            month=answer_month.lower()
            break     
        else:
            print('Please try again. There seems to have been a problem with your answer.')


    while day.casefold() not in (name.casefold() for name in day_list):
        answer_day = input(("Please enter a three letter abreviation for the day or All : "," ".join(day_list)," : "))
        
        if answer_day.casefold()  in (name.casefold() for name in day_list):
            day=answer_day.lower()
            break
        else:
            print ("Sorry, the answer has to be one of the following"," ".join(day_list))
    



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
    
    # Used to change input abbreviation to full name as used in dataframe.
    days_dict = {"all":"all",
            "sun": "Sunday", 
            "mon": "Monday", 
            "tue": "Tuesday", 
            "wed": "Wednesday", 
            "thu": "Thursday", 
            "fri": "Friday", 
            "sat": "Saturday", 
            "sun": "Sunday"}
    day=days_dict[day].lower()

    
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])


    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
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
    print("most_popular month" , df['month'].mode()[0])

    # display the most common day of week
    print("most_popular day" , df['day_of_week'].mode()[0])

    # display the most common start hour
    print("most_popular hour" , df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("most_popular start station" , df['Start Station'].mode()[0])


    # display most commonly used end station
    print("most_popular start station" , df['End Station'].mode()[0])


    # display most frequent combination of start station and end station trip
    print("Most common Start and End station and count of trips")
    trip_count=df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    print(trip_count.head(1))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    total=np.round(total,0)
    print("Total Trip Duration : ", total)


    # display mean travel time
    mean = df['Trip Duration'].mean()
    mean=np.round(mean,0)
    print("THe mean trip time is : ", mean)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    # Display counts of user types
    print(df['User Type'].value_counts())


    # Display counts of gender
    if city == "new york city".casefold() or city == "chicago".casefold():
        print("Gender Stats:", df['Gender'].value_counts())


    # Display earliest, most recent, and most common year of birth
    if city == "new york city".casefold() or city == "chicago".casefold():
        min, max, mode = df['Birth Year'].min(), df['Birth Year'].max(), df['Birth Year'].mode()[0]
        print("The min, max and mode are : ",min, max, mode)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)






def main():
    while True:

        city, month, day = get_filters()
        if city=='blank' or month=='blank' or day=='blank':
            break
        df=load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        scroll=""
        while scroll != "y" and scroll != "n":
            scroll=input("Would you like to scroll through the raw data? (y/n)?")
            print(scroll)
        if scroll == "y":
            x=1
            while scroll != "n":
                print(df.iloc[x:x+5,:])
                x+=5
                scroll=input("Would you like to see more data? (y/n)")        


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
