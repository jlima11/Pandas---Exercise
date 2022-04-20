import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv', delimiter=',')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count_ascesnding =   df.groupby(['race']).size().to_frame().reset_index().rename(columns={0:'QT'})
    race_count_dfr = race_count_ascesnding.sort_values('QT',ascending=False)
    race_count = race_count_dfr.QT

    # What is the average age of men?
    average_age_men_list = df.loc[df.sex=='Male',['age']].mean()
    average_age_men = round(average_age_men_list.age,1)

    # What is the percentage of people who have a Bachelor's degree?
    bachelors = df.loc[df.education=='Bachelors',['education']].count()
    percentage_bachelors = round((bachelors/df.shape[0])*100,1).education

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = bachelors = df[df.education.isin(['Bachelors','Masters','Doctorate'])].count()[0]
    lower_education = df.shape[0] - higher_education

    # percentage with salary >50K
    higher_education_rich_num = df[(df.education.isin(['Bachelors','Masters','Doctorate']))&(df.salary=='>50K')].count()[0]
    higher_education_rich = round((higher_education_rich_num/higher_education)*100,1)
    lower_education_rich_num = df[(~df.education.isin(['Bachelors','Masters','Doctorate']))&(df.salary=='>50K')].count()[0]
    lower_education_rich = round((lower_education_rich_num/lower_education)*100,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    df = df.rename(columns={'hours-per-week': 'hours'})
    num_min_workers = df[(df.hours==min_work_hours)].count()[0]

    rich_percentage_min_workers = df[((df.hours==min_work_hours)&(df.salary=='>50K'))].count()[0]
    rich_percentage = (rich_percentage_min_workers/num_min_workers)*100

    # What country has the highest percentage of people that earn >50K?
    df = df.rename(columns={'native-country':'country'})
    highest_earning_countrys = df[(df.salary=='>50K')].groupby(df.country).salary.count()
    highest_earning_countrys=highest_earning_countrys.to_frame().reset_index()
    countrys_num_people = df.groupby(df.country).salary.count().reset_index()
    country_anali = highest_earning_countrys.merge(countrys_num_people,how='left', on='country')
    country_anali =  country_anali.rename(columns={'salary_y':'total_salary'})
    country_anali['perc'] =  country_anali.salary_x/ country_anali.total_salary
    maximo_earn =  country_anali.perc.max()
    highest_earning_country =  country_anali[(country_anali.perc==maximo_earn)].country.values[0]
    highest_earning_country_percentage =  round(( country_anali.perc.max())*100,1)

    # Identify the most popular occupation for those who earn >50K in India.
    filtro_india = df[(df.salary=='>50K')&(df.country=='India')].groupby(df.occupation).salary.count()
    top_IN = filtro_india.to_frame().reset_index()
    top_IN_ordenado = top_IN.sort_values('salary',ascending=False)
    top_IN_occupation = top_IN_ordenado.iloc[0].occupation

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
