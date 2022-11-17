# Data Science Salary Exploratory Data Analysis

Data from: [https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries](https://www.kaggle.com/datasets/ruchi798/data-science-job-salaries)

## Context
Data Science is the practice of using data to extract meaningful insights. It is a multidisciplinary field that combines the skills of mathematics, statistics and computer engineering among many others to achieve an organization's goals. This analysis is key in helping an organization answer questions and gain knowledge about this business practicies and how they can achieve their objective.

## Questions seeking answers:
- What countries have the most remote workers?
- Are people who work remotely paid more?
- How have remote percentages changed?
- Have salary levels changed as the remote percentage has?
- Is there a relationship between job type and experience level?
- Do company sizes correlate with job type and salary?

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
- This data includes data science salary information from 2019-2022.
- Experience level is categorized into four values:
  - EN - 'Entry-Level'
  - MI - 'Mid-Level'
  - SE - 'Senior-Level'
  - EX - Executive Level
- There are many unique job titles within the dataset.
- People working in data science live all over the world.
- This data categorizes remote percentage as In-Person, Hybrid, or Onsite with the corresponding values of 0, 50, or 100 respectively.
- Companies employing data scientists are located all over the world.
- A variety of small, medium, and large businesses are employing data scientists.

We also learn that there are a number of columns that will not be useful to our exploration and there are repeated rows. There's also multiple values that could be more meaningful for our exploration. Let's remove the unused columns/rows, remove rows with duplicated data, and rename the values to be more meaningful.
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

First, let's create a graph that visualizes the top 15 countries with the most remote workers.
```
sns.set_palette('autumn')
sns.set_style('whitegrid')

top_remote_locations = df.groupby('company_location')['remote_percentage'].mean().sort_values(ascending=False)[:20]

plt.figure(figsize=(15, 6))

ax = sns.barplot(y=top_remote_locations.index, x=top_remote_locations, palette='autumn')
ax.set_title('Countries With Most Remote Workers', fontdict={'fontsize': 14})
plt.show()
```
