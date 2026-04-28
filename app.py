import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import sqlite3
import os

# Set layout
st.set_page_config(layout="wide", page_title="Taiwan Weather Forecast", page_icon="🌦️")

st.title("Taiwan 7-Day Regional Agricultural Weather Forecast")

def load_data():
    # If the database exists, query from SQLite
    if os.path.exists("weather.db"):
        conn = sqlite3.connect("weather.db")
        df = pd.read_sql_query("SELECT * FROM forecast", conn)
        conn.close()
        return df
    # Fallback to CSV if DB doesn't exist yet
    elif os.path.exists("weather_data.csv"):
        return pd.read_csv("weather_data.csv")
    else:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No weather data found in database. Please run fetch_weather.py to fetch data from CWA API.")
    st.stop()

# Regional coordinates (approximate)
REGION_COORDS = {
    '北部': [25.0330, 121.5654],
    '中部': [23.9738, 120.9796],
    '南部': [22.6272, 120.3014],
    '東北部': [24.7505, 121.7516],
    '東部': [23.9855, 121.6033],
    '東南部': [22.7554, 121.1504]
}

def get_color(t):
    if t < 20:
        return 'blue'
    elif 20 <= t <= 25:
        return 'green'
    elif 25 < t <= 30:
        return 'yellow'
    else:
        return 'red'

# Create two tabs for the different views
tab1, tab2 = st.tabs(["🗺️ Map View (By Date)", "📈 Trend View (By Region)"])

with tab1:
    st.header("Daily Weather Map")
    col1, col2 = st.columns([2, 1])

    with col1:
        # Get unique dates for the dropdown
        dates = sorted(df['Date'].unique())
        selected_date = st.selectbox("Select Date for Forecast", dates, key='map_date_select')

        # Filter data by date
        filtered_df = df[df['Date'] == selected_date]

        st.subheader(f"Weather Map for {selected_date}")
        
        # Initialize Folium Map over Taiwan
        m = folium.Map(location=[23.6978, 120.9605], zoom_start=7)
        
        # Add markers
        for _, row in filtered_df.iterrows():
            region = row['Region']
            if region in REGION_COORDS:
                avg_temp = row['Avg_Temperature']
                color = get_color(avg_temp)
                
                popup_html = f"""
                <b>{region}</b><br>
                Avg: {avg_temp:.1f}°C<br>
                Max: {row['Max_Temperature']:.1f}°C<br>
                Min: {row['Min_Temperature']:.1f}°C
                """
                
                folium.CircleMarker(
                    location=REGION_COORDS[region],
                    radius=15,
                    popup=folium.Popup(popup_html, max_width=200),
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.7,
                    tooltip=f"{region} ({avg_temp:.1f}°C)"
                ).add_to(m)
                
        # Render map
        st_folium(m, width=700, height=500)

    with col2:
        st.subheader("Data Highlights")
        st.dataframe(filtered_df, use_container_width=True, hide_index=True)

with tab2:
    st.header("Region Temperature Trend")
    
    # Dropdown for selecting region
    regions = sorted(df['Region'].unique())
    selected_region = st.selectbox("Select Region", regions, key='trend_region_select')
    
    # Explicitly query SQLite database for the selected region
    # Requirement: "必須從 SQLite 資料庫查詢資料" (Must query data from SQLite database)
    if os.path.exists("weather.db"):
        conn = sqlite3.connect("weather.db")
        query = f"SELECT Date, Min_Temperature, Max_Temperature, Avg_Temperature FROM forecast WHERE Region = '{selected_region}' ORDER BY Date"
        region_df = pd.read_sql_query(query, conn)
        conn.close()
    else:
        # Fallback if DB doesn't exist (e.g. testing CSV)
        region_df = df[df['Region'] == selected_region].sort_values('Date')
        region_df = region_df[['Date', 'Min_Temperature', 'Max_Temperature', 'Avg_Temperature']]

    col_chart, col_table = st.columns([2, 1])
    
    with col_chart:
        st.subheader(f"7-Day Temperature Trend for {selected_region}")
        # Prepare data for line chart
        chart_df = region_df.set_index('Date')[['Min_Temperature', 'Max_Temperature', 'Avg_Temperature']]
        st.line_chart(chart_df)
        
    with col_table:
        st.subheader("Forecast Data")
        st.dataframe(region_df, use_container_width=True, hide_index=True)
