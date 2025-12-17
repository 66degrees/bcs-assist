# BCS Profile Assistant

A high-fidelity customer profile assistant application for HSBC Commercial Banking Services (BCS). This application integrates with Genesys Cloud for conversation context and BigQuery for customer data, providing real-time customer insights to banking representatives.

## 🏗️ Architecture Overview

The application consists of two main components:

- **Backend (FastAPI)**: Mock Genesys service that handles authentication, customer data fetching, and BigQuery integration
- **Frontend (Streamlit)**: Interactive dashboard displaying customer profiles, KPIs, and insights

## Python Packages & Dependencies

### Backend Dependencies (`/backend/requirements.txt`)
```python
# Core Framework
fastapi                    # Modern, fast web framework for building APIs
uvicorn[standard]         # ASGI web server implementation
pydantic                  # Data validation and settings management

# Configuration & Environment
python-dotenv             # Load environment variables from .env files

# HTTP Client & Authentication
httpx                     # Async HTTP client for Python 3
PyJWT                     # JSON Web Token implementation

# Data Generation & Testing
Faker                     # Generate fake data for testing

# Google Cloud Integration
google-cloud-bigquery     # BigQuery client library for real data integration
```

### Frontend Dependencies (`/frontend/requirements.txt`)
```python
streamlit>=1.28.0         # Web app framework for machine learning and data science
requests                  # Simple HTTP library for Python
pandas                    # Data manipulation and analysis library
```

##  Installation & Setup

### Prerequisites
- Python 3.8+
- Google Cloud Platform account (for BigQuery integration)
- Genesys Cloud account (for production deployment)

### 1. Clone Repository
```bash
git clone <repository-url>
cd bcs-assist
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp env.example .env
# Edit .env file with your actual credentials (see Configuration section)
```

### 3. Frontend Setup
```bash
cd frontend

# Create virtual environment (if not using shared environment)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## ⚙️ Configuration

### Environment Variables (.env)
Create a `.env` file in the `/backend` directory with the following configuration:

```bash
# --- Genesys Cloud Credentials (Production) ---
GENESYS_CLIENT_ID=your_genesys_client_id
GENESYS_CLIENT_SECRET=your_genesys_client_secret
GENESYS_REGION=mypurecloud.com
GENESYS_REDIRECT_URI=https://your-frontend-app-url.com

# --- BigQuery Configuration (Real Data) ---
BQ_PROJECT_ID=your_gcp_project_id
BQ_DATASET_ID=your_bigquery_dataset_id
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account.json

# --- API Configuration ---
FRONTEND_URL=http://localhost:8501

# --- API Endpoints (Production) ---
GENESYS_AUTH_URL=https://login.mypurecloud.com/oauth/token
GENESYS_API_URL=https://api.mypurecloud.com
```

### Google Cloud Setup
1. Create a Google Cloud Project
2. Enable BigQuery API
3. Create a service account with BigQuery permissions
4. Download the service account JSON key
5. Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your JSON key file

##  Running the Application

### Development Mode (Mock Data)

#### 1. Start Backend Server
```bash
cd backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The backend will be available at: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

#### 2. Start Frontend Application
```bash
cd frontend
source venv/bin/activate
streamlit run app.py --server.port 8501
```
The frontend will be available at: `http://localhost:8501`

### Production Mode (Docker)
```bash
# Build and run with Docker
cd backend
docker build -t bcs-assist-backend .
docker run -d -p 8000:8000 --env-file .env bcs-assist-backend
```

##  Real Implementation Details

### Current Mock vs. Real Implementation

The application is designed with a dual approach - it currently uses **mock data and services** for development/demonstration, but includes **real implementation code** (commented out) for production deployment.

#### Authentication Flow (Real Implementation)
1. **PKCE Flow Integration**: Real Genesys Cloud OAuth 2.0 with PKCE (Proof Key for Code Exchange)
   - Authorization code received from Genesys Widget
   - Code verifier used for secure token exchange
   - Access token obtained for API calls

2. **Token Exchange**: 
   ```python
   # Real implementation in auth_service.py (currently commented)
   POST https://login.{region}/oauth/token
   ```

#### Customer Data Retrieval (Real Implementation)
1. **Genesys API Integration**:
   ```python
   # Real implementation in customer_service.py (currently commented)
   GET https://api.{region}/api/v2/conversations/{conversation_id}
   ```
   - Fetches conversation participants
   - Extracts customer identifiers (PCIN, BCIN)
   - Maps to internal customer IDs

2. **BigQuery Data Sources**: Real customer data is fetched from multiple BigQuery tables:
   - `complaints`: Customer complaint history
   - `customer_kpis`: Key performance indicators
   - `revenue_data`: Financial metrics and trends
   - `transaction_data`: Transaction volume summaries
   - `inhibit_data`: Account restrictions and inhibits
   - `customer_journeys`: Customer lifecycle data

#### Data Pipeline Architecture


###  Production Deployment Steps

1. **Genesys Cloud Configuration**:
   - Create OAuth 2.0 client in Genesys Cloud
   - Configure redirect URIs for your domain
   - Set up conversation routing to trigger widget

2. **BigQuery Data Setup**:
   - Create required tables with customer data schema
   - Set up service account with appropriate permissions
   - Configure data pipelines for real-time updates

3. **Enable Real Implementation**:
   ```python
   # In auth_service.py - uncomment and use:
   # get_real_genesys_auth_token()
   
   # In customer_service.py - uncomment and use:
   # get_real_genesys_customer_data()
   
   # In prep_pack_service.py - already implemented:
   # Real BigQuery functions are active (fetch_*_from_bigquery)
   ```

4. **Production Environment Variables**:
   - Set all Genesys credentials
   - Configure BigQuery project and dataset
   - Set up proper CORS origins
   - Configure SSL certificates

## Dashboard Features

The frontend provides a comprehensive customer profile dashboard:

### Core Components
- **Network Relationship**: Customer hierarchy and linked businesses
- **KPI Metrics**: Financial and relationship metrics (10+ KPIs)
- **AI Insights**: Contextual customer insights and recommendations
- **Financial Charts**: Revenue trends and distribution analysis
- **Transaction Summary**: Volume and value analytics
- **Risk Indicators**: Account inhibits and restrictions
- **Customer Journey**: Lifecycle stage and journey status
- **Complaint History**: Recent customer complaints and resolution status

### Real-time Features
- **Genesys Integration**: Automatic customer identification from conversation context
- **Dynamic Data**: Real-time data fetching from BigQuery
- **Responsive UI**: Modern, card-based layout optimized for banking workflows

## 🐳 Docker Deployment

### Build and Run
```bash
cd backend
docker build -t bcs-assist-backend .
docker run -d \
  --name bcs-assist \
  -p 8000:8000 \
  --env-file .env \
  bcs-assist-backend
```

### Docker Environment
The Dockerfile includes all necessary dependencies and configurations for production deployment.

## 🔧 Development & Testing

### Testing Mock Data
The application includes comprehensive mock data generation:
```bash
cd backend
python generate_mock_bigquery_data.py  # Generate test BigQuery data
python test_existing_tables.py         # Test BigQuery connectivity
```

### API Testing
- Interactive API documentation at `/docs` endpoint
- Health check endpoint for monitoring
- CORS configured for cross-origin requests

## 🔐 Security Considerations

- **Environment Variables**: All sensitive credentials stored in `.env` files
- **CORS Configuration**: Properly configured for production domains
- **Token Validation**: JWT token validation for API requests
- **BigQuery IAM**: Service account with minimal required permissions

##  Monitoring & Analytics

The application supports comprehensive monitoring:
- Health check endpoints for service monitoring
- Request/response logging for audit trails
- Error handling with detailed logging
- Performance metrics for BigQuery queries

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with proper error handling
4. Add tests for new functionality
5. Update documentation as needed
6. Submit pull request

---

