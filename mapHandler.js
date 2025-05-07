let coords = [0,0]
let listOfAirports = []

async function mapUpdater(){
    const response = await fetch(`http://127.0.0.1:3000/updatemap`);
    const data = await response.json();
    console.log("mapUpdater: new coordinates; "+data)
    updateCoords(data[0], data[1])
}
async function fetchAirportsInRange(){
    const response = await fetch(`http://127.0.0.1:3000/availableairports`)
    const data = await response.json()
    console.log("fetchAirportsInRange: found;"+data)
    for (let i=0;i<data.length;i++){
        //########## how'd'ya handle jsons with multiple sections again? ########################3
        listOfAirports.push(data.array[i] )
    }
}

function updateCoords(newcoordsX,newcoordsY){
    coords[0] = newcoordsX
    coords[1] = newcoordsY
}

function addAirportMarker(airportLat, airportLong, ICAO, name){
    L.marker([airportLong,airportLat])
        .addTo(map)
        .popupmenu()
}


//let jsHTMLtest = document.getElementById("showcountry").innerText
//console.log(jsHTMLtest)
let map = L.map("map", {
    zoomControl: false
}).setView(coords, 13);

// Add the OpenStreetMap laatta kerros
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 5,
    minZoom: 5,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

//Add a marker
const playerPositionMarker = L.marker(coords)
    .addTo(map)
    .bindPopup("You are currently at: "+coords);