import pandas as pd # data processing
import numpy as np # linear algebra
import matplotlib.pyplot as plt
import matplotlib.gridspec
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


# Removing the redundant 'Unnamed: 0' column
df.drop('Unnamed: 0', axis=1, inplace=True)
print(df.head())


# Removing salary and salary_currency column and renaming salary_in_usd to salary
df.drop(['salary', 'salary_currency'], axis=1, inplace=True)
df.rename(columns={'salary_in_usd': 'salary'}, inplace=True)


# Removing duplicate rows of data (42 rows)
print(df.duplicated().sum())
df.drop_duplicates(inplace=True)

# Changing country names in country_location and employee_residence from abbreviations to full country names
coco = cc.CountryConverter()
df['employee_residence'] = coco.convert(df['employee_residence'], to='name_short')
df['company_location'] = coco.convert(df['company_location'], to='name_short')
print(df.head())

# Changing company_size from abbreviated to extended values
print(df['company_size'].value_counts())
df['company_size'] = df['company_size'].map({
    'S': 'Small',
    'M': 'Medium',
    'L': 'Large'

})
print(df.head())


# Changing experience_level from abbreviated to extended values
print(df['experience_level'].value_counts())
df['experience_level'] = df['experience_level'].map({
    'EN': 'Entry-Level',
    'MI': 'Mid-Level',
    'SE': 'Senior-Level',
    'EX': 'Executive-Level'

})
print(df.head())


# Changing employment_type from abbreviated to extended values
print(df['employment_type'].value_counts())
df['employment_type'] = df['employment_type'].map({
    'FL': 'Freelance',
    'CT': 'Contract',
    'PT': 'Part-Time',
    'FT': 'Full-Time'

})


# Changing remote ratio to remote percentage
df.rename(columns={'remote_ratio': 'remote_percentage'}, inplace=True)


# Finding the correlation between remote_percentage and experience_level
sns.set_palette('autumn')
sns.set_style('whitegrid')

# finding which countries have the highest amount of remote workers
top_remote_locations = df.groupby('company_location')['remote_percentage'].mean().sort_values(ascending=False)[:20]

ax = sns.barplot(y=top_remote_locations.index, x=top_remote_locations, palette='autumn')
ax.set_title('Countries With Most Remote Workers', fontdict={'fontsize': 16})
plt.show()

exp_lvl_gb = df.groupby('experience_level')['remote_percentage'].mean().sort_values()

ax = sns.barplot(x=exp_lvl_gb.index, y=exp_lvl_gb, order=['Entry-Level', 'Mid-Level', 'Senior-Level', 'Executive-Level'], data=df)
ax.set_title('Experience Level Vs Mean Remote Percentage', fontdict={'fontsize': 14})
plt.show()


# mean salary by year and job type
mean_s_work_year = df.groupby('work_year')['salary'].mean().sort_values()
fig, axes = plt.subplots(1,2)

ax = sns.barplot(x=mean_s_work_year.index, y=mean_s_work_year, data=df, ax=axes[0])
ax.set_title('Mean Salary VS Work Year', fontdict={'fontsize': 14})

mean_s_remote_percentage_year = df.groupby('work_year')['remote_percentage'].mean().sort_values()
ax = sns.barplot(x=mean_s_remote_percentage_year.index, y=mean_s_remote_percentage_year, data=df, ax=axes[1])
ax.set_title('Mean Remote Percentage by Year', fontdict={'fontsize': 14})
plt.show()


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


# comparing job_type and company_size to their salaries
plt.figure(figsize=(15, 6))
sns.set_palette('autumn')
ax = sns.boxenplot(data=df, x='job_type', y='salary', order=['In-Person', 'Hybrid', 'Remote'], hue='company_size')
ax.set_title('Job Type & Company Size VS Salary', fontdict={'fontsize': 14})
plt.show()

