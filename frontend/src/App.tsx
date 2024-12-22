import React from 'react';
import { MapContainer, TileLayer, FeatureGroup } from 'react-leaflet';
import L from 'leaflet';
import * as turf from '@turf/turf';
import { 
  Box, 
  AppBar, 
  Toolbar, 
  Typography, 
  Container,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  IconButton,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Snackbar,
  Alert,
  Divider
} from '@mui/material';
import {
  Menu as MenuIcon,
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Save as SaveIcon,
  Refresh as RefreshIcon,
  Map as MapIcon
} from '@mui/icons-material';

// Import Leaflet CSS
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

// Import Leaflet Draw
import 'leaflet-draw';

// Fix Leaflet's default icon issue
let DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

interface AOI {
  id?: number;
  name: string;
  description: string;
  geometry: GeoJSON.Feature;
  area?: number;
  center?: [number, number];
  createdAt?: string;
  updatedAt?: string;
}

function App() {
  const position: [number, number] = [51.505, -0.09];
  const mapRef = React.useRef<L.Map | null>(null);
  const drawnItemsRef = React.useRef<L.FeatureGroup | null>(null);
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [snackbarOpen, setSnackbarOpen] = React.useState(false);
  const [snackbarMessage, setSnackbarMessage] = React.useState('');
  const [snackbarSeverity, setSnackbarSeverity] = React.useState<'success' | 'error'>('success');
  const [currentAOI, setCurrentAOI] = React.useState<AOI | null>(null);
  const [aois, setAOIs] = React.useState<AOI[]>([]);
  const [aoiName, setAOIName] = React.useState('');
  const [aoiDescription, setAOIDescription] = React.useState('');

  const calculateAOIMetrics = (geojson: GeoJSON.Feature): { area: number; center: [number, number] } => {
    const area = turf.area(geojson);
    const center = turf.center(geojson);
    return {
      area: Math.round((area / 1000000) * 100) / 100, // Convert to km² and round to 2 decimal places
      center: [
        Math.round(center.geometry.coordinates[0] * 1000000) / 1000000,
        Math.round(center.geometry.coordinates[1] * 1000000) / 1000000
      ]
    };
  };

  const handleCreated = (e: any) => {
    const layer = e.layer;
    const geojson = layer.toGeoJSON();
    const metrics = calculateAOIMetrics(geojson);
    console.log('New AOI created:', geojson);
    setCurrentAOI({
      name: '',
      description: '',
      geometry: geojson,
      area: metrics.area,
      center: metrics.center
    });
    setDialogOpen(true);
  };

  const handleSaveAOI = () => {
    if (currentAOI && aoiName) {
      const newAOI: AOI = {
        ...currentAOI,
        name: aoiName,
        description: aoiDescription,
        createdAt: new Date().toISOString()
      };
      setAOIs([...aois, newAOI]);
      setSnackbarMessage('AOI saved successfully');
      setSnackbarSeverity('success');
      setSnackbarOpen(true);
      setDialogOpen(false);
      setAOIName('');
      setAOIDescription('');
      setCurrentAOI(null);
    }
  };

  const handleDeleteAOI = (aoi: AOI) => {
    setAOIs(aois.filter(a => a !== aoi));
    setSnackbarMessage('AOI deleted successfully');
    setSnackbarSeverity('success');
    setSnackbarOpen(true);
    if (drawnItemsRef.current) {
      drawnItemsRef.current.clearLayers();
    }
  };

  const handleViewAOI = (aoi: AOI) => {
    if (mapRef.current && drawnItemsRef.current) {
      drawnItemsRef.current.clearLayers();
      const layer = L.geoJSON(aoi.geometry);
      drawnItemsRef.current.addLayer(layer);
      const bounds = layer.getBounds();
      mapRef.current.fitBounds(bounds);
    }
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
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={() => setDrawerOpen(true)}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            GEEScan - SAR Data Monitor
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        anchor="left"
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
      >
        <Box sx={{ width: 350 }} role="presentation">
          <List>
            <ListItem>
              <Typography variant="h6">Areas of Interest</Typography>
            </ListItem>
            <Divider />
            {aois.map((aoi, index) => (
              <React.Fragment key={index}>
                <ListItem>
                  <ListItemIcon>
                    <MapIcon />
                  </ListItemIcon>
                  <ListItemText 
                    primary={aoi.name}
                    secondary={
                      <React.Fragment>
                        <Typography variant="body2" color="text.secondary">
                          {aoi.description}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Area: {aoi.area} km²
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          Center: [{aoi.center?.[0]}, {aoi.center?.[1]}]
                        </Typography>
                      </React.Fragment>
                    }
                  />
                </ListItem>
                <ListItem>
                  <IconButton onClick={() => handleViewAOI(aoi)}>
                    <RefreshIcon />
                  </IconButton>
                  <IconButton onClick={() => handleDeleteAOI(aoi)}>
                    <DeleteIcon />
                  </IconButton>
                </ListItem>
                <Divider />
              </React.Fragment>
            ))}
          </List>
        </Box>
      </Drawer>

      <Container maxWidth="xl" sx={{ mt: 2 }}>
        <Box sx={{ height: 'calc(100vh - 100px)', width: '100%' }}>
          <div id="map" style={{ height: '100%', width: '100%' }} />
        </Box>
      </Container>

      <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
        <DialogTitle>Save Area of Interest</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Name"
            fullWidth
            variant="outlined"
            value={aoiName}
            onChange={(e) => setAOIName(e.target.value)}
          />
          <TextField
            margin="dense"
            label="Description"
            fullWidth
            multiline
            rows={4}
            variant="outlined"
            value={aoiDescription}
            onChange={(e) => setAOIDescription(e.target.value)}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleSaveAOI} variant="contained" color="primary">
            Save
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar 
        open={snackbarOpen} 
        autoHideDuration={6000} 
        onClose={() => setSnackbarOpen(false)}
      >
        <Alert 
          onClose={() => setSnackbarOpen(false)} 
          severity={snackbarSeverity}
          sx={{ width: '100%' }}
        >
          {snackbarMessage}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default App;
