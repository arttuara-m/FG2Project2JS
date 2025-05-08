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
    //if (data.length <= 2){
    //    for (const item of data[0]) {
    //        console.log('Airport found: '+item[1])
    //    }}
}

function updateCoords(newcoordsX,newcoordsY){
    coords[0] = newcoordsX
    coords[1] = newcoordsY
}

function addAirportMarkers(){
    for (let i=0;i<listOfAirports;i++){
        L.marker([airportLong,airportLat])
        .addTo(map)
    }
}

//################   vvvvvvv   mitä tekee hän? vvvvv   #######################3
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

/*
var choicePopUp = L.popup();
var container = L.DomUtil.create('div');
chooseBtn = this.createButton('Choose airport', container);
div.innerHTML = ''+chooseBtn
L.DomEvent.on(destBtn, 'click', () => {
  alert("Airport chosen");
});
*/