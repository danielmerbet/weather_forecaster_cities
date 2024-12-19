import requests
import plotly.graph_objects as go

# Function to fetch weather data from Open-Meteo API
def fetch_weather(region_lat_lon):
    forecasts = []
    for location in region_lat_lon:
        lat, lon, name = location["lat"], location["lon"], location["name"]
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecasts.append({"name": name, "data": data})
        else:
            print(f"Failed to fetch data for {name}. HTTP Status: {response.status_code}")
    return forecasts

# Function to generate HTML plots for each location
def generate_plots(forecasts):
    plots_html = ""
    for forecast in forecasts:
        name = forecast["name"]
        data = forecast["data"]
        dates = data["daily"]["time"]
        max_temp = data["daily"]["temperature_2m_max"]
        min_temp = data["daily"]["temperature_2m_min"]
        precipitation = data["daily"]["precipitation_sum"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=max_temp, mode='lines+markers', name='Max Temp (°C)', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=dates, y=min_temp, mode='lines+markers', name='Min Temp (°C)', line=dict(color='blue')))
        fig.add_trace(go.Bar(x=dates, y=precipitation, name='Precipitation (mm)', marker_color='rgba(0, 123, 255, 0.5)'))

        fig.update_layout(
            title=f"Weather Forecast for {name}",
            xaxis_title="Date",
            yaxis_title="Temperature (°C) / Precipitation (mm)",
            legend_title="Legend",
            template="plotly_white",
        )
        plots_html += fig.to_html(full_html=False, include_plotlyjs=False)
    return plots_html

# Main function to generate the HTML file
def main():
    # Define the region with locations
    region_lat_lon = [
        {"lat": 41.9794, "lon": 2.8214, "name": "Girona"},
        {"lat": 41.3879, "lon": 2.16992, "name": "Barcelona"},
        {"lat": 9.3046, "lon": -75.3906, "name": "Sincelejo"},
    ]

    # Fetch weather data
    forecasts = fetch_weather(region_lat_lon)

    # Generate plots
    plots_html = generate_plots(forecasts)

    # Render HTML
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Weather Forecast</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h1 {{ color: #333; }}
            .plot {{ margin-bottom: 50px; }}
        </style>
    </head>
    <body>
        <h1>Weather Forecast for Selected Regions</h1>
        <p>This forecast uses data provided by the <a href="https://open-meteo.com/" target="_blank">Open-Meteo API</a>. Below are the weather forecasts for the upcoming days for each selected location:</p>
        {plots_html}
    </body>
    </html>
    """

    with open("index.html", "w") as file:
        file.write(html_template)

if __name__ == "__main__":
    main()
