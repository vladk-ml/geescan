# GEEScan Project Setup

## Backend Setup

1. Create a virtual environment and activate it:
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
```

2. Install the required packages:
```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-CORS python-dotenv GeoAlchemy2 psycopg2-binary earthengine-api
```

3. Set up the environment variables in `.env`:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/geescan
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json
```

4. Initialize the database:
```bash
flask db init
flask db migrate
flask db upgrade
```

5. Start the Flask development server:
```bash
python run.py
```

## Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install --legacy-peer-deps
```

2. Start the development server:
```bash
npm start
```

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
- Make sure PostgreSQL and PostGIS are installed
- Ensure Google Earth Engine credentials are properly configured
- Node.js and npm should be installed for frontend development
