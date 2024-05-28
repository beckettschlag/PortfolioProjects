# -----
# Questions Seeking Answers:
# 1. What cities have the most health code violations?
# 2. What health code violations are most common?
# 3. What's the most common type of inspection type?
# 4. What's the frequency of inspections?
# -----

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
print(pd.value_counts(df.Food_Establishment_City)) # Many unique values across delaware, most populated being Wilmington, Dover, Newark, New Castle
print(pd.value_counts(df.Food_Establishment_Zip_Code)) # Similar findings as above, NOTE: Zip Codes listed as floats, CHANGE TO INT
print(pd.value_counts(df.Inspection_Type)) # Routine: 24408, Follow-up: 5791, Complaint, 387
print(pd.value_counts(df.Violation_Code)) # Many violation types

# ----- Cleaning data

# Looking for duplicated rows
print(df.duplicated().sum()) # 243 duplicated rows
df = df.drop_duplicates()

# Looking for null values
print(df.isnull().sum()) # 22 null values, specifically in Food_Establishment_Zip_Code
df = df.dropna().reset_index()

#Function to extract latitude and longitude from 'Geocoded Location' String
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

# -----

# Creating Food_Establishment_City top 10 visualization
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


# Creating Inspection_Type visualization
inspection_type = df['Inspection_Type'].value_counts()
inspection_type_desc = inspection_type[::-1]
plt.figure(figsize=(15, 6))
bars = inspection_type_desc.plot(kind='barh', color=['#d3d3d3']*2 + ['#669ca4'], edgecolor='black')

for i, value in enumerate(inspection_type_desc):
    plt.text(value, i, str(value), va='center', ha='left')

plt.title('Inspection Type Occurrence', fontsize=20, pad=20)
plt.ylabel('')
plt.show()


# Creating Violation_Code visualization
violation_type = df['Violation_Code'].value_counts().head(15)
violation_type_desc = violation_type[::-1]
plt.figure(figsize=(15, 6))
bars = violation_type_desc.plot(kind='barh', color=['#d3d3d3']*14 + ['#669ca4'], edgecolor='black')

for i, value in enumerate(violation_type_desc):
    plt.text(value, i, str(value), va='center', ha='left')

plt.title('Violation Count Occurrence', fontsize=20, pad=20)
plt.ylabel('')
plt.show()


# Creating a Table with violation code descriptions
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


# Filter violation codes for Wilmington
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


# Filter violation codes for Newark
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


# Plotting total violations by month
df['Inspection_Month'] = df['Inspection_Date'].dt.month
violations_month = df['Inspection_Month'].value_counts().sort_index()

plt.figure(figsize= (15,6))

violations_month.plot(kind='bar')
plt.title('Violations by Month')
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()

plt.show()

# Plotting most popular violations by Month
df['Month'] = df['Inspection_Date'].dt.month
# ---
violations_per_code_per_month = df.groupby(['Month', 'Violation_Code']).size().reset_index(name='Count')
top_violations = violations_per_code_per_month.groupby('Violation_Code')['Count'].sum().nlargest(5).index
top_violations_data = violations_per_code_per_month[violations_per_code_per_month['Violation_Code'].isin(top_violations)]
pivot_top_violations = top_violations_data.pivot(index='Month', columns='Violation_Code', values='Count').fillna(0)

plt.figure(figsize=(15, 6))

for code in top_violations:
    plt.plot(pivot_top_violations.index, pivot_top_violations[code], label=f'Violation Code {code}')

plt.xlabel('Month')
plt.ylabel('Number of Violations')
plt.title('Top 5 Health Code Violations by Month in Delaware')
plt.legend()
plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.show()

# Top 5 Violations Visualization
violation_type = df['Violation_Code'].value_counts().head(5)
violation_type_desc = violation_type[::-1]
plt.figure(figsize=(15, 6))
bars = violation_type_desc.plot(kind='barh', color=['#d3d3d3']*4 + ['#669ca4'], edgecolor='black')

for i, value in enumerate(violation_type_desc):
    plt.text(value, i, str(value), va='center', ha='left')

plt.title('Top 5 Violation Count Occurrence', fontsize=20, pad=20)
plt.ylabel('')
plt.show()
