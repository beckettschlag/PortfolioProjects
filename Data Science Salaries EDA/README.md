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
-This data includes data science salary information from 2019-2022.
-Experience level is categorized into four values:
  -EN - 'Entry-Level'
  -MI - 'Mid-Level'
  -SE - 'Senior-Level'
  -EX - Executive Level
-There are many unique job titles within the dataset.
-People working in data science live all over the world.
-This data categorizes remote percentage as In-Person, Hybrid, or Onsite with the corresponding values of 0, 50, or 100 respectively.
-Companies employing data scientists are located all over the world.
-A variety of small, medium, and large businesses are employing data scientists.
