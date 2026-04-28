import os
import requests
import pandas as pd
import json
import sqlite3

def fetch_and_parse_real_data():
    # Using the real public fileapi endpoint and public authorization key
    url = "https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization=rdec-key-123-45678-011121314&format=JSON"
    
    # Ignore SSL Warnings
    import urllib3
    urllib3.disable_warnings()

    print("Fetching real data from CWA fileapi endpoint...")
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"Error fetching data: HTTP {response.status_code}")
        print(response.text)
        return
    
    # Parse json and dump raw
    data = response.json()
    with open('raw_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Extract locations based on F-A0010-001 file structure
    locations = data['cwaopendata']['resources']['resource']['data']['agrWeatherForecasts']['weatherForecasts']['location']
    
    rows = []
    
    for loc in locations:
        loc_name = loc['locationName'].replace('地區', '')
        
        weatherElements = loc['weatherElements']
        max_ts = weatherElements['MaxT']['daily']
        min_ts = weatherElements['MinT']['daily']
        
        for max_day, min_day in zip(max_ts, min_ts):
            date = max_day['dataDate']
            max_t = float(max_day['temperature'])
            min_t = float(min_day['temperature'])
            avg_t = (max_t + min_t) / 2
            
            rows.append({
                'Region': loc_name,
                'Date': date,
                'Min_Temperature': min_t,
                'Max_Temperature': max_t,
                'Avg_Temperature': avg_t
            })
            
    df = pd.DataFrame(rows)
    
    # Save to CSV
    df.to_csv("weather_data.csv", index=False, encoding='utf-8-sig')
    print("Saved real data to weather_data.csv")
    
    # Save to SQLite
    conn = sqlite3.connect('weather.db')
    df.to_sql('forecast', conn, if_exists='replace', index=False)
    conn.close()
    print("Saved real data to SQLite (weather.db)")
    
    print(df.head())

if __name__ == "__main__":
    fetch_and_parse_real_data()
