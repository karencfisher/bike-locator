from flask import Flask, jsonify
from db import load_database, search


loaded = False
app = Flask(__name__)

@app.get('/api/search/<address>')
def getStations(address):
    global loaded
    if not loaded:
        load_database()
        loaded = True
    results = search(address)
    results_json = {'lat': results[0][0], 'lon': results[0][1]}
    locations = []
    for result in results[1]:
        location = {'capacity': result[1],
                    'lat': result[2],
                    'lon': result[3]}
        locations.append(location)
    results_json['locations'] = locations
    return jsonify(results_json)


if __name__ == "__main__":
    app.run()
