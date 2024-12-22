# GEEScan - SAR Data Monitoring System

A robust system for monitoring SAR data from Google Earth Engine, with support for managing Areas of Interest (AOIs) and automated data processing.

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker Desktop
- PostgreSQL 14+ with PostGIS extension
- Google Earth Engine account with authentication set up

## First Time Setup

1. Clone the repository and navigate to it:
   ```bash
   git clone https://github.com/yourusername/geescan.git
   cd geescan
   ```

2. Run the initialization script:
   ```bash
   .\init_containers.bat
   ```
   This will set up the required Docker containers for PostgreSQL and PGAdmin.

3. Run the startup script:
   ```bash
   .\start_app.bat
   ```
   The first run will:
   - Create and activate Python virtual environment
   - Install Python dependencies
   - Initialize the database
   - Install frontend dependencies
   - Start all services

## Daily Usage

### Starting the Application
```bash
.\start_app.bat
```
This will:
- Start Docker containers
- Start the Flask backend (http://localhost:5000)
- Start the React frontend (port shown in terminal)

### Stopping the Application
```bash
.\clear_ports.bat
```
This will:
- Stop Docker containers (preserves data)
- Clear any processes on ports 3000 and 5000

## Project Structure

```
geescan/
├── backend/           # Flask backend
│   ├── app/          # Application code
│   │   ├── api/      # API endpoints
│   │   └── models/   # Database models
│   └── venv/         # Python virtual environment
├── frontend/         # React frontend
│   └── src/         # Source code
└── scripts/         # Utility scripts
    ├── init_containers.bat  # First-time container setup
    ├── start_app.bat       # Start the application
    └── clear_ports.bat     # Stop the application
```

## Development

- Backend API: http://localhost:5000
- Frontend: Port shown in React terminal
- PostgreSQL: localhost:5432
- PGAdmin: http://localhost:5050

## Common Issues

1. If you see `'react-scripts' is not recognized` or other npm-related errors:
   ```bash
   cd frontend
   npm install --legacy-peer-deps
   ```

2. If ports are already in use:
   ```bash
   .\clear_ports.bat
   ```

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

MIT License