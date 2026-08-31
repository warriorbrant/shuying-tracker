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

// Small triangle marker + name tooltip for a named mountain peak, and a thin
// line for a named river's real course (possibly several disjoint OSM way
// segments, since long rivers are often split into more than one). Shared by
// the draw/edit page (live preview while resolving) and the view page
// (showing what got saved) so both look identical.
function addMountainMarker(map, m) {
  var icon = L.divIcon({
    className: "route-mountain-icon",
    html: "▲",
    iconSize: [18, 18],
    iconAnchor: [9, 9],
  });
  return L.marker([m.lat, m.lng], { icon: icon }).bindTooltip(m.name, { permanent: false }).addTo(map);
}

function addRiverLines(map, river) {
  var layers = [];
  (river.segments || []).forEach(function (seg) {
    if (seg.length < 2) return;
    var latlngs = seg.map(function (p) { return [p.lat, p.lng]; });
    layers.push(
      L.polyline(latlngs, { color: "#4a7a94", weight: 3, opacity: 0.85 })
        .bindTooltip(river.name, { permanent: false })
        .addTo(map)
    );
  });
  return layers;
}

// Bounding box (padded outward, with a floor so a tiny or single-point route
// doesn't collapse to a near-zero box) around a set of {lat,lng} points --
// used to scope the river lookup to roughly the route's own area, and to
// bias the mountain lookup toward it, so a common place name doesn't return
// a result from the wrong side of the world.
function routeBoundsWithMargin(points, marginRatio, minMarginDeg) {
  var lats = points.map(function (p) { return p.lat; });
  var lngs = points.map(function (p) { return p.lng; });
  var latMin = Math.min.apply(null, lats), latMax = Math.max.apply(null, lats);
  var lngMin = Math.min.apply(null, lngs), lngMax = Math.max.apply(null, lngs);
  var latPad = Math.max((latMax - latMin) * marginRatio, minMarginDeg);
  var lngPad = Math.max((lngMax - lngMin) * marginRatio, minMarginDeg);
  return { south: latMin - latPad, west: lngMin - lngPad, north: latMax + latPad, east: lngMax + lngPad };
}
