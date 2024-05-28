# Delaware Health Code Violations Exploratory Data Analysis

Data from: [https://www.kaggle.com/datasets/msjahid/delaware-restaurant-inspection-violations-records](https://www.kaggle.com/datasets/msjahid/delaware-restaurant-inspection-violations-records)

## Context
Businesses in the state of Delaware must undergo routine health inspections by the Department of Health. These businesses have strict regulations that they must adhere to so that they may continue to operate. If they fail to meet a standard as set by the Department of Health, they receive a health code violation. This analysis is to look into these violations and examine their frequency, location, and any trends.

## Prompt
You work for the Delaware Department of Health and are tasked with examining data relating to health code violations to answer the following questions, in addition to creating visuals to support your findings.

## Questions seeking answers:
- What cities have the most health code violations?
- What's the most common inspection type?
- What health code violations are the most common?
- What trends can we find by examining violations by month?
- What trends can we find among the most common health code violations by month?

## Loading the data, some light cleaning to start, and gaining insight into its structure
```
import numpy as np # Linear Algebra
import pandas as pd # Data Processing
import matplotlib.pyplot as plt # Visualizations
import seaborn as sns # Visualizations
import re # Data Cleaning

pd.set_option('display.max_columns', None)

# Importing Data
df = pd.read_csv(r'C:\Users\becke\Desktop\Delaware_Restaurant_Inspection_Violations.csv')

# Replacing spaces in column names with underscores
df.columns = df.columns.str.replace(' ', '_')

# ----- Understanding Data

# Understanding the data
print(df.dtypes)
print('Column Names: ', df.columns)

print('Unique establishment city values: \n', df.Food_Establishment_City.unique())
print('Unique establishment zip code values: \n', df.Food_Establishment_Zip_Code.unique())
print('Unique inspection type values: \n', df.Inspection_Type.unique())
print('Unique violation code values: \n', df.Violation_Code.unique())

# Counting How many unique values there are
print(pd.value_counts(df.Food_Establishment_City))
print(pd.value_counts(df.Food_Establishment_Zip_Code))
print(pd.value_counts(df.Inspection_Type))
print(pd.value_counts(df.Violation_Code))
```

Right away we can get a good understanding of the data we're working with:
- This data contains all violations across the state of Delaware from 04/18/2022-04/16/2024.
- There are three inspection types:
  - Routine
  - Follow-up
  - Complaint
- There are many different kinds of violations, and the type of violations are varied across locations.
- Some fields, like 'Inspection_Type' are floats, when they should be integers.
- There are repeated rows, and NaN (Null or missing) values.

Before we start our analysis, let's clean the data so that it is more accurate and meaningful.
```
# Looking for duplicated rows
print(df.duplicated().sum()) # 243 duplicated rows
df = df.drop_duplicates()

# Looking for null values
print(df.isnull().sum()) # 22 null values, specifically in Food_Establishment_Zip_Code
df = df.dropna().reset_index()

# Function to extract latitude and longitude from 'Geocoded Location'
def extract_coordinates(location):
    match = re.search(r'\(([^,]+), ([^)]+)\)', location)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

df['Latitude'], df['Longitude'] = zip(*df['Geocoded_Location'].apply(extract_coordinates))

df.drop(columns=['Geocoded_Location'], inplace=True)

# Converting Inspection_Type to datetime format
df['Inspection_Date'] = pd.to_datetime(df['Inspection_Date'], format='%m/%d/%Y')

# Converting Food_Establishment_Zip_Code from float to int
df.Food_Establishment_Zip_Code = df.Food_Establishment_Zip_Code.astype(int)
# print(df.dtypes)
```

Now that we have data that has been transformed to be more meaningful, while also removing missing or repeated values, we can begin our analysis.

## Exploring the data

First, let's create a visual to answer our first question, "What cities have the most health code violations?"
```
top_cities = df['Food_Establishment_City'].value_counts().head(10)

# Sorting cities in descending order
top_cities_sorted_desc = top_cities[::-1]

# Determining figure size, and plot properties
plt.figure(figsize=(15, 6))
bars = top_cities_sorted_desc.plot(kind='barh', color=['#d3d3d3']*9 + ['#669ca4'], edgecolor='black')

# Adding value labels
for i, value in enumerate(top_cities_sorted_desc):
    plt.text(value, i, str(value), va='center', ha='left',)

# Plotting figure
plt.title('Top 10 Cities by Violation Count', fontsize=20, pad=20)
plt.ylabel('')
plt.show()
```
![Alt text](https://i.imgur.com/CxmLCG1.png)

From this, we can see that the city of Wilmington has the most health code violations at 6,985. Which is double the amount of the city with the second most violations. We can also break down this information into a table, so it's easier to read and comprehend.

| City  | Number of Violations |
| ------------- | ------------- |
| Wilmington  | 6985  |
| Dover  | 3495  |
| Newark  | 2407  |
| New Castle  | 2378  |
| Rehoboth Beach  | 1598  |
| Millsboro  | 1539  |
| Milford  | 1441  |
| Lewes  | 1223  |
| Wyoming  | 841  |
| Smyrna  | 801  |

Now that we know which cities have the most violations, this begs a question. Do people in Wilmington complain more to the Health Department? To examine the issue we can create a visual to answer our second question, "What's the most common inspection type?"
```
inspection_type = df['Inspection_Type'].value_counts()
inspection_type_desc = inspection_type[::-1]
plt.figure(figsize=(15, 6))
bars = inspection_type_desc.plot(kind='barh', color=['#d3d3d3']*2 + ['#669ca4'], edgecolor='black')

for i, value in enumerate(inspection_type_desc):
    plt.text(value, i, str(value), va='center', ha='left')

plt.title('Inspection Type Occurrence', fontsize=20, pad=20)
plt.ylabel('')
plt.show()
```
![Alt text](https://i.imgur.com/apGaH3X.png)

Now that we have visualized this, we can tell the most common type of inspection are 'Routine' inspections. This also tells us it's less likely that Wilmington has more violations due to to customer complaints. 

Now that we know the cities with the most amount of violations, we can move onto examining our next question, "What health code violations are the most common?"
```
violation_type = df['Violation_Code'].value_counts().head(15)
violation_type_desc = violation_type[::-1]
plt.figure(figsize=(15, 6))
bars = violation_type_desc.plot(kind='barh', color=['#d3d3d3']*14 + ['#669ca4'], edgecolor='black')

for i, value in enumerate(violation_type_desc):
    plt.text(value, i, str(value), va='center', ha='left')

plt.title('Violation Count Occurrence', fontsize=20, pad=20)
plt.ylabel('')
plt.show()
```
![Alt text](https://i.imgur.com/3Y58PtY.png)

Given the number of violations throughout this two-year period I thought it would be insightful to examine the 15 most popular violations that occur. While the result is a great visual that tells us what violation occurs most, it's hard to gain insight into the exact violation without more context. So, let's create a table that tells us what these violations mean.
```
violation_type_desc = violation_type_desc.reset_index()
violation_type_desc = violation_type_desc[::-1]
violation_type_desc.columns = ['Violation_Code', 'Violation_Count']

violation_type_description = df[['Violation_Code', 'Violation_Description']].drop_duplicates()
all_violations = pd.merge(violation_type_desc, violation_type_description, on="Violation_Code")

fig, ax = plt.subplots(figsize=(15, 6))
ax.axis('off')

table = ax.table(cellText=all_violations.values, colLabels=all_violations.columns, cellLoc='center', loc='center')
table.auto_set_column_width(col=list(range(len(all_violations.columns))))
table.scale(1, 2)

for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_fontsize(12)
        cell.set_text_props(weight='bold')
    if key[1] == 2 and key[0] != 0:
        cell.set_text_props(ha='left')

plt.title('Top 15 Violation Codes and Descriptions', fontsize=15, pad=35)
plt.show()
```
![Alt text](https://imgur.com/ajhHLdJ.png)

Great! Now we can see what the top 15 violations mean exactly. The leading cause of health code violations are 'Sanitizing Solutions, Testing Devices' with 'Certified Food Protection Manager' and 'Time/Temperature Control for Safety Food, Hot and Cold Holding' following shortly behind. It looks like food safety violations are the most common type of violations.

What about specifically the city of Wilmington? Let's create a table to examine their 15 most common health code violations.
```
wilmington_data = df[df['Food_Establishment_City'] == 'Wilmington']
wilmington_vc = wilmington_data['Violation_Code'].value_counts().head(15)

wilmington_vc = wilmington_vc.reset_index()
wilmington_vc.columns = ['Violation_Code', 'Violation_Count']

wilmington_vc_descriptions = df[['Violation_Code', 'Violation_Description']].drop_duplicates()
wilmington_top_violations = pd.merge(wilmington_vc, wilmington_vc_descriptions, on='Violation_Code')

fig, ax = plt.subplots(figsize=(15, 6))
ax.axis('off')

table = ax.table(cellText=wilmington_top_violations.values, colLabels=wilmington_top_violations.columns, cellLoc='center', loc='center')
table.auto_set_column_width(col=list(range(len(all_violations.columns))))
table.scale(1, 2)

for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_fontsize(12)
        cell.set_text_props(weight='bold')
    if key[1] == 2 and key[0] != 0:
        cell.set_text_props(ha='left')

plt.title('Wilmingtons Top 15 Violation Codes and Descriptions', fontsize=15, pad=35)
plt.show()
```
![Alt text](https://i.imgur.com/BH2bqw1.png)

Although we can see similar results for Wilmington compared to the state-wide analysis, we can see that Wilmington's leading health code violation is 'Controlling Pests'. Most of the other violations are again related to food safety with some being equipment and labor related.

I live in Newark, Delaware. For curiosities sake let's look at Newark's top 15 health code violations.
```
newark_data = df[df['Food_Establishment_City'] == 'Newark']
newark_vc = newark_data['Violation_Code'].value_counts().head(15)

newark_vc = newark_vc.reset_index()
newark_vc.columns = ['Violation_Code', 'Violation_Count']

newark_vc_descriptions = df[['Violation_Code', 'Violation_Description']].drop_duplicates()
newark_top_violations = pd.merge(newark_vc, newark_vc_descriptions, on='Violation_Code')

fig, ax = plt.subplots(figsize=(15, 6))
ax.axis('off')

table = ax.table(cellText=newark_top_violations.values, colLabels=newark_top_violations.columns, cellLoc='center', loc='center')
table.auto_set_column_width(col=list(range(len(all_violations.columns))))
table.scale(1, 2)

for key, cell in table.get_celld().items():
    if key[0] == 0:
        cell.set_fontsize(12)
        cell.set_text_props(weight='bold')
    if key[1] == 2 and key[0] != 0:
        cell.set_text_props(ha='left')

plt.title('Newarks Top 15 Violation Codes and Descriptions', fontsize=15, pad=35)
plt.show()
```
![Alt text](https://i.imgur.com/8oUdE59.png)

Here we can see similar results to the state-wide analysis with food safety issues being among the most frequent.

Now lets move on to answering our next question, "What trends can we find by examining violations by month?"
```
df['Inspection_Month'] = df['Inspection_Date'].dt.month
violations_month = df['Inspection_Month'].value_counts().sort_index()

plt.figure(figsize= (15,6))

violations_month.plot(kind='bar')
plt.title('Violations by Month')
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

plt.show()
```
![Alt text](https://i.imgur.com/LqgXaf8.png)

We can gain some valuable insight from this visual. January has the most violations, with another notable peek in October. From winter into spring, violations occur less frequently until May when there is a sudden spike. Violations are least frequent in the summer months of June and July, when they raise dramatically leading into the fall months of August, September, and October. 

Now that we know the months where these violations occur most frequently, let's create a visual to answer our last question, "What trends can we find among the most common health code violations by month?"
```
violation_type = df['Violation_Code'].value_counts().head(5)
violation_type_desc = violation_type[::-1]
plt.figure(figsize=(15, 6))
bars = violation_type_desc.plot(kind='barh', color=['#d3d3d3']*4 + ['#669ca4'], edgecolor='black')

for i, value in enumerate(violation_type_desc):
    plt.text(value, i, str(value), va='center', ha='left')

plt.title('Top 5 Violation Count Occurrence', fontsize=20, pad=20)
plt.ylabel('')
plt.show()
```
![Alt text](https://i.imgur.com/GK3CeNg.png)

As a reminder, here are the top 5 health code violation descriptions:

| Violation Code  | Description |
| ------------- | ------------- |
| 4-302.14  | Sanitizing Solutions, Testing Devices  |
| 2-102.12  | Certified Food Protection Manager  |
| 3-501.16  | Time/Temperature Control for Safety Food, Hot and Cold Holding  |
| 5-205.11  | Using a Handwashing Sink-Operation and Maintenance  |
| 6-301.12  | Hand Drying Provision  |

We gain some very interesting insight from this. We can see similar trends as the previous visual, where leading into the summer months the most common violations are declining until May when they suddenly spike. The violation of "Certified Food Protection Manager" beat out the top violation of "Sanitizing Solutions, Testing Devices" which may relate to retention as summer approaches. All violations decrease leading into summer with "Time/Temperature Control for Safety Food, Hot and Cold Holding" beating out all other violations in July. In September, these violations started to increase but are not near the amount as they were in the May peak, other than "Sanitizing Solutions, Testing Devices" which suggests that violations normally out of the top 5 are the leading causes. "Sanitizing Solutions, Testing Devices" takes over for the rest of the year as the leading violation.

## Conclusion
Throughout this project, we were able to clean, explore, and analyze our data using Python. Through transforming and visualizing our data, we were able to find answers to our questions. We found that over two years, Wilmington had the most health code violations with 6,985 violations total. The most common type of inspection by a large lead is 'Routine' inspections. Most health code violations across the state were related to food safety, with the most prominent being "Sanitizing Solutions, Testing Devices". When we examined the violations monthly, we found that there are the most violations in January at over 3,000 violations. We can also see that these violations decline into summer reaching a low point in July at just over 1,500. In August they start to spike again reaching slightly over 3,000 violations where they drop again leading into the new year.

**Overall there are many health code violations across the state with Wilmington having the most by far, and most health code violations are related to food safety standards.**






