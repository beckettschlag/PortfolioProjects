# Data Science Salary Exploratory Data Analysis

Data from: [https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries)

## Context
Data Science is the practice of using data to extract meaningful insights. It is a multidisciplinary field that combines the skills of mathematics, statistics and computer engineering among many others to achieve an organization's goals. This analysis is key in helping an organization answer questions and gain knowledge about this business practicies and how they can achieve their objective.

**The intended audience for this project are people curious about the advantages of remote work in data science.**

## Questions seeking answers:
- Which countries have companies with the most remote workers?
- Does experience level correlate with remote percentage?
- Are people who work remotely paid more?
- Have salary levels changed as the remote percentage has?
- How do company sizes correlate with job type and salary?

## Loading the data and gaining insight about it's structure
```
import pandas as pd # data processing
import numpy as np # linear algebra
import matplotlib.pyplot as plt # data visualization
import matplotlib.gridspec # data visualization
import seaborn as sns # data visualization
import country_converter as cc # Used to convert country abbreviations


# Getting the dataset
df = pd.read_csv(r'C:\Users\becke\Desktop\DA Projects\Data Science Project\ds_salaries.csv')
print(df.head())


# Understanding the columns and data types
print(df.dtypes)
print('Column Names:',df.columns)

print('Unique values from work_year: \n', df.work_year.unique())
print('Unique vales from experience_level: \n' , df.experience_level.unique())
print('Unique values from job_title: \n', df.job_title.unique())
print('Unique values from employee_residence: \n', df.employee_residence.unique())
print('Unique values from remote_ratio: \n', df.remote_ratio.unique())
print('Unique values from company_location: \n', df.company_location.unique())
print('Unique values from company_size: \n', df.company_size.unique())
```

From this, we learn a number of things: 
- This data includes data science salary information from 2020-2022.
- Experience level is categorized into four values:
  - EN - 'Entry-Level'
  - MI - 'Mid-Level'
  - SE - 'Senior-Level'
  - EX - Executive Level
- There are 50 unique job titles within the dataset.
- People working in data science live in 57 unique countries.
- This data categorizes remote percentage as In-Person, Hybrid, or Onsite with the corresponding values of 0, 50, or 100 respectively.
- Companies employing data scientists are located in 50 unique countries.
- Company sizes are broken down into three categories: small, medium, and large.

We also learn that there are a number of columns that will not be useful to our exploration and there are repeated rows. There's also multiple values that could be more meaningful for our exploration. Let's remove the unused columns, remove rows with duplicated data, and rename the values to be more meaningful.
```
# Removing the redundant 'Unnamed: 0' column
df.drop('Unnamed: 0', axis=1, inplace=True)
#print(df.head())


# Removing salary and salary_currency column and renaming salary_in_usd to salary
df.drop(['salary', 'salary_currency'], axis=1, inplace=True)
df.rename(columns={'salary_in_usd': 'salary'}, inplace=True)


# Removing duplicate rows of data (42 rows)
#print(df.duplicated().sum())
df.drop_duplicates(inplace=True)

# Changing country names in country_location and employee_residence from abbreviations to full country names
coco = cc.CountryConverter()
df['employee_residence'] = coco.convert(df['employee_residence'], to='name_short')
df['company_location'] = coco.convert(df['company_location'], to='name_short')
#print(df.head())

# Changing company_size from abbreviated to extended values
#print(df['company_size'].value_counts())
df['company_size'] = df['company_size'].map({
    'S': 'Small',
    'M': 'Medium',
    'L': 'Large'

})
#print(df.head())


# Changing experience_level from abbreviated to extended values
#print(df['experience_level'].value_counts())
df['experience_level'] = df['experience_level'].map({
    'EN': 'Entry-Level',
    'MI': 'Mid-Level',
    'SE': 'Senior-Level',
    'EX': 'Executive-Level'

})


# Changing employment_type from abbreviated to extended values
#print(df['employment_type'].value_counts())
df['employment_type'] = df['employment_type'].map({
    'FL': 'Freelance',
    'CT': 'Contract',
    'PT': 'Part-Time',
    'FT': 'Full-Time'

})


# Changing remote ratio to remote percentage
df.rename(columns={'remote_ratio': 'remote_percentage'}, inplace=True)
```

Now that we have ensured our data is clean and meaninful, we can begin our exploration.

## Exploring the data

First, let's create a graph that visualizes the top 20 countries with the most remote workers.
```
sns.set_palette('autumn')
sns.set_style('whitegrid')

top_remote_locations = df.groupby('company_location')['remote_percentage'].mean().sort_values(ascending=False)[:20]

plt.figure(figsize=(15, 6))

ax = sns.barplot(y=top_remote_locations.index, x=top_remote_locations, palette='autumn')
ax.set_title('Countries With Most Remote Workers', fontdict={'fontsize': 14})
plt.show()
```
![Alt text](https://i.imgur.com/fHbkcRH.png)

We discover that there are 12 countries where 100% of data scientists work remote. The next 5 countries with the highest percentage of remote workers lay somewhere between 80% and 100% with the last 3 operating between 60%-80%. To find specifically what their remote percentage is lets run the following.
```
print(top_remote_locations[12:20])
```
| Country  | Remote Percentage |
| ------------- | ------------- |
| Spain  | 92.86  |
| Netherlands  | 87.50  |
| Greece  | 85.00  |
| Luxembourg  | 83.33  |
| Australia  | 83.33  |
| United States  | 76.73  |
| Slovenia  | 75.00  |
| Czech Republic  | 75.00  |

Now that we know the countries with the highest remote percentage lets explore the question, 'Does experience level correlate with remote percentage?' We can use our data in a visualization to help us answer this.
```
# Finding the correlation between remote_percentage and experience_level

exp_lvl_gb = df.groupby('experience_level')['remote_percentage'].mean().sort_values()

ax = sns.barplot(x=exp_lvl_gb.index, y=exp_lvl_gb, order=['Entry-Level', 'Mid-Level', 'Senior-Level', 'Executive-Level'], data=df)
ax.set_title('Experience Level Vs Mean Remote Percentage', fontdict={'fontsize': 14})
plt.show()
```
![Alt text](https://i.imgur.com/eldvxTU.png)


From this we can clearly see that all experience levels have a remote percentage of at least 60%. An interesting insight is that Mid-Level employees have the lowest remote percentage at 64.18%  while Executive-Level employees have the highest, at 78.85%.

| Experience Level  | Remote Percentage |
| ------------- | ------------- |
| Entry-Level  | 69.89  |
| Mid-Level  | 64.18  |
| Senior Level  | 73.87  |
| Executive-Level  | 78.85  |

Now let's visualize the data needed to answer the question of 'Have salary levels changed as the remote percentage has?'
```
# mean salary by year and job type
mean_s_work_year = df.groupby('work_year')['salary'].mean().sort_values()
fig, axes = plt.subplots(1,2)

ax = sns.barplot(x=mean_s_work_year.index, y=mean_s_work_year, data=df, ax=axes[0])
ax.set_title('Mean Salary VS Work Year', fontdict={'fontsize': 14})

mean_s_remote_percentage_year = df.groupby('work_year')['remote_percentage'].mean().sort_values()
ax = sns.barplot(x=mean_s_remote_percentage_year.index, y=mean_s_remote_percentage_year, data=df, ax=axes[1])
ax.set_title('Mean Remote Percentage by Work Year', fontdict={'fontsize': 14})
plt.show()
```
![Alt text](https://i.imgur.com/roilmvc.png)

From the graphs we can see that from 2020-2022 both average remote percentage and mean salary have both increased. In the first graph we can see that in 2022 there was a significant increase in the average salary while remote percentage has increased by smaller margins. But, there is a clear upward trend for both margins.

Which job types have the highest average salary and what is the distribution like?
```
# finding salary distribution by job_type and mean salary distribution by job_type
df['remote_percentage'] = df['remote_percentage'].map({
    100: 'Remote',
    50: 'Hybrid',
    0: 'In-Person'

})

df.rename(columns={'remote_percentage': 'job_type'}, inplace=True)
mean_s_job_type = df.groupby('job_type')['salary'].mean().sort_values()

fig, axes = plt.subplots(1,2)

ax = sns.barplot(x=mean_s_job_type.index, y=mean_s_job_type, order=['In-Person', 'Hybrid', 'Remote'], ax=axes[0])
ax.set_title('Mean Salary VS Job Type', fontdict={'fontsize': 14})

ax = sns.violinplot(x='job_type', y='salary', data=df, order=['In-Person', 'Hybrid', 'Remote'], ax=axes[1])
ax.set_title('Salary VS Job Type', fontdict={'fontsize': 14})
plt.show()
```
![Alt text](https://i.imgur.com/hh2t1bL.png)

It seems that hybrid workers have the lowest mean salary of $80,721.90. Meanwhile, remote works recieve the highest salary of $120,763.19. In the second graph we can see the distribution of salary by job type. Each job type seems to have an outlier that is much higher than the average with the highest value being a remote worker earning over $600,000.


| Job Type  | Salary |
| ------------- | ------------- |
| In-Person  | $105,785.90  |
| Hybrid  | $80,721.90  |
| Remote  | $120,763.19  |

Lets explore these values ploted while also including company size.
```
# comparing job_type and company_size to their salaries
plt.figure(figsize=(15, 6))
sns.set_palette('autumn')
ax = sns.boxenplot(data=df, x='job_type', y='salary', order=['In-Person', 'Hybrid', 'Remote'], hue='company_size')
ax.set_title('Job Type & Company Size VS Salary', fontdict={'fontsize': 14})
plt.show()
```
![Alt text](https://i.imgur.com/Y6DVUFB.png)

This visualization allows us to understand the outliers for each job type while also giving us insight into what size company they work for. We can see that remote workers seem to get the highest salaries while working for large companies. Meanwhile, hybrid workers get relatively low salaries with less variation. We can also easily spot the outliers within the data for each job type, and identify what size company they work for.

## Conclusion
Through our exploration we were able to get answers to all of our questions by visualizing our data with Python. We found that there are 12 countries with 100% remote workers and the following 8 are between 60-80%. Then, we were able to find that all experience levels except mid-level employees have a 70% remote percentage with executive-level employees nearing 80%. We also found that both average salaries and average remote percentages have increased significantly since 2020. Noteably, in 2022 average salaries have risen over $20,000. When investigated further we found that remote workers make the highest slary on average reaching $120,000 while hybrid workers earn the least on average at $80,000. We can also see the districution of these values for each job type and note some outliers. Finally, we learn that Remote workers have the largest variation in their salaries while hybrid workers have the least variation reguardless of their company size.

Overall we can see that jobs within data science have a growing overage salary that allows their employees to work from home at an increasing rate. Those that work at the executive-level can expect to have the highest probablity of securing a job where they can work at home. Remote workers can expect to earn the highest salary despite their company size while hybrid workers can expect to make the least by a margin of over $20,000. **Therefore, we can determine that remote work has the best opportunities for an increased salary in multiple countries and company sizes.**
