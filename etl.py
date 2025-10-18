import requests
import psycopg2
from datetime import datetime

cities = {
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "Chicago": (41.8781, -87.6298),
    "Houston": (29.7604, -95.3698),
    "Miami": (25.7617, -80.1918),
    "London": (51.5074, -0.1278),
    "Paris": (48.8566, 2.3522),
    "Berlin": (52.5200, 13.4050),
    "Tokyo": (35.6895, 139.6917),
    "Osaka": (34.6937, 135.5023),
    "Beijing": (39.9042, 116.4074),
    "Shanghai": (31.2304, 121.4737),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Delhi": (28.7041, 77.1025),
    "Sydney": (-33.8688, 151.2093),
    "Melbourne": (-37.8136, 144.9631),
    "Toronto": (43.6532, -79.3832),
    "Vancouver": (49.2827, -123.1207),
    "Moscow": (55.7558, 37.6173),
    "Dubai": (25.2048, 55.2708),
    "Singapore": (1.3521, 103.8198),
    "Johannesburg": (-26.2041, 28.0473),
    "Rio de Janeiro": (-22.9068, -43.1729),
}

DB_NAME = "weather"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"


def run_etl():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cursor = conn.cursor()
    for city, (lat, lon) in cities.items():
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relativehumidity_2m"
        res = requests.get(url).json()

        timestamps = res['hourly']['time']
        temps = res['hourly']['temperature_2m']
        hums = res['hourly'].get('relativehumidity_2m') or [None]*len(timestamps)

        for t, temp, hum in zip(timestamps, temps, hums):
            cursor.execute(
                """
                INSERT INTO weather_raw (city, latitude, longitude, timestamp, temperature, humidity)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (city, lat, lon, datetime.fromisoformat(t), temp, hum)
            )

        print(f"Inserted weather data for {city}")

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    run_etl()
