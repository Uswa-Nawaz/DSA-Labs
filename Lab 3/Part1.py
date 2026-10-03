import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('population_by_country_2020.csv')

list1 = df['Country (or dependency)'].values.tolist()
list2 = df['Population (2020)'].values.tolist()

plt.bar(list1, list2, width=1, color=['red', 'green'])

plt.show()

# ---- Fitbit Task 1: line chart of total steps per day ----
activity = pd.read_csv('fitbit/dailyActivity_merged.csv')
activity['ActivityDate'] = pd.to_datetime(activity['ActivityDate'])

daily_steps = activity.groupby('ActivityDate')['TotalSteps'].sum()

plt.figure()
plt.plot(daily_steps.index, daily_steps.values)
plt.title('Total Steps per Day (all users)')
plt.xlabel('Date')
plt.ylabel('Total Steps')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---- Fitbit Task 2: bar chart of total distance per day ----
daily_distance = activity.groupby('ActivityDate')['TotalDistance'].sum()

plt.figure()
plt.bar(daily_distance.index, daily_distance.values)
plt.title('Total Distance Covered per Day (all users)')
plt.xlabel('Date')
plt.ylabel('Total Distance (km)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---- Fitbit Task 3: scatter chart of total time in bed ----
sleep = pd.read_csv('fitbit/sleepDay_merged.csv')
sleep['SleepDay'] = pd.to_datetime(sleep['SleepDay'])

plt.figure()
plt.scatter(sleep['SleepDay'], sleep['TotalTimeInBed'])
plt.title('Total Time in Bed (each dot = one person, one night)')
plt.xlabel('Date')
plt.ylabel('Time in Bed (minutes)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# ---- Fitbit Task 4: pie chart of hourly steps on 12 April 2016 ----
hourly = pd.read_csv('fitbit/hourlySteps_merged.csv')
hourly['ActivityHour'] = pd.to_datetime(hourly['ActivityHour'])

# keep only the rows from 12 April 2016
day = hourly[hourly['ActivityHour'].dt.strftime('%Y-%m-%d') == '2016-04-12']

# add up the steps of all people for each hour (0 to 23)
steps_by_hour = day.groupby(day['ActivityHour'].dt.hour)['StepTotal'].sum()
print(steps_by_hour)

labels = [str(h) + ':00' for h in steps_by_hour.index]

plt.figure(figsize=(10, 7))
plt.pie(steps_by_hour.values, startangle=90)
plt.legend(labels, title='Hour', loc='center left', bbox_to_anchor=(1, 0.5))
plt.title('Steps per Hour on 12 April 2016 (all users)')
plt.tight_layout()
plt.show()