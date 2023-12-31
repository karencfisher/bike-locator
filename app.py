from flask import Flask, request, jsonify
from db import load_database, search


loaded = False
app = Flask(__name__)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/search')
def getStations():
    global loaded
    if not loaded:
        load_database()
        loaded = True
    results = search(request.args.get('address'))
    results_json = {'center': {'lat': results[0][0], 'lon': results[0][1]}}
    locations = []
    for result in results[1]:
        location = {'capacity': result[1],
                    'lat': result[2],
                    'lon': result[3]}
        locations.append(location)
    results_json['locations'] = locations
    return jsonify(results_json)


if __name__ == "__main__":
    app.run(debug=True)
