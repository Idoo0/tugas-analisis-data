import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
day_df = pd.read_csv('day.csv')
hour_df = pd.read_csv('hour.csv')

# Mapping for weekdays
weekday_mapping = {
    0: 'Sunday',
    1: 'Monday',
    2: 'Tuesday',
    3: 'Wednesday',
    4: 'Thursday',
    5: 'Friday',
    6: 'Saturday'
}

# Set Seaborn style and palette
sns.set(style="whitegrid")
palette = sns.color_palette("muted")

st.title("Bike Sharing Analysis Dashboard")

# --- 1. Analysis: Day and Time of Most Bike Rentals ---
st.header("1. On which day and time are most bikes rented?")
st.write("""
The following charts show when the most bike rentals occur by weekday, and compare total users, registered users, and casual users.
""")

# Convert hour and day columns
# mengganti data type untuk kolom dteday pada tabel day dan hour menjadi datetime

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Aggregating data by weekday and hour
weekday_grouped = day_df.groupby('weekday').agg({'cnt': 'sum', 'registered': 'sum', 'casual': 'sum'}).reset_index()

fig, ax = plt.subplots(figsize=(18, 12))
width = 0.2
x = np.arange(len(weekday_grouped))

# Plot the bars
total_bars = ax.bar(x - width, weekday_grouped['cnt'], width, label='Total Customers', color=palette[0])
registered_bars = ax.bar(x, weekday_grouped['registered'], width, label='Registered Customers', color=palette[1])
casual_bars = ax.bar(x + width, weekday_grouped['casual'], width, label='Casual Customers', color=palette[2])

# Highlight highest bars
max_total_index = weekday_grouped['cnt'].idxmax()
max_registered_index = weekday_grouped['registered'].idxmax()
max_casual_index = weekday_grouped['casual'].idxmax()

# Add stars above the highest bars
ax.annotate('★', 
            (x[max_total_index] - width, weekday_grouped['cnt'][max_total_index] + 5),
            color='black', fontsize=20, ha='center')
ax.annotate('★', 
            (x[max_registered_index], weekday_grouped['registered'][max_registered_index] + 5),
            color='black', fontsize=20, ha='center')
ax.annotate('★', 
            (x[max_casual_index] + width, weekday_grouped['casual'][max_casual_index] + 5),
            color='black', fontsize=20, ha='center')

# Set labels and title
ax.set_xlabel('Weekday')
ax.set_ylabel('Number of Customers')
ax.set_title('Total, Registered, and Casual Customers by Weekday')
ax.set_xticks(x)
ax.set_xticklabels([weekday_mapping[i] for i in weekday_grouped['weekday']])
ax.legend()

st.pyplot(fig)

st.write("""
The following charts show when the most bike rentals occur by hours, and compare total users, registered users, and casual users.
""")

# Convert hour and day columns
# mengganti data type untuk kolom dteday pada tabel day dan hour menjadi datetime

day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Aggregating data by weekday and hour
weekday_grouped = hour_df.groupby('hr').agg({'cnt': 'sum', 'registered': 'sum', 'casual': 'sum'}).reset_index()

fig, ax = plt.subplots(figsize=(18, 12))
width = 0.2
x = np.arange(len(weekday_grouped))

# Plot the bars
total_bars = ax.bar(x - width, weekday_grouped['cnt'], width, label='Total Customers', color=palette[0])
registered_bars = ax.bar(x, weekday_grouped['registered'], width, label='Registered Customers', color=palette[1])
casual_bars = ax.bar(x + width, weekday_grouped['casual'], width, label='Casual Customers', color=palette[2])

# Highlight highest bars
max_total_index = weekday_grouped['cnt'].idxmax()
max_registered_index = weekday_grouped['registered'].idxmax()
max_casual_index = weekday_grouped['casual'].idxmax()

# Add stars above the highest bars
ax.annotate('★', 
            (x[max_total_index] - width, weekday_grouped['cnt'][max_total_index] + 5),
            color='black', fontsize=20, ha='center')
ax.annotate('★', 
            (x[max_registered_index], weekday_grouped['registered'][max_registered_index] + 5),
            color='black', fontsize=20, ha='center')
ax.annotate('★', 
            (x[max_casual_index] + width, weekday_grouped['casual'][max_casual_index] + 5),
            color='black', fontsize=20, ha='center')

# Set labels and title
ax.set_xlabel('Weekday')
ax.set_ylabel('Number of Customers')
ax.set_title('Total, Registered, and Casual Customers by Weekday')
ax.set_xticks(x)
ax.set_xticklabels([f"{i}:00" for i in weekday_grouped.index])
ax.legend()

st.pyplot(fig)
# --- 2. Analysis: Effect of Working Day and Holiday ---
st.header("2. Does working day or holiday affect casual or registered users?")
st.write("A correlation heatmap between working day, holiday, casual, and registered users:")

correlation_matrix = day_df[['workingday', 'holiday', 'casual', 'registered']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap: Working Day, Holiday, Casual, Registered')
st.pyplot(plt.gcf())

# --- 3. Analysis: Effect of Seasons on Total Cyclists ---
st.header("3. Effect of Seasons on Total Cyclists")
st.write("A correlation heatmap between season and the total number of users:")

season_corr = day_df[['season', 'cnt']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(season_corr, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap: Season and Total Users')
st.pyplot(plt.gcf())

# --- Conclusion ---
st.header("Conclusion")
st.markdown("""
1. **On which day and time are most bikes rented?**  
   - Total users rent bikes most frequently on **Friday**.  
   - Registered users rent mostly on **Thursday**, while casual users prefer **Saturday**.
   - Most users rent bikes at **6 PM**, though casual users peak at **2 PM**.

2. **Does working day or holiday affect casual or registered users?**  
   - Yes, casual users tend to rent more bikes on non-working days (50%), while 30% of registered users rent on non-working days.

3. **Effect of seasons on total cyclists?**  
   - A positive correlation exists between seasons and the number of users. Most cyclists rent bikes in **Fall** (Season 3), while **Winter** (Season 4) sees the lowest numbers.
""")
