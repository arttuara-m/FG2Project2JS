let coords = [0,0]

let map = L.map("map", {
    zoomControl: false
}).setView(coords, 13);

// Add the OpenStreetMap laatta kerros
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 5,
    minZoom: 5,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

//Add a player marker
const playerPositionMarker = L.marker(coords)
    .addTo(map)
    .bindPopup("You are currently at: "+coords);

async function mapUpdater(){
    const response = await fetch(`http://127.0.0.1:3000/updatemap`);
    const data = await response.json();
    console.log("mapUpdater: new coordinates; "+data)
    updateCoords(data[0], data[1])
}


function updateCoords(newcoordsX,newcoordsY){
    coords[0] = newcoordsX
    coords[1] = newcoordsY
}

function addAirportMarkers(data){
    if (data.length <= 2){
        for (const item of data[1]) {
            airportCoords = [ parseFloat(item[2]) ,parseFloat(item[3])]
            console.log('addAirportMarker: data recieved for '+item[0]+
                '\n at coordinates: '+airportCoords)
            const newAirport = L.marker(airportCoords)
                .addTo(map).bindPopup(item[0]+' '+item[1]);
        }}
}

//################   vvvvvvv   mitä tekee hän? vvvvv   ################
//let jsHTMLtest = document.getElementById("showcountry").innerText
//console.log(jsHTMLtest)

/*
var choicePopUp = L.popup();
var container = L.DomUtil.create('div');
chooseBtn = this.createButton('Choose airport', container);
div.innerHTML = ''+chooseBtn
L.DomEvent.on(destBtn, 'click', () => {
  alert("Airport chosen");
});
*/