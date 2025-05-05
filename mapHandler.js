// Initialize the map and set its view to Helsinki
const map = L.map("map").setView([60.1699, 24.9384], 13);

// Add the OpenStreetMap tile layer
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
}).addTo(map);

// Example: Add a marker
const marker = L.marker([60.1699, 24.9384])
  .addTo(map)
  .bindPopup("Welcome to your game map!")
  .openPopup();
