# GEEScan - SAR Data Monitoring System

A robust system for monitoring SAR data from Google Earth Engine, with support for managing Areas of Interest (AOIs) and automated data processing.

## Prerequisites

- Python 3.9+
- Node.js 18+
- Docker and Docker Compose
- PostgreSQL 14+ with PostGIS extension
- Google Earth Engine account
- Google Cloud Platform account

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/geescan.git
   cd geescan
   ```

2. Set up Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. Start the development environment:
   ```bash
   docker-compose up -d  # Starts PostgreSQL and other services
   python backend/run.py  # Starts the Flask backend
   cd frontend && npm start  # Starts the React frontend
   ```

## Project Structure

```
geescan/
├── backend/
│   ├── api/            # API endpoints
│   ├── models/         # Database models
│   ├── services/       # Business logic
│   └── utils/          # Utility functions
├── frontend/
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   └── services/   # API services
│   └── public/         # Static files
└── docker/             # Docker configuration
```

## Development

- Backend API: http://localhost:5000
- Frontend: http://localhost:3000
- API Documentation: http://localhost:5000/api/docs

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

[Your chosen license]