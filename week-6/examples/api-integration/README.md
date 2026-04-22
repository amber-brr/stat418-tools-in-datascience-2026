# API Integration Example

## Overview

This example demonstrates how to integrate external APIs into your Streamlit applications. You'll learn to make API calls, handle responses, display results, and manage errors.

## What You'll Learn

- Making API requests from Streamlit
- Handling API responses and errors
- Displaying API data
- Managing API keys securely
- Implementing retry logic
- Caching API responses

## Example: Weather Dashboard

We'll build a weather dashboard that fetches data from a weather API and displays it interactively.

## Complete API Integration Code

```python
import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# Page config
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Title
st.title("🌤️ Weather Dashboard")
st.markdown("Real-time weather data from OpenWeatherMap API")

# API Configuration
# In production, use st.secrets
API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "demo_key")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Helper functions
@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_weather(city):
    """Fetch current weather for a city"""
    try:
        url = f"{BASE_URL}/weather"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.Timeout:
        st.error("Request timed out. Please try again.")
        return None
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            st.error(f"City '{city}' not found.")
        elif response.status_code == 401:
            st.error("Invalid API key.")
        else:
            st.error(f"HTTP Error: {e}")
        return None
    except Exception as e:
        st.error(f"Error fetching weather: {str(e)}")
        return None

@st.cache_data(ttl=600)
def get_forecast(city):
    """Fetch 5-day forecast for a city"""
    try:
        url = f"{BASE_URL}/forecast"
        params = {
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except Exception as e:
        st.error(f"Error fetching forecast: {str(e)}")
        return None

def display_current_weather(data):
    """Display current weather information"""
    if not data:
        return
    
    # Extract data
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description'].title()
    icon = data['weather'][0]['icon']
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Temperature",
            value=f"{temp:.1f}°C",
            delta=f"Feels like {feels_like:.1f}°C"
        )
    
    with col2:
        st.metric(
            label="Humidity",
            value=f"{humidity}%"
        )
    
    with col3:
        st.metric(
            label="Wind Speed",
            value=f"{wind_speed} m/s"
        )
    
    with col4:
        st.metric(
            label="Pressure",
            value=f"{pressure} hPa"
        )
    
    # Weather description with icon
    st.markdown(f"### {description}")
    st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png")

def display_forecast(data):
    """Display forecast chart"""
    if not data:
        return
    
    # Extract forecast data
    forecasts = data['list']
    
    # Prepare data for plotting
    times = []
    temps = []
    
    for forecast in forecasts[:40]:  # 5 days, 8 readings per day
        times.append(datetime.fromtimestamp(forecast['dt']))
        temps.append(forecast['main']['temp'])
    
    # Create DataFrame
    df = pd.DataFrame({
        'Time': times,
        'Temperature': temps
    })
    
    # Create plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Time'],
        y=df['Temperature'],
        mode='lines+markers',
        name='Temperature',
        line=dict(color='#FF4B4B', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="5-Day Temperature Forecast",
        xaxis_title="Date/Time",
        yaxis_title="Temperature (°C)",
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Sidebar
st.sidebar.header("Settings")

# City input
city = st.sidebar.text_input(
    "Enter City Name",
    value="London",
    help="Enter a city name to get weather data"
)

# Refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh (every 10 min)")

if auto_refresh:
    st.sidebar.info("Data will refresh automatically")

# Main content
if city:
    with st.spinner(f"Fetching weather data for {city}..."):
        # Get current weather
        weather_data = get_weather(city)
        
        if weather_data:
            st.subheader(f"Current Weather in {city}")
            display_current_weather(weather_data)
            
            st.markdown("---")
            
            # Get forecast
            forecast_data = get_forecast(city)
            if forecast_data:
                st.subheader("5-Day Forecast")
                display_forecast(forecast_data)
            
            # Display raw data in expander
            with st.expander("📊 View Raw API Response"):
                st.json(weather_data)

# Multiple cities comparison
st.markdown("---")
st.subheader("Compare Multiple Cities")

cities_to_compare = st.multiselect(
    "Select cities to compare",
    options=["London", "New York", "Tokyo", "Paris", "Sydney", "Mumbai"],
    default=["London", "New York"]
)

if cities_to_compare:
    comparison_data = []
    
    for city in cities_to_compare:
        data = get_weather(city)
        if data:
            comparison_data.append({
                'City': city,
                'Temperature': data['main']['temp'],
                'Humidity': data['main']['humidity'],
                'Wind Speed': data['wind']['speed']
            })
    
    if comparison_data:
        df_comparison = pd.DataFrame(comparison_data)
        
        # Display comparison table
        st.dataframe(df_comparison, use_container_width=True)
        
        # Comparison charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig_temp = go.Figure(data=[
                go.Bar(x=df_comparison['City'], y=df_comparison['Temperature'])
            ])
            fig_temp.update_layout(
                title="Temperature Comparison",
                yaxis_title="Temperature (°C)",
                height=300
            )
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col2:
            fig_humidity = go.Figure(data=[
                go.Bar(x=df_comparison['City'], y=df_comparison['Humidity'])
            ])
            fig_humidity.update_layout(
                title="Humidity Comparison",
                yaxis_title="Humidity (%)",
                height=300
            )
            st.plotly_chart(fig_humidity, use_container_width=True)

# API information
with st.expander("ℹ️ About the API"):
    st.markdown("""
    **API Provider:** OpenWeatherMap
    
    **Endpoints Used:**
    - Current Weather: `/weather`
    - 5-Day Forecast: `/forecast`
    
    **Rate Limits:**
    - Free tier: 60 calls/minute
    - 1,000,000 calls/month
    
    **Data Refresh:**
    - Current weather: Every 10 minutes
    - Forecast: Every 3 hours
    
    **Get Your API Key:**
    Visit [OpenWeatherMap](https://openweathermap.org/api) to get a free API key.
    """)

# Footer
st.markdown("---")
st.markdown(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
```

## Key Concepts

### 1. Making API Requests

```python
import requests

# GET request
response = requests.get(url, params=params, headers=headers)

# POST request
response = requests.post(url, json=data, headers=headers)

# Check status
if response.status_code == 200:
    data = response.json()
```

### 2. Error Handling

```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raises HTTPError for bad status
    data = response.json()
except requests.exceptions.Timeout:
    st.error("Request timed out")
except requests.exceptions.HTTPError as e:
    st.error(f"HTTP Error: {e}")
except requests.exceptions.RequestException as e:
    st.error(f"Error: {e}")
```

### 3. Caching API Responses

```python
@st.cache_data(ttl=600)  # Cache for 10 minutes
def fetch_data(param):
    response = requests.get(url, params={'q': param})
    return response.json()
```

### 4. Managing API Keys

**Using Streamlit Secrets:**
```python
# .streamlit/secrets.toml
API_KEY = "your-api-key-here"

# In code
api_key = st.secrets["API_KEY"]
```

**Using Environment Variables:**
```python
import os
api_key = os.getenv("API_KEY")
```

### 5. Retry Logic

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# Use it
response = requests_retry_session().get(url)
```

## Common API Integration Patterns

### Pattern 1: Search and Display

```python
query = st.text_input("Search")
if query:
    results = search_api(query)
    for result in results:
        st.write(result)
```

### Pattern 2: Form Submission

```python
with st.form("api_form"):
    param1 = st.text_input("Parameter 1")
    param2 = st.number_input("Parameter 2")
    submitted = st.form_submit_button("Submit")
    
    if submitted:
        result = call_api(param1, param2)
        st.write(result)
```

### Pattern 3: Real-time Updates

```python
placeholder = st.empty()

while True:
    data = fetch_latest_data()
    with placeholder.container():
        st.write(data)
    time.sleep(60)  # Update every minute
```

### Pattern 4: Pagination

```python
page = st.number_input("Page", min_value=1, value=1)
results = fetch_page(page)
st.write(results)

col1, col2 = st.columns(2)
if col1.button("Previous") and page > 1:
    st.rerun()
if col2.button("Next"):
    st.rerun()
```

## Best Practices

1. **Always use timeouts**: Prevent hanging requests
2. **Cache responses**: Reduce API calls and improve performance
3. **Handle errors gracefully**: Provide helpful error messages
4. **Respect rate limits**: Implement backoff and retry logic
5. **Secure API keys**: Never commit keys to version control
6. **Validate inputs**: Check user inputs before making API calls
7. **Show loading states**: Use spinners for better UX
8. **Log API calls**: Track usage and debug issues

## Deployment Considerations

### Streamlit Cloud

Add secrets in dashboard:
```toml
API_KEY = "your-key"
```

### Google Cloud Run

Set environment variables:
```bash
gcloud run services update app \
    --set-env-vars="API_KEY=your-key"
```

### Docker

Use environment variables:
```dockerfile
ENV API_KEY=${API_KEY}
```

## Common Issues

### Issue: CORS errors
**Solution**: Make requests from backend, not frontend

### Issue: Rate limiting
**Solution**: Implement caching and request throttling

### Issue: Slow responses
**Solution**: Use async requests or background tasks

### Issue: API key exposure
**Solution**: Use secrets management, never hardcode

## Next Steps

- Implement authentication flows (OAuth)
- Add webhook support
- Create API monitoring dashboard
- Implement request queuing
- Add response validation

## Resources

- [Requests Documentation](https://requests.readthedocs.io/)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
- [API Design Best Practices](https://swagger.io/resources/articles/best-practices-in-api-design/)
