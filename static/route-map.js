// Shared base-layer setup for both the draw-a-route page and the
// view-a-route page -- adds the standard OSM street tiles (default) plus
// an OpenTopoMap terrain layer, with Leaflet's built-in layer-switcher
// control to toggle between them. Neither tile source needs an API key.
function addRouteBaseLayers(map, labels) {
  var standard = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; OpenStreetMap contributors'
  });
  var terrain = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    maxZoom: 17,
    attribution: 'Map data: &copy; OpenStreetMap contributors, SRTM | Map style: &copy; OpenTopoMap (CC-BY-SA)'
  });
  standard.addTo(map);
  var baseLayers = {};
  baseLayers[labels.standard] = standard;
  baseLayers[labels.terrain] = terrain;
  L.control.layers(baseLayers).addTo(map);
}
