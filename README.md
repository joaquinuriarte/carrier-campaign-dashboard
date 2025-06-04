# Carrier Campaign Dashboard

A Streamlit-based dashboard for visualizing carrier campaign call data, featuring call outcomes, sentiment analysis, and negotiation metrics.

## Structure

- `app/` - Main application code
  - `components/` - Reusable UI components
  - `services/` - Data processing and business logic
  - `database/` - Database models and connection
- `main.py` - Application entry point
- `requirements.txt` - Python dependencies
- `Dockerfile` - Container configuration

## Deployment

### Local Development

1. Install Docker
2. Build and run:
```bash
docker build -t carrier-campaign-dashboard .
docker run -p 8501:8501 -e DATABASE_URL="your_db_url" carrier-campaign-dashboard
```

The dashboard will be available at http://localhost:8501

### Render Deployment

1. Fork this repository
2. Create a new Web Service on Render
3. Connect to your GitHub repository
4. Add environment variables:
   - `DATABASE_URL`: Your PostgreSQL connection string

## Access

The dashboard is hosted at: https://carrier-campaign-dashboard-docker.onrender.com/

- Secure HTTPS connection
- Database authentication via environment variables
- Real-time data visualization

