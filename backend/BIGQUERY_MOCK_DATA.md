# BigQuery Mock Data Generator

This script generates synthetic data for all BigQuery tables used by the HSBC BCS Assist prep pack service.

## Tables Generated

The script creates mock data for the following tables:

### Core Tables (as specified)
1. **Complaints** - Customer complaint data
   - Fields: `complaint_id`, `complaint_date`, `service_name`, `resolution_type`, `category_name`, `product_type`
   
2. **Inhibits** - Account inhibits and blocks  
   - Fields: `inhibit_name`, `inhibit_date`, `inhibit_desc`
   
3. **Journeys** - Customer journey tracking
   - Fields: `journey_type`, `journey_date`, `journey_name`, `journey_desc`
   
4. **ICS Results** - Customer satisfaction scores
   - Fields: `ics_summary`, `ics_score`, `score_date`

### Additional Tables (assumptions made)
5. **Current Account Tariffs** - Account fee structures
   - Fields: `tariff_name`, `monthly_fee`, `transaction_fee`, `account_type`
   
6. **Digitally Active** - Digital banking activity
   - Fields: `customer_id`, `activity_date`, `digital_channel`, `activity_type`, `session_duration`
   
7. **Vulnerability** - Customer vulnerability assessments  
   - Fields: `customer_id`, `vulnerability_type`, `risk_score`, `assessment_date`, `mitigation_status`

## Setup

### Prerequisites
1. Google Cloud Project with BigQuery enabled
2. Service account with BigQuery admin permissions
3. Python dependencies (already in requirements.txt):
   - `google-cloud-bigquery`
   - `faker`

### Environment Variables
Set the following environment variables:

```bash
export BQ_PROJECT_ID="your-gcp-project-id"
export BQ_DATASET_ID="hsbc_mock_data"  # Optional, defaults to hsbc_mock_data
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"
```

### Authentication
Ensure you have Google Cloud credentials set up:

```bash
# Option 1: Service account key file
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

# Option 2: Use gcloud auth (for development)
gcloud auth application-default login
```

## Usage

### Run the Complete Data Generation
```bash
cd backend
python generate_mock_bigquery_data.py
```

This will:
1. Create the dataset if it doesn't exist
2. Create all tables with proper schemas
3. Generate and insert mock data for all tables
4. Display sample data from each table

### Generated Data Volumes
- **Complaints**: 50 records
- **Inhibits**: 30 records  
- **Journeys**: 40 records
- **ICS Results**: 25 records
- **Current Account Tariffs**: 20 records
- **Digitally Active**: 100 records
- **Vulnerability**: 15 records

### Customer IDs
The script generates 500 mock customers (`CUST_000001` to `CUST_000500`) that are used consistently across all tables.

## Data Characteristics

### Realistic Data Generation
- **Dates**: Realistic date ranges (last 2 years for most data)
- **Names**: Business-appropriate service and product names
- **Descriptions**: Contextual descriptions using Faker
- **Scores**: Appropriate ranges (1-10 for ICS scores, 0.1-10.0 for risk scores)
- **Status Values**: Realistic status progressions

### Sample Data Types

**Complaints**:
- Service names: "Online Banking", "Mobile App", "Branch Services"
- Categories: "Technical Issue", "Service Quality", "Billing Dispute"
- Statuses: "Open", "Resolved", "Pending", "Closed"

**Digital Activity**:
- Channels: "Mobile App", "Online Banking", "ATM", "Phone Banking"
- Activities: "Login", "Transfer", "Payment", "Balance Check"
- Session durations: 30 seconds to 30 minutes

**Vulnerability**:
- Types: "Financial Hardship", "Mental Health", "Physical Disability"
- Severity: "Low", "Medium", "High", "Critical"

## Integration with Prep Pack Service

The generated data is designed to work with the existing prep pack service functions. The table schemas match the expected data structure in the BigQuery integration comments in `prep_pack_service.py`.

### Example Query Usage
```python
# Example BigQuery query to fetch complaints for a customer
query = f"""
    SELECT complaint_id, complaint_date, description, status
    FROM `{PROJECT_ID}.{DATASET_ID}.complaints`
    WHERE customer_id = @customer_id
    ORDER BY complaint_date DESC
"""
```

## Customization

### Modify Data Volumes
Edit the `generate_count` in `TABLE_CONFIGS` dictionary:

```python
TABLE_CONFIGS = {
    "complaints": {
        "generate_count": 100,  # Change from 50 to 100
        # ...
    }
}
```

### Add New Fields
1. Update the schema in `TABLE_CONFIGS`
2. Modify the corresponding generator function
3. Add new sample data arrays as needed

### Change Data Ranges
Modify the date ranges in generator functions:
```python
# Change date range
complaint_date = fake.date_between(start_date="-1y", end_date="today")
```

## Troubleshooting

### Common Issues

1. **Authentication Error**
   ```
   Error: Could not automatically determine credentials
   ```
   Solution: Set `GOOGLE_APPLICATION_CREDENTIALS` or run `gcloud auth application-default login`

2. **Project Not Found**
   ```
   Error: Project your-project-id not found
   ```
   Solution: Set correct `BQ_PROJECT_ID` environment variable

3. **Permission Denied**
   ```
   Error: 403 Access denied: BigQuery
   ```
   Solution: Ensure service account has BigQuery admin permissions

### Verification
After running, verify data in BigQuery console:
```sql
-- Check record counts
SELECT 
  table_name,
  row_count
FROM `your-project-id.hsbc_mock_data.INFORMATION_SCHEMA.TABLE_STORAGE`
WHERE schema_name = 'hsbc_mock_data';
```

## Next Steps

1. Update `prep_pack_service.py` to uncomment and configure BigQuery integration
2. Test service functions with the generated mock data
3. Adjust data generation parameters based on testing needs
4. Set up automated data refresh if needed for continuous testing
