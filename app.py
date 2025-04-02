import streamlit as st
import requests
import plotly.graph_objects as go
import os
from dotenv import load_dotenv
from datetime import datetime

# Set page configuration first - this must be the first Streamlit command
st.set_page_config(
    page_title=" Live Weather Dashboard ", 
    page_icon="🌦️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load API Key from .env file
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Define background images for different weather conditions
WEATHER_BACKGROUNDS = {
    'Clear': "https://images.unsplash.com/photo-1470252649378-9c29740c9fa8?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
    'Clouds': "https://images.unsplash.com/photo-1534088568595-a066f410bcda?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2071&q=80",
    'Rain': "https://images.unsplash.com/photo-1519692933481-e162a57d6721?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
    'Drizzle': "https://images.unsplash.com/photo-1508873699372-7aeab60b44ab?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
    'Thunderstorm': "https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2071&q=80",
    'Snow': "https://images.unsplash.com/photo-1491002052546-bf38f186af56?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2083&q=80",
    'Mist': "https://images.unsplash.com/photo-1543968996-ee822b8176ba?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
    'Fog': "https://images.unsplash.com/photo-1487621167305-5d248087c724?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2072&q=80",
    'Haze': "https://images.unsplash.com/photo-1533757704860-f673d3e1bc57?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2070&q=80",
    'Dust': "https://images.unsplash.com/photo-1584036561566-baf8f5f1b144?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2072&q=80",
    'default': "https://images.unsplash.com/photo-1429734956993-8a9b0555e122?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2079&q=80"
}

# Function to get background URL for weather condition
def get_weather_background(condition):
    for key in WEATHER_BACKGROUNDS:
        if key in condition:
            return WEATHER_BACKGROUNDS[key]
    return WEATHER_BACKGROUNDS['default']

# Apply the CSS to remove whitespace and style the dashboard
st.markdown(
    """
    <style>
  
    
    /* Remove top margin from main app */
    .main > div:first-child {
        margin-top: 0 !important;
        padding-top: 0 !important;
    }
    
    /* Remove default Streamlit margins and padding */
    div.stButton > button {
        margin-top: 0;
    }
    
    /* Remove extra padding from text inputs */
    div.stTextInput > div {
        padding-top: 0;
        padding-bottom: 0;
    }
    
    /* Modify header styling */
  .main-header {
    color: white !important;
    font-size: 5rem;
    text-align: center !important;
    text-shadow: 2px 2px 6px rgba(0, 0, 0, 0.8) !important;
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
    padding: 15px;
    font-weight: 900;
    border-radius: 12px;
    border-bottom: 3px solid rgba(255, 255, 255, 0.3);
}

    
    .metric-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #1E88E5;
    }
    
    .metric-label {
        font-size: 2rem;
        color: #333;
        font-weight: 800;
    }
    
    
    /* Style for forecast cards */
    .forecast-card {
        transition: transform 0.3s;
    }
    
    .forecast-card:hover {
        transform: scale(1.05);
    }
    
    /* Text and heading colors */
    h1, h2, h3, h4 {
        color: #1E4B88;
        font-size: 1.6rem !important;
        text-shadow: 1px 1px 1px rgba(255, 255, 255, 0.7);
    }
    
    /* Improved paragraph text */
    p {
        color: #333 !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
    }
    
    /* Make regular text more visible */
    div.markdown-text-container {
        color: #333 !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        background-color: rgba(255, 255, 255, 0.5);
        padding: 3px 5px;
        border-radius: 3px;
    }
    
    /* Bold text enhancement */
    strong {
        color: #1E4B88 !important;
        font-weight: 700 !important;
    }
    
    .weather-status {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1E4B88;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.7);
        background-color: rgba(255, 255, 255, 0.5);
        padding: 5px 10px;
        border-radius: 5px;
        display: inline-block;
    }
    
    /* Date display styling */
    .date-display {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 8px 12px;
        border-radius: 5px;
        font-size: 1.1rem;
        font-weight: 500;
        color: #1E4B88;
        display: inline-block;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Styling for all Streamlit metric components */
    .stMetric {
        background-color: rgba(255, 255, 255, 0.6);
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    
    /* Fix Streamlit metrics display */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        font-weight: bold !important;
        color: #1E4B88 !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #FFFFFF !important;
    }
    
    /* Info block styling */
    div[data-testid="stInfo"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        color: #333 !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
    }
    
    /* Error block styling */
    div[data-testid="stError"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        color: #D32F2F !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
    }
    
    /* Section headings styling */
    .section-heading {
        font-size: 1.8rem !important;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.3));
        padding: 10px 15px;
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 15px;
        border-left: 4px solid #1E4B88;
        color: #1E4B88;
        text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.7);
    }
    
    /* Remove unwanted empty white bars */
    .css-18e3th9 {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    .css-1d391kg {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    
    /* Weather text info styling */
    .weather-info-text {
        background-color: rgba(255, 255, 255, 0.5);
        padding: 8px;
        border-radius: 5px;
        margin-top: 10px;
    }
    
    /* Background image setup */
    .stApp {
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to set background image
def set_background(background_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{background_url}");
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Function to fetch weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to fetch 5-day forecast
def get_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Create a color map for weather conditions
def get_condition_color(condition):
    color_map = {
        'Clear': '#FFC107',  # Yellow
        'Clouds': '#90A4AE',  # Blue Grey
        'Rain': '#2196F3',   # Blue
        'Drizzle': '#64B5F6', # Light Blue
        'Thunderstorm': '#5C6BC0', # Indigo
        'Snow': '#E1F5FE',   # Light Blue lighten
        'Mist': '#B0BEC5',   # Blue Grey lighten
        'Fog': '#CFD8DC',    # Blue Grey lighten
        'Haze': '#ECEFF1',   # Blue Grey lighten
    }
    for key in color_map:
        if key in condition:
            return color_map[key]
    return '#78909C'  # Default Blue Grey

# Function to get weather icon URLs
def get_weather_icon(icon_code):
    return f"http://openweathermap.org/img/wn/{icon_code}@4x.png"

# Set default background
set_background(WEATHER_BACKGROUNDS['default'])

# Header with improved styling
st.markdown('<div style="background: linear-gradient(135deg, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.4)); padding: 10px; border-radius: 12px; margin-bottom: 0.5rem; border-bottom: 3px solid rgba(255, 255, 255, 0.3);"><h1 class="main-header">🌦️ Live Weather Dashboard</h1></div>', unsafe_allow_html=True)

# Search box with lighter background
st.markdown('<div class="search-bar">', unsafe_allow_html=True)
col1, col2 = st.columns([4, 1])
with col1:
    city = st.text_input("", placeholder="Enter city name...", value="Sangli", label_visibility="collapsed")
with col2:
    search_button = st.button("Get Weather", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Main dashboard container with lighter background
st.markdown('<div class="weather-container">', unsafe_allow_html=True)

if search_button or city:
    weather_data = get_weather(city)
    forecast_data = get_forecast(city)
    
    if weather_data and forecast_data:
        # Get weather condition and set background
        weather_condition = weather_data['weather'][0]['main']
        bg_url = get_weather_background(weather_condition)
        set_background(bg_url)
        
        # Current conditions section with improved heading
        st.markdown(f'<h3 class="section-heading">Current Weather in {city}</h3>', unsafe_allow_html=True)
        current_time = datetime.fromtimestamp(weather_data['dt']).strftime('%A, %b %d, %Y %I:%M %p')
        st.markdown(f'<div class="date-display"><strong>Last Updated</strong>: {current_time}</div>', unsafe_allow_html=True)
        
        # Weather condition with icon
        weather_description = weather_data['weather'][0]['description'].title()
        weather_icon = weather_data['weather'][0]['icon']
        
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(get_weather_icon(weather_icon), width=120)
        with col2:
            st.markdown(f'<div class="weather-status">{weather_condition}: {weather_description}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="weather-info-text">Current conditions in {city} show <strong>{weather_description}</strong>. The dashboard background reflects these conditions.</div>', unsafe_allow_html=True)
        
        # Main metrics in cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{weather_data["main"]["temp"]:.1f}°C</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Temperature</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{weather_data["main"]["humidity"]}%</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Humidity</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{weather_data["wind"]["speed"]:.1f} m/s</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Wind Speed</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            pressure = weather_data["main"]["pressure"]
            st.markdown(f'<div class="metric-value">{pressure} hPa</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Pressure</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Additional metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # Feels like, min/max temp
            subcolA, subcolB, subcolC = st.columns(3)
            with subcolA:
                st.metric("Feels Like", f"{weather_data['main'].get('feels_like', 'N/A'):.1f}°C")
            with subcolB:
                st.metric("Min Temp", f"{weather_data['main'].get('temp_min', 'N/A'):.1f}°C")
            with subcolC:
                st.metric("Max Temp", f"{weather_data['main'].get('temp_max', 'N/A'):.1f}°C")
            
            # Sunrise/sunset times
            if 'sys' in weather_data:
                sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%I:%M %p')
                sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%I:%M %p')
                
                subcol1, subcol2 = st.columns(2)
                with subcol1:
                    st.metric("Sunrise", sunrise)
                with subcol2:
                    st.metric("Sunset", sunset)
        
        with col2:
            # Visibility and clouds
            if 'visibility' in weather_data:
                visibility_km = weather_data['visibility'] / 1000
                st.metric("Visibility", f"{visibility_km:.1f} km")
            
            if 'clouds' in weather_data:
                st.metric("Cloud Cover", f"{weather_data['clouds']['all']}%")
            
            # Wind direction
            if 'wind' in weather_data and 'deg' in weather_data['wind']:
                wind_deg = weather_data['wind']['deg']
                directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
                direction_index = round(wind_deg / 45)
                st.metric("Wind Direction", f"{wind_deg}° ({directions[direction_index]})")
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # Forecast section with improved heading
        st.markdown('<h3 class="section-heading">24-Hour Temperature Forecast</h3>', unsafe_allow_html=True)
        
        # Process forecast data
        forecast_temps = []
        forecast_times = []
        forecast_conditions = []
        forecast_icons = []
        
        for item in forecast_data['list'][:8]:  # Next 24 hours (8 x 3-hour intervals)
            dt = datetime.fromtimestamp(item['dt'])
            forecast_times.append(dt.strftime('%I %p'))
            forecast_temps.append(item['main']['temp'])
            forecast_conditions.append(item['weather'][0]['main'])
            forecast_icons.append(item['weather'][0]['icon'])
        
        # Temperature chart with improved styling
        fig = go.Figure()
        
        # Add temperature line
        fig.add_trace(go.Scatter(
            x=forecast_times,
            y=forecast_temps,
            mode="lines+markers",
            name="Temperature",
            line=dict(width=4, color='#1E88E5'),
            marker=dict(size=10, color='#1E88E5'),
        ))
        
        # Customize layout
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Temperature (°C)",
            template="plotly_white",
            height=400,
            margin=dict(l=20, r=20, t=20, b=20),
            hovermode="x unified",
            plot_bgcolor="rgba(255,255,255,0.5)",
            paper_bgcolor="rgba(255,255,255,0.0)",
            font=dict(
                family="Arial, sans-serif",
                size=16,
                color="#333333"
            ),
            # Make axis titles larger and bolder
            xaxis=dict(
                title_font=dict(size=18, color="#1E4B88", family="Arial, sans-serif"),
                tickfont=dict(size=14, color="#333333"),
                title_standoff=25
            ),
            yaxis=dict(
                title_font=dict(size=18, color="#1E4B88", family="Arial, sans-serif"),
                tickfont=dict(size=14, color="#333333"),
                title_standoff=25
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Daily forecast cards with improved heading
        st.markdown('<h3 class="section-heading">5-Day Forecast</h3>', unsafe_allow_html=True)
        
        # Get daily forecast (taking data at noon for each day)
        daily_forecast = []
        days_processed = set()
        
        for item in forecast_data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            day = dt.date()
            hour = dt.hour
            
            # Take data for around noon each day (closest to 12:00)
            if day not in days_processed and abs(hour - 12) <= 3:  # Within 3 hours of noon
                daily_forecast.append({
                    'day': dt.strftime('%a'),
                    'date': dt.strftime('%b %d'),
                    'temp': item['main']['temp'],
                    'condition': item['weather'][0]['main'],
                    'description': item['weather'][0]['description'],
                    'icon': item['weather'][0]['icon']
                })
                days_processed.add(day)
            
            if len(daily_forecast) >= 5:  # Limit to 5 days
                break
        
        # Create forecast cards
        cols = st.columns(min(5, len(daily_forecast)))
        for i, day_data in enumerate(daily_forecast):
            with cols[i]:
                st.markdown(f"""
                <div class="forecast-card" style="text-align: center; padding: 15px; background-color: {get_condition_color(day_data['condition'])}; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h4 style="color: white; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5); font-size: 1.2rem; margin: 5px 0;">{day_data['day']}</h4>
                    <p style="color: white; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5); margin: 5px 0;">{day_data['date']}</p>
                    <img src="{get_weather_icon(day_data['icon'])}" width="70">
                    <h3 style="color: white; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5); font-size: 1.5rem; margin: 5px 0;">{day_data['temp']:.1f}°C</h3>
                    <p style="color: white; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5); margin: 5px 0;">{day_data['description'].title()}</p>
                </div>
                """, unsafe_allow_html=True)
        
    else:
        st.error("City not found. Please enter a valid city name.")
else:
    st.info("Enter a city name and click 'Get Weather' to see the forecast. The background will change based on current weather conditions.")

st.markdown('</div>', unsafe_allow_html=True)