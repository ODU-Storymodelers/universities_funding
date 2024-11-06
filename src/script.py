import pandas as pd
import matplotlib.pyplot as plt

# Load the data (assuming you have a CSV file with the given columns)
# Replace 'path_to_file.csv' with the path to your actual data file
data = pd.read_excel('university_funding/data.xlsx')


# Change the column names to strings
data.columns = data.columns.astype(str)


# Convert '2010' and '2022' columns to numeric, replacing non-numeric values with NaN
data['2010'] = pd.to_numeric(data['2010'], errors='coerce')
data['2022'] = pd.to_numeric(data['2022'], errors='coerce')



# Convert all year columns to numeric
years = [str(year) for year in range(2010, 2023)]  # Include 2022
for year in years:
    data[year] = pd.to_numeric(data[year], errors='coerce')

# Calculate year-over-year growth rates for each institution
data['Avg_Yearly_Growth'] = 0  # Initialize the column

for index, row in data.iterrows():
    yearly_growths = []
    for i in range(len(years) - 1):
        current_year = years[i]
        next_year = years[i+1]
        if pd.notnull(row[current_year]) and pd.notnull(row[next_year]) and row[current_year] > 0:
            growth = (row[next_year] - row[current_year]) / row[current_year]
            yearly_growths.append(growth)
    
    if yearly_growths:  # Check if we have any valid growth rates
        data.at[index, 'Avg_Yearly_Growth'] = sum(yearly_growths) / len(yearly_growths)



# Calculate the growth rate between 2010 and 2022 for each institution

# Sort the universities based on funding growth (from highest to lowest)
data_sorted = data.sort_values(by='Avg_Yearly_Growth', ascending=False)

# Select relevant columns to display
ranked_data = data_sorted[['Institution', 'Avg_Yearly_Growth']]


# Export the ranked data to a new Excel file
ranked_data.to_excel('university_funding/ranked_universities_avg_growth.xlsx')

# Repeat filtering only for the rank between 135 and 190
ranked_data_135_190 = data_sorted[data['Rank'].between(135, 190)]
ranked_data_135_190 = ranked_data_135_190[['Institution', 'Avg_Yearly_Growth']]

# Export the ranked data to a new Excel file
ranked_data_135_190.to_excel('university_funding/ranked_universities_avg_growth_135_190.xlsx')

# Repeat filtering only for the rank between 198 and 134
ranked_data_98_134 = data_sorted[data['Rank'].between(98, 134)]
ranked_data_98_134 = ranked_data_98_134[['Institution', 'Avg_Yearly_Growth']]

# Export the ranked data to a new Excel file
ranked_data_98_134.to_excel('university_funding/ranked_universities_avg_growth_98_134.xlsx')

