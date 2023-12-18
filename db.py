import os
import psycopg2
from dotenv import load_dotenv
import requests


CITIBIKES_URL = "https://gbfs.citibikenyc.com/gbfs/en/station_information.json"
GEOCODE_URL = "https://geocode.maps.co/search"
REVERSE_URL = "https://geocode.maps.co/reverse"


def load_database():
    result = requests.get(CITIBIKES_URL)
    if result.status_code != 200:
        raise Exception(f"HTTP error returned {result}")
        return
    data = result.json()

    load_dotenv()
    db_url = os.environ.get("DATABSE_URL")
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    with open('schema.sql', 'r') as FILE:
        query = FILE.read()
    queries = query.split(";")
    for q in queries[:-1]:
        cursor.execute(q)
    connection.commit()

    q = f'''INSERT INTO bike_stations (capacity, lat, lon) 
                    VALUES '''
    updates = []
    for station in data['data']['stations']:
        capacity = station['capacity']
        if capacity > 0:
            updates.append (f"({capacity}, {station['lat']}, {station['lon']})")
    q += ','.join(updates)
    q += ';'
    cursor.execute(q)
    connection.commit()

    cursor.close()
    connection.close()
            

def search(address, k=5):
    result = requests.get(GEOCODE_URL, {'q': address + ', new York, NY'})
    data = result.json()
    lat = float(data[0]['lat'])
    lon = float(data[0]['lon'])

    load_dotenv()
    db_url = os.environ.get("DATABSE_URL")
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM bike_stations")
    data = cursor.fetchall()
    cursor.close()
    connection.close()

    distances = []
    for row in data:
        distance = manhattanDistance(lat, lon, row[2], row[3])
        distances.append((distance, row[1], row[2], row[3]))
    distances.sort(key=lambda x: x[0])
    return (lat, lon), distances[:k]


def manhattanDistance(lat1, lon1, lat2, lon2):
    distance = abs(lat1 - lat2) + abs(lon1 - lon2)
    return distance
