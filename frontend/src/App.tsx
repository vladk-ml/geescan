import React from 'react';
import { MapContainer, TileLayer, FeatureGroup } from 'react-leaflet';
import L from 'leaflet';
import { Box, AppBar, Toolbar, Typography, Container } from '@mui/material';
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw';
import 'leaflet-draw/dist/leaflet.draw.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// Fix Leaflet's default icon issue
let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

function App() {
  const position: [number, number] = [51.505, -0.09];
  const mapRef = React.useRef<L.Map | null>(null);
  const drawnItemsRef = React.useRef<L.FeatureGroup | null>(null);

  const handleCreated = (e: any) => {
    const layer = e.layer;
    console.log('New AOI created:', layer.toGeoJSON());
  };

  React.useEffect(() => {
    if (!mapRef.current) {
      const map = L.map('map').setView(position, 13);
      mapRef.current = map;

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);

      // Initialize FeatureGroup for the draw control
      const drawnItems = new L.FeatureGroup();
      drawnItemsRef.current = drawnItems;
      map.addLayer(drawnItems);

      // Initialize draw control
      const drawControl = new (L.Control as any).Draw({
        position: 'topright',
        draw: {
          marker: false,
          circle: false,
          circlemarker: false,
          polyline: false,
          polygon: {
            allowIntersection: false,
            showArea: true,
            drawError: {
              color: '#e1e100',
              message: '<strong>Oh snap!<strong> you can\'t draw that!'
            },
            shapeOptions: {
              color: '#3388ff'
            }
          },
          rectangle: {
            shapeOptions: {
              color: '#3388ff'
            }
          }
        },
        edit: {
          featureGroup: drawnItems,
          remove: true
        }
      });

      map.addControl(drawControl);

      // Handle created features
      map.on(L.Draw.Event.CREATED, (e: any) => {
        const layer = e.layer;
        drawnItems.addLayer(layer);
        handleCreated(e);
      });
    }

    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            GEEScan - SAR Data Monitor
          </Typography>
        </Toolbar>
      </AppBar>
      <Container maxWidth="xl" sx={{ mt: 2 }}>
        <Box sx={{ height: 'calc(100vh - 100px)', width: '100%' }}>
          <div id="map" style={{ height: '100%', width: '100%' }} />
        </Box>
      </Container>
    </Box>
  );
}

export default App;
