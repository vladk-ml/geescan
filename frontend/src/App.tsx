import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Polygon, GeoJSON, FeatureGroup } from 'react-leaflet';
import * as ReactLeafletGeoJSON from 'react-leaflet'; // Add this line here
import L, { LatLngBounds, ControlPosition, FeatureGroup as LeafletFeatureGroup } from 'leaflet';
import * as turf from '@turf/turf';
import * as material from '@mui/material';
import {
    Menu as MenuIcon,
    Edit as EditIcon,
    Delete as DeleteIcon,
    Map as MapIcon,
    Refresh as RefreshIcon
} from '@mui/icons-material';

// Import Leaflet and Leaflet Draw CSS
import 'leaflet/dist/leaflet.css';
import 'leaflet-draw/dist/leaflet.draw.css';

// Import Leaflet Draw
import 'leaflet-draw';

// Fix for the default icon issue
const DefaultIcon = L.icon({
    iconUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-icon.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.3/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    tooltipAnchor: [16, -28],
    shadowSize: [41, 41]
});

L.Marker.prototype.options.icon = DefaultIcon;

interface AOI {
    id: number;
    name: string;
    description?: string;
    geometry: any; // Ensure this matches your backend, or use GeoJSON.Geometry
    area?: number;
    center?: [number, number];
    createdAt?: string;
    updatedAt?: string;
}

function App() {
    const [aois, setAois] = useState<AOI[]>([]);
    const position: [number, number] = [51.505, -0.09];
    const mapRef = useRef<L.Map | null>(null);
    const drawnItemsRef = useRef<LeafletFeatureGroup>(new L.FeatureGroup());
    const [drawerOpen, setDrawerOpen] = useState(false);
    const [dialogOpen, setDialogOpen] = useState(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState('');
    const [snackbarSeverity, setSnackbarSeverity] = useState<'success' | 'error'>('success');
    const [currentAOI, setCurrentAOI] = useState<AOI | null>(null);
    const [aoiName, setAOIName] = useState('');
    const [aoiDescription, setAOIDescription] = useState('');

    // Function to calculate the area and center of a drawn polygon
    const calculateAOIMetrics = (geojson: any): { area: number; center: [number, number] } => {
        const area = turf.area(geojson);
        const center = turf.center(geojson);
        return {
            area: Math.round((area / 1000000) * 100) / 100, // Convert to km² and round
            center: [
                Math.round(center.geometry.coordinates[0] * 1000000) / 1000000,
                Math.round(center.geometry.coordinates[1] * 1000000) / 1000000
            ]
        };
    };

    // Fetch and load AOIs from the database
    const loadAois = async () => {
        try {
            const response = await fetch('http://localhost:5000/api/aois');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            if (Array.isArray(data.aois)) {
                const formattedAois = data.aois.map((aoi: any) => ({
                    id: aoi.id,
                    name: aoi.name,
                    description: aoi.description,
                    geometry: JSON.parse(aoi.geometry),
                    area: aoi.area,
                    center: aoi.center,
                    createdAt: aoi.createdAt,
                    updatedAt: aoi.updatedAt,
                }));
                setAois(formattedAois);
            } else {
                console.error('Unexpected data structure from API:', data);
            }
        } catch (error) {
            console.error("Could not fetch AOIs:", error);
        }
    };

    const handleCreated = (e: L.Draw.CreatedEvent) => {
        const { layer } = e;
        const geojson = layer.toGeoJSON();
        const metrics = calculateAOIMetrics(geojson);

        setCurrentAOI({
            name: '',
            description: '',
            geometry: geojson.geometry as any, // Keep this for now
            area: metrics.area,
            center: metrics.center,
            id: aois.length > 0 ? Math.max(...aois.map(aoi => aoi.id)) + 1 : 1,
        });
        setDialogOpen(true);
    };

    // Call this when the user clicks "Save" in the dialog
    const handleSaveAOI = async () => {
        if (!currentAOI || !aoiName) {
            console.error('Error: currentAOI or aoiName is not defined');
            return;
        }

        const newAOI = {
            ...currentAOI,
            name: aoiName,
            description: aoiDescription,
        };

        await handleAoiDraw(newAOI);

        setDialogOpen(false);
        setCurrentAOI(null);
        setAOIName('');
        setAOIDescription('');
    };

    const handleAoiDraw = async (aoi: AOI) => {
        try {
            const geometryString = JSON.stringify(aoi.geometry);

            const response = await fetch('http://localhost:5000/api/aois', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name: aoi.name, description: aoi.description, geometry: geometryString }),
            });

            const newAoiResponse = await response.json();

            if (response.ok) {
                setAois([...aois, { ...newAoiResponse }]);
                setSnackbarMessage('AOI created successfully');
                setSnackbarSeverity('success');
                setSnackbarOpen(true);
                loadAois(); // Reload AOIs to reflect changes
            } else {
                setSnackbarMessage('Failed to save AOI: ' + newAoiResponse.message);
                setSnackbarSeverity('error');
                setSnackbarOpen(true);
            }
        } catch (error) {
            console.error('Error creating AOI:', error);
            setSnackbarMessage('Failed to save AOI');
            setSnackbarSeverity('error');
            setSnackbarOpen(true);
        }
    };

    const handleDeleteAOI = async (aoiId: number) => {
        try {
            const response = await fetch(`http://localhost:5000/api/aois/${aoiId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                setAois(prevAois => prevAois.filter(aoi => aoi.id !== aoiId));
                if (mapRef.current) {
                    mapRef.current.eachLayer((layer: any) => {
                        if (layer.feature && layer.feature.properties && layer.feature.properties.id === aoiId) {
                            mapRef.current?.removeLayer(layer);
                        }
                    });
                }
                setSnackbarMessage('AOI deleted successfully');
                setSnackbarSeverity('success');
                setSnackbarOpen(true);
            } else {
                const result = await response.json();
                setSnackbarMessage(`Error deleting AOI: ${result.message || response.statusText}`);
                setSnackbarSeverity('error');
                setSnackbarOpen(true);
            }
        } catch (error) {
            console.error('Error deleting AOI:', error);
            setSnackbarMessage('Failed to delete AOI. See console for details.');
            setSnackbarSeverity('error');
            setSnackbarOpen(true);
        }
    };

    const handleViewAOI = (aoi: AOI) => {
        if (mapRef.current && aoi.geometry) {
            const geoJsonLayer = L.geoJSON(aoi.geometry);
            drawnItemsRef.current?.clearLayers();
            drawnItemsRef.current?.addLayer(geoJsonLayer);
            const bounds = geoJsonLayer.getBounds();
            if (bounds.isValid()) {
                mapRef.current.fitBounds(bounds);
            } else {
                console.error('Invalid bounds for the layer of AOI:', aoi);
            }
        }
    };

    useEffect(() => {
        if (!mapRef.current) {
            const map = L.map('map', {
                center: position,
                zoom: 13,
                layers: [
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    })
                ]
            });
            mapRef.current = map;
            drawnItemsRef.current = new L.FeatureGroup().addTo(map);

            const drawOptions: L.Control.DrawConstructorOptions = {
                position: 'topright' as ControlPosition,
                draw: {
                    polygon: {
                        allowIntersection: false,
                        drawError: {
                            color: '#e1e100',
                            message: '<strong>Error:</strong> Polygon intersections not allowed!'
                        },
                        shapeOptions: {
                            color: 'purple'
                        }
                    },
                    polyline: false,
                    circle: false,
                    rectangle: {
                        shapeOptions: {
                            color: 'green'
                        }
                    },
                    marker: false,
                    circlemarker: false
                },
                edit: {
                    featureGroup: drawnItemsRef.current,
                    remove: true
                }
            };
            const drawControl = new (L.Control as any).Draw(drawOptions);
            mapRef.current.addControl(drawControl);
            mapRef.current.on('draw:created', handleCreated);

            loadAois();
        }
        return () => {
            mapRef.current?.off('draw:created', handleCreated);
        };
    }, []);

    useEffect(() => {
        if (mapRef.current) {
            drawnItemsRef.current.clearLayers();
            aois.forEach(aoi => {
                const geoJsonLayer = L.geoJSON(aoi.geometry, {
                    onEachFeature: (feature, layer) => {
                        layer.bindTooltip(aoi.name);
                        layer.on('click', () => handleViewAOI(aoi));
                        layer.feature = { properties: { id: aoi.id } };
                    }
                });
                drawnItemsRef.current.addLayer(geoJsonLayer);
            });
        }
    }, [aois]);

    return (
        <material.Box sx={{ display: 'flex' }}>
            <material.Drawer
                open={drawerOpen}
                onClose={() => setDrawerOpen(false)}
            >
                <material.List>
                    <material.ListItem button key="refresh" onClick={loadAois}>
                        <material.ListItemIcon><RefreshIcon /></material.ListItemIcon>
                        <material.ListItemText primary="Refresh AOIs" />
                    </material.ListItem>
                    {aois.map((aoi) => (
                        <material.ListItem button key={aoi.id} onClick={() => handleViewAOI(aoi)}>
                            <material.ListItemIcon><MapIcon /></material.ListItemIcon>
                            <material.ListItemText primary={aoi.name} secondary={`Area: ${aoi.area} km²`} />
                            <material.IconButton edge="end" aria-label="edit" onClick={(e) => { e.stopPropagation(); /* Implement edit functionality */ }}>
                                <EditIcon />
                            </material.IconButton>
                            <material.IconButton edge="end" aria-label="delete" onClick={(e) => { e.stopPropagation(); handleDeleteAOI(aoi.id); }}>
                                <DeleteIcon />
                            </material.IconButton>
                        </material.ListItem>
                    ))}
                </material.List>
            </material.Drawer>
            <material.Box component="main" sx={{ flexGrow: 1, p: 3, height: '100vh', position: 'relative' }}>
                <material.AppBar position="static">
                    <material.Toolbar>
                        <material.IconButton
                            size="large"
                            edge="start"
                            color="inherit"
                            aria-label="menu"
                            sx={{ mr: 2 }}
                            onClick={() => setDrawerOpen(true)}
                        >
                            <MenuIcon />
                        </material.IconButton>
                        <material.Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                            AOI Management
                        </material.Typography>
                    </material.Toolbar>
                </material.AppBar>
                <div id="map" style={{ height: 'calc(100vh - 64px)', width: '100%' }} />
            </material.Box>
            <material.Dialog open={dialogOpen} onClose={() => setDialogOpen(false)}>
                <material.DialogTitle>Name Your AOI</material.DialogTitle>
                <material.DialogContent>
                    <material.TextField
                        autoFocus
                        margin="dense"
                        id="name"
                        label="AOI Name"
                        type="text"
                        fullWidth
                        variant="standard"
                        value={aoiName}
                        onChange={(e) => setAOIName(e.target.value)}
                    />
                    <material.TextField
                        margin="dense"
                        id="description"
                        label="AOI Description"
                        type="text"
                        fullWidth
                        variant="standard"
                        value={aoiDescription}
                        onChange={(e) => setAOIDescription(e.target.value)}
                    />
                </material.DialogContent>
                <material.DialogActions>
                    <material.Button onClick={() => setDialogOpen(false)}>Cancel</material.Button>
                    <material.Button onClick={handleSaveAOI}>Save</material.Button>
                </material.DialogActions>
            </material.Dialog>
            <material.Snackbar
                open={snackbarOpen}
                autoHideDuration={6000}
                onClose={() => setSnackbarOpen(false)}
                message={snackbarMessage}
                severity={snackbarSeverity}
            />
        </material.Box>
    );
}

export default App;