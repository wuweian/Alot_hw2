import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import random

# Regions in Taiwan
regions = ['北部', '中部', '南部', '東北部', '東部', '東南部']
start_date = datetime(2026, 5, 1)

data = []

# Generate 7 days of realistic mock data
for i in range(7):
    date_str = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
    for region in regions:
        # Simulate local temperature base ranges depending on the region
        if region == '北部':
            min_t = random.randint(16, 21)
            max_t = min_t + random.randint(3, 6)
        elif region == '南部':
            min_t = random.randint(24, 28)
            max_t = min_t + random.randint(4, 7)
        elif region == '中部':
            min_t = random.randint(20, 24)
            max_t = min_t + random.randint(4, 8)
        else:
            min_t = random.randint(19, 23)
            max_t = min_t + random.randint(4, 7)
            
        avg_t = (min_t + max_t) / 2
        data.append([region, date_str, float(min_t), float(max_t), float(avg_t)])

# Create DataFrame
df = pd.DataFrame(data, columns=['Region', 'Date', 'Min_Temperature', 'Max_Temperature', 'Avg_Temperature'])

# Save to CSV
df.to_csv('weather_data.csv', index=False, encoding='utf-8-sig')

# Save to SQLite
conn = sqlite3.connect('weather.db')
df.to_sql('forecast', conn, if_exists='replace', index=False)
conn.close()

print("Successfully generated 7 days of mock data and populated both CSV and weather.db!")
