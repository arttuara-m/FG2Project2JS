// Initialize the map and set its view to Helsinki
let coords = [60.1699, 24.9384]
const map = L.map("map").setView(coords, 13);

// Add the OpenStreetMap tile layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

// Example: Add a marker
const marker = L.marker(coords)
  .addTo(map)
  .bindPopup("Welcome to your game map!")
  .openPopup();