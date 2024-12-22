# SAR AOI Manager Project Scaffold

## Project Structure
```
geescan/
├── gee_interface/          # Google Earth Engine interface
│   ├── __init__.py
│   ├── authenticate.py     # GEE authentication
│   ├── image_viewer.py     # Map viewer using Folium
│   └── query.py           # GEE query functions
├── ui/                    # User interface components
│   ├── __init__.py
│   ├── main_window.py     # Main application window
│   └── main_window.ui     # Qt Designer UI file
└── main.py               # Application entry point
```

## Dependencies
- Python 3.10+
- PyQt5 (GUI Framework)
- Folium (Map Visualization)
- earthengine-api (Google Earth Engine)
- geopy (Geographic coordinates)
- pandas (Data handling)

## Components

### Map Viewer (`image_viewer.py`)
- Uses Folium for interactive map display
- Handles AOI drawing and coordinate extraction
- Integrates with GEE for image queries
- Features:
  - Draw/Edit AOIs
  - Display available image count
  - Show temporal distribution of images

### Main Window (`main_window.py`)
- Main application interface
- Layout:
  - Map view (center)
  - AOI management buttons (left)
  - Timeline display (bottom)
  - Export options (right)

### GEE Interface (`query.py`)
- Handles GEE queries for SAR data
- Functions:
  - Query available images for AOI
  - Get temporal distribution
  - Export GeoTIFF

## Data Flow
1. User draws AOI on map
2. Coordinates sent to GEE query module
3. Query returns:
   - Available image count
   - Image dates
   - Temporal distribution
4. Display results in timeline
5. Enable export for selected dates

## UI Components
- Map View (Folium)
  - Drawing tools
  - Base map layers
- Timeline Display
  - Date range
  - Image count
  - Temporal distribution
- Control Buttons
  - Add/Import/Delete AOI
  - Refresh
  - Export

## Future Enhancements
- Multiple AOI support
- Advanced filtering options
- Batch export capabilities
- Custom visualization parameters
