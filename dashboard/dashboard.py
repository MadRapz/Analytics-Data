import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from babel.numbers import format_currency

# Load the cleaned data
day_cleaned = pd.read_csv("D:\Kuliah\Bangkit\Task\AnalisDataProjek\submission\data\day_cleaned.csv")
hour_cleaned = pd.read_csv("D:\Kuliah\Bangkit\Task\AnalisDataProjek\submission\data\hour_cleaned.csv")

# Convert date columns to datetime format
day_cleaned['dteday'] = pd.to_datetime(day_cleaned['dteday'])
hour_cleaned['dteday'] = pd.to_datetime(hour_cleaned['dteday'])

with st.sidebar:
    # Display company logo
    st.image("D:\Kuliah\Bangkit\Task\AnalisDataProjek\submission\dashboard\8-bit City_1920x1080.jpg")
    
    # Date range selection
    min_date = day_cleaned['dteday'].min()
    max_date = day_cleaned['dteday'].max()
    start_date, end_date = st.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Convert the selected dates to the same dtype as 'dteday' column
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data based on selected date range
filtered_day = day_cleaned[(day_cleaned['dteday'] >= start_date) & (day_cleaned['dteday'] <= end_date)]
filtered_hour = hour_cleaned[(hour_cleaned['dteday'] >= start_date) & (hour_cleaned['dteday'] <= end_date)]

# Dashboard Header
st.header("Bike Rental Analysis Dashboard :bike:")

#==========================================================================================================#

# Correlation analysis for daily data
st.subheader("Daily Correlation Between Weather Conditions and Bike Rentals")
correlation_day = filtered_day[['temp', 'hum', 'windspeed', 'cnt']].corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_day, annot=True, cmap='coolwarm')
plt.title('Weather and Daily Rentals Correlation')
st.pyplot(plt)

# Extract specific correlation values
temp_rental_corr = correlation_day.at['temp', 'cnt']
hum_rental_corr = correlation_day.at['hum', 'cnt']
windspeed_rental_corr = correlation_day.at['windspeed', 'cnt']

# Display correlation results with descriptions
st.write("Detailed Correlation Insights for Daily Rentals:")
st.write(f"**Temperature and Rental Count Correlation:** {temp_rental_corr:.2f} (Strongest positive correlation implies warmer weather increases rentals.)")
st.write(f"**Humidity and Rental Count Correlation:** {hum_rental_corr:.2f} (Negative correlation indicates higher humidity reduces rentals.)")
st.write(f"**Wind Speed and Rental Count Correlation:** {windspeed_rental_corr:.2f} (Slight negative correlation suggests higher wind speeds might decrease rentals.)")

# If needed, provide more detailed insights
if temp_rental_corr > 0.5:
    st.write("Since temperature has a strong positive correlation with rentals, marketing campaigns could focus on warm days.")
if hum_rental_corr < -0.5:
    st.write("Consider promoting indoor activities or providing discounts on particularly humid days to maintain rental levels.")
if windspeed_rental_corr < -0.2:
    st.write("On windy days, rentals decrease slightly, which might indicate a preference for less strenuous activities.")

#==========================================================================================================#

# Correlation analysis for hourly data
st.subheader("Hourly Correlation Between Weather Conditions and Bike Rentals")
correlation_hour = filtered_hour[['temp', 'hum', 'windspeed', 'cnt']].corr()
plt.figure(figsize=(10, 6))
sns.heatmap(correlation_hour, annot=True, cmap='coolwarm')
plt.title('Weather and Hourly Rentals Correlation')
st.pyplot(plt)

# Extract specific correlation values
temp_hourly_corr = correlation_hour.at['temp', 'cnt']
hum_hourly_corr = correlation_hour.at['hum', 'cnt']
windspeed_hourly_corr = correlation_hour.at['windspeed', 'cnt']

# Display correlation results with descriptions
st.write("Detailed Correlation Insights for Hourly Rentals:")
st.write(f"**Temperature and Rental Count Correlation:** {temp_hourly_corr:.2f} (Indicates that as temperature increases, hourly rentals generally increase.)")
st.write(f"**Humidity and Rental Count Correlation:** {hum_hourly_corr:.2f} (Shows a negative correlation, suggesting that higher humidity may deter hourly rentals.)")
st.write(f"**Wind Speed and Rental Count Correlation:** {windspeed_hourly_corr:.2f} (A negative correlation indicates that stronger winds may reduce the comfort or safety of biking, thus lowering rentals.)")

# Provide recommendations or further analysis suggestions based on correlations
if temp_hourly_corr > 0.5:
    st.write("Strategic promotions during warmer hours could potentially boost rental activity.")
if hum_hourly_corr < -0.5:
    st.write("Consider scheduling maintenance or offering promotions during high humidity periods to counteract reduced demand.")
if windspeed_hourly_corr < -0.2:
    st.write("Monitoring wind conditions and advising customers on optimal biking times could improve user experience and satisfaction.")

#==========================================================================================================#

# Bike rentals by weather situation (daily)
st.subheader("Daily Bike Rentals by Weather Condition")
plt.figure(figsize=(12, 6))
sns.boxplot(x='weathersit', y='cnt', data=filtered_day)
plt.title('Bike Rentals by Weather Condition (Daily)')
st.pyplot(plt)

# Calculate median rentals by weather condition
median_rentals_weather = filtered_day.groupby('weathersit')['cnt'].median().sort_values()

# Find the weather condition with the highest and lowest median rentals
max_weather_condition = median_rentals_weather.idxmax()
min_weather_condition = median_rentals_weather.idxmin()
max_rentals = median_rentals_weather.max()
min_rentals = median_rentals_weather.min()

# Map weather condition codes to descriptions (as needed)
weather_conditions = {1: 'Clear', 2: 'Misty', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}

# Displaying the results in Streamlit
st.write("Weather Condition Impact on Bike Rentals:")
st.write(f"**Highest Median Rentals:** {weather_conditions.get(max_weather_condition, 'N/A')} ({max_rentals} rentals)")
st.write(f"**Lowest Median Rentals:** {weather_conditions.get(min_weather_condition, 'N/A')} ({min_rentals} rentals)")

# Additional insights
st.write("Insights:")
if max_weather_condition == 1:
    st.write("Clear weather significantly increases bike rentals, suggesting good weather encourages biking.")
if min_weather_condition == 3 or min_weather_condition == 4:
    st.write("Poor weather (rain/snow) drastically reduces bike rentals, indicating a need for alternative transport solutions on bad weather days.")

#==========================================================================================================#

# Hourly Bike Rentals by Weather Condition
st.subheader("Hourly Bike Rentals by Weather Condition")
plt.figure(figsize=(12, 6))
sns.boxplot(x='weathersit', y='cnt', data=filtered_hour)
plt.title('Bike Rentals by Weather Condition (Hourly)')
st.pyplot(plt)

# Calculate median rentals by weather condition
median_hourly_rentals_weather = filtered_hour.groupby('weathersit')['cnt'].median().sort_values()

# Find the weather condition with the highest and lowest median rentals
max_hourly_weather_condition = median_hourly_rentals_weather.idxmax()
min_hourly_weather_condition = median_hourly_rentals_weather.idxmin()
max_hourly_rentals = median_hourly_rentals_weather.max()
min_hourly_rentals = median_hourly_rentals_weather.min()

# Map weather condition codes to descriptions
weather_conditions = {1: 'Clear', 2: 'Misty', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}

# Displaying the results in Streamlit
st.write("Detailed Analysis of Hourly Bike Rentals by Weather:")
st.write(f"**Highest Median Rentals:** {weather_conditions.get(max_hourly_weather_condition, 'N/A')} with {max_hourly_rentals} rentals per hour")
st.write(f"**Lowest Median Rentals:** {weather_conditions.get(min_hourly_weather_condition, 'N/A')} with {min_hourly_rentals} rentals per hour")

# Additional insights based on conditions
st.write("Insights:")
if max_hourly_weather_condition == 1:
    st.write("Clear weather leads to the highest number of hourly rentals, ideal for targeting promotions or events.")
if min_hourly_weather_condition == 3 or min_hourly_weather_condition == 4:
    st.write("Rain or snow significantly reduces the number of hourly rentals, possibly indicating the need for weather-adaptive rental options or promotions during inclement weather.")

#==========================================================================================================#

# Daily Bike Rentals by Day Type
st.subheader("Daily Bike Rentals by Day Type")
rentals_by_day = filtered_day.groupby(['holiday', 'weekday'])['cnt'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='weekday', y='cnt', hue='holiday', data=rentals_by_day)
plt.title('Average Daily Rentals by Day Type')
plt.xlabel('Weekday (0: Sunday, 6: Saturday)')
plt.ylabel('Average Number of Rentals')
st.pyplot(plt)

# Calculate the overall average rentals for holidays and non-holidays
average_rentals_holiday = rentals_by_day[rentals_by_day['holiday'] == 1]['cnt'].mean()
average_rentals_non_holiday = rentals_by_day[rentals_by_day['holiday'] == 0]['cnt'].mean()

# Calculate percentage change in rentals from non-holidays to holidays
if average_rentals_non_holiday > 0:
    percentage_change = ((average_rentals_holiday - average_rentals_non_holiday) / average_rentals_non_holiday) * 100

# Displaying the results in Streamlit
st.write("Bike Rental Patterns by Day Type:")
st.write(f"**Average Rentals on Holidays:** {average_rentals_holiday:.2f} bikes")
st.write(f"**Average Rentals on Non-Holidays:** {average_rentals_non_holiday:.2f} bikes")
if percentage_change is not None:
    st.write(f"**Percentage Change in Rentals from Non-Holidays to Holidays:** {percentage_change:.2f}%")

# Provide insights based on the data
st.write("Insights:")
if percentage_change > 0:
    st.write("Bike rentals increase on holidays, suggesting a potential opportunity for targeted promotions or special offers.")
elif percentage_change < 0:
    st.write("Bike rentals decrease on holidays, which may indicate closures, reduced demand, or a shift in user behavior.")
else:
    st.write("No significant change in bike rentals between holidays and non-holidays.")

#==========================================================================================================#

# Hourly Bike Rentals by Day Type
st.subheader("Hourly Bike Rentals by Day Type")
rentals_by_hour = filtered_hour.groupby(['holiday', 'weekday'])['cnt'].mean().reset_index()
plt.figure(figsize=(12, 6))
sns.barplot(x='weekday', y='cnt', hue='holiday', data=rentals_by_hour)
plt.title('Average Hourly Rentals by Day Type')
plt.xlabel('Weekday (0: Sunday, 6: Saturday)')
plt.ylabel('Average Number of Rentals')
st.pyplot(plt)

# Calculate the overall average rentals for holidays and non-holidays
average_hourly_rentals_holiday = rentals_by_hour[rentals_by_hour['holiday'] == 1]['cnt'].mean()
average_hourly_rentals_non_holiday = rentals_by_hour[rentals_by_hour['holiday'] == 0]['cnt'].mean()

# Calculate percentage change in rentals from non-holidays to holidays
percentage_change_hourly = ((average_hourly_rentals_holiday - average_hourly_rentals_non_holiday) / average_hourly_rentals_non_holiday) * 100 if average_hourly_rentals_non_holiday else None

# Displaying the results in Streamlit
st.write("Insights on Hourly Bike Rentals:")
st.write(f"**Average Hourly Rentals on Holidays:** {average_hourly_rentals_holiday:.2f} bikes")
st.write(f"**Average Hourly Rentals on Non-Holidays:** {average_hourly_rentals_non_holiday:.2f} bikes")
if percentage_change_hourly is not None:
    st.write(f"**Percentage Change in Hourly Rentals from Non-Holidays to Holidays:** {percentage_change_hourly:.2f}%")

# Provide strategic insights based on the data
if percentage_change_hourly and percentage_change_hourly > 0:
    st.write("There is an increase in bike rentals per hour on holidays, suggesting higher leisure activity. Consider increasing available bikes and staffing on these days.")
elif percentage_change_hourly and percentage_change_hourly < 0:
    st.write("There is a decrease in bike rentals per hour on holidays, possibly due to closures or other factors reducing demand.")
else:
    st.write("No significant change in bike rentals between holidays and non-holidays.")


st.caption('Copyright © I Gede Made Rapriananta Pande 2024')
