# GEEScan Project Setup

Start in the `geescan` directory.

## First Time Setup

1. Initialize Docker containers (will preserve any existing containers):
```bash
.\init_containers.bat
```

2. Create a virtual environment and activate it:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-CORS python-dotenv GeoAlchemy2 psycopg2-binary earthengine-api
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Install frontend dependencies:
```bash
cd frontend
# Use --legacy-peer-deps to handle Material-UI version conflicts
npm install --legacy-peer-deps
```

## Daily Development

### Starting the Application
```bash
.\start_app.bat
```
This will:
- Start Docker containers
- Start the Flask backend
- Start the React frontend

### Stopping the Application
```bash
.\clear_ports.bat
```
This will:
- Stop Docker containers (preserves data)
- Clear any processes on ports 3000 and 5000

## Development Notes

### Database
- Using PostgreSQL with PostGIS extension for spatial data
- Default connection: localhost:5432
- Database name: geescan
- Username: postgres
- Password: postgres

### API Endpoints
- Backend runs on http://localhost:5000
- Frontend runs on http://localhost:3000

### Environment Setup
- Make sure Docker Desktop is running
- Node.js and npm should be installed for frontend development

### Common Issues
1. If you see `'react-scripts' is not recognized` or other npm-related errors:
   ```bash
   cd frontend
   # Clean install with legacy peer deps flag
   npm install --legacy-peer-deps
   ```
