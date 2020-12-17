import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv("adult.data.csv")

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()
    # What is the average age of men?
    average_age_men = round(df[(df['sex'] == 'Male')]['age'].mean(), ndigits = 1)

    # What is the percentage of people who have a Bachelor's degree?
    total_education_count = df['education'].count()
    bachelors_count =df[df['education'] == 'Bachelors']['education'].count()
    
    percentage_bachelors = round((bachelors_count / total_education_count) * 100, ndigits = 1)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?


    # with and without `Bachelors`, `Masters`, or `Doctorate`

    # percentage with salary >50K
    
    higher_education_rich = round((len(df[(df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])) & (df['salary'] == '>50K')]) / len(df[df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])]) ) * 100, ndigits = 1)

    lower_education_rich = round((len(df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate']) & (df['salary'] == '>50K')]) / len(df[~df['education'].isin(['Bachelors', 'Masters', 'Doctorate'])])) * 100, ndigits = 1 )

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    rich_percentage = round((len(df[(df['hours-per-week'] == df['hours-per-week'].min()) & (df['salary'] == '>50K')]) / len(df[df['hours-per-week'] == df['hours-per-week'].min()])) * 100)

    # What country has the highest percentage of people that earn >50K?
    
    # Defining the new columns in a new grouped table
    aggregation = {
        '>50K':  ('salary', lambda x: (x == ">50K").sum()),
        '<=50K': ('salary', lambda x: (x == "<=50K").sum()),
    }

    # Creating a new table that has native-country as the index and columns that have the counts of >50K and <=50K
    df2 = df.groupby('native-country').agg(**aggregation)

    # Function that gets the total per country
    def getTotal(row):
            return row['>50K'] + row['<=50K']

    # Add a column that calculate the % of those that earn >50K
    df2['>50K%'] = df2.apply(lambda row: (row['>50K'] / getTotal(row) *100).round(1), axis=1)

    # Sorting the values by >50K% - largest number at the top
    df2 = df2.sort_values(">50K%",ascending=False)

    # Get the name of the country and put into Title Case
    highest_earning_country = df2.iloc[0].name.title()

    # Get the percentage
    highest_earning_country_percentage = df2.iloc[0][">50K%"]

    # Identify the most popular occupation for those who earn >50K in India.
    top_IN_occupation = df[(df['salary'] == '>50K') & (df['native-country'] == 'India')].occupation.value_counts().index[0]

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
