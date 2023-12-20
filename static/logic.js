const base_url = window.location.origin + window.location.pathname + "search?address=";

function submitForm() {
    let query_url = base_url + address.value;
    d3.json(query_url).then(data => {
        showMap(data);
    })
}

function showMap(data) {
    let streetmap = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    });

    let center_lat = data['center']['lat'];
    let center_lon = data['center']['lon'];

    let container = L.DomUtil.get("map");
    if (container != null) {
        container._leaflet_id = null;
    }
    
    let map = L.map("map", {
        center: [center_lat, center_lon],
        zoom: 17,
        layers: [streetmap]
    });

    let marker = L.marker([center_lat, center_lon], {
        draggable: false,
        title: "My Location"
    }).addTo(map);

    let redIcon = new L.Icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
      });

    data['locations'].forEach(location => {
        let lat = location['lat'];
        let lon = location['lon']
        L.marker([lat, lon], {
            draggable: false,
            title: `Capacity: ${location['capacity']}`,
            icon: redIcon
        }).addTo(map);
    })
}
