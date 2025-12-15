"""
Mock Data Generator for BigQuery Tables

This script generates synthetic data for all BigQuery tables used by the prep pack service.
Tables covered:
- Complaints
- Inhibits  
- Journeys
- ICS Results
- Current Account Tariffs
- Digitally Active
- Vulnerability
"""

import os
import random
from datetime import date, timedelta, datetime
from typing import List, Dict, Any
from faker import Faker
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

# Initialize Faker
fake = Faker()

# BigQuery configuration
PROJECT_ID = os.getenv("BQ_PROJECT_ID", "ai-ml-team-sandbox")
DATASET_ID = os.getenv("BQ_DATASET_ID", "HSBC_mock_reuben")

# Define table schemas and sample data configurations
TABLE_CONFIGS = {
    "complaints": {
        "schema": [
            bigquery.SchemaField("complaint_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("complaint_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("service_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("resolution_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("category_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("product_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        ],
        "generate_count": 50
    },
    
    "inhibits": {
        "schema": [
            bigquery.SchemaField("inhibit_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("inhibit_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("inhibit_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("inhibit_desc", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("inhibit_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        ],
        "generate_count": 30
    },
    
    "journeys": {
        "schema": [
            bigquery.SchemaField("journey_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("journey_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("journey_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("journey_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("journey_desc", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("status", "STRING", mode="REQUIRED"),
        ],
        "generate_count": 40
    },
    
    "ics_results": {
        "schema": [
            bigquery.SchemaField("ics_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("ics_summary", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("ics_score", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("score_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("assessment_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("numeric_score", "FLOAT", mode="NULLABLE"),
        ],
        "generate_count": 25
    },
    
    "current_account_tariffs": {
        "schema": [
            bigquery.SchemaField("tariff_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("tariff_name", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("monthly_fee", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("transaction_fee", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("account_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("effective_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("currency", "STRING", mode="REQUIRED"),
        ],
        "generate_count": 20
    },
    
    "digitally_active": {
        "schema": [
            bigquery.SchemaField("activity_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("activity_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("digital_channel", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("activity_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("session_duration", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("transaction_count", "INTEGER", mode="NULLABLE"),
            bigquery.SchemaField("device_type", "STRING", mode="NULLABLE"),
        ],
        "generate_count": 100
    },
    
    "vulnerability": {
        "schema": [
            bigquery.SchemaField("vulnerability_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("customer_id", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("vulnerability_type", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("risk_score", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("assessment_date", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("mitigation_status", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("severity_level", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("notes", "STRING", mode="NULLABLE"),
        ],
        "generate_count": 15
    }
}

class MockDataGenerator:
    def __init__(self):
        self.client = bigquery.Client(project=PROJECT_ID)
        self.customer_ids = [f"CUST_{i:06d}" for i in range(1, 501)]  # 500 mock customers
        
    def generate_complaints_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock complaints data"""
        service_names = ["Online Banking", "Mobile App", "Branch Services", "Phone Banking", 
                        "Investment Services", "Credit Cards", "Mortgages", "Business Banking"]
        resolution_types = ["Resolved", "Escalated", "Pending Investigation", "Closed", "Refunded"]
        categories = ["Technical Issue", "Service Quality", "Billing Dispute", "Product Information", 
                     "Access Issues", "Transaction Error", "Account Management"]
        product_types = ["Current Account", "Savings Account", "Credit Card", "Mortgage", 
                        "Business Account", "Investment Product", "Insurance"]
        statuses = ["Open", "Resolved", "Pending", "Closed"]
        
        data = []
        for i in range(count):
            complaint_date = fake.date_between(start_date="-2y", end_date="today")
            data.append({
                "complaint_id": f"CMP_{i+1:06d}",
                "complaint_date": complaint_date,
                "service_name": fake.random_element(service_names),
                "resolution_type": fake.random_element(resolution_types),
                "category_name": fake.random_element(categories),
                "product_type": fake.random_element(product_types),
                "customer_id": fake.random_element(self.customer_ids),
                "description": fake.paragraph(nb_sentences=2),
                "status": fake.random_element(statuses)
            })
        return data
    
    def generate_inhibits_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock inhibits data"""
        inhibit_names = ["ACH Debit Block", "Check Block", "Wire Block", "Card Block", 
                        "Online Access Block", "ATM Block", "International Block"]
        inhibit_types = ["Payment Block", "Access Restriction", "Security Hold", "Regulatory Block"]
        statuses = ["Active", "Inactive", "Pending", "Removed"]
        
        data = []
        for i in range(count):
            inhibit_date = fake.date_between(start_date="-1y", end_date="today")
            inhibit_name = fake.random_element(inhibit_names)
            data.append({
                "inhibit_id": f"INH_{i+1:06d}",
                "inhibit_name": inhibit_name,
                "inhibit_date": inhibit_date,
                "inhibit_desc": f"Inhibit placed on {inhibit_name.lower()} - {fake.sentence()}",
                "customer_id": fake.random_element(self.customer_ids),
                "inhibit_type": fake.random_element(inhibit_types),
                "status": fake.random_element(statuses)
            })
        return data
    
    def generate_journeys_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock journeys data"""
        journey_types = ["Account Opening", "Product Application", "Service Request", 
                        "Complaint Resolution", "Onboarding", "KYC Update"]
        journey_names = ["New Business Account Setup", "Credit Card Application", 
                        "Mortgage Application", "Online Banking Registration",
                        "International Wire Setup", "Investment Account Opening"]
        statuses = ["Completed", "In Progress", "Pending", "Cancelled", "On Hold"]
        
        data = []
        for i in range(count):
            journey_date = fake.date_between(start_date="-18m", end_date="today")
            journey_name = fake.random_element(journey_names)
            data.append({
                "journey_id": f"JNY_{i+1:06d}",
                "journey_type": fake.random_element(journey_types),
                "journey_date": journey_date,
                "journey_name": journey_name,
                "journey_desc": f"Customer journey for {journey_name.lower()} - {fake.sentence()}",
                "customer_id": fake.random_element(self.customer_ids),
                "status": fake.random_element(statuses)
            })
        return data
    
    def generate_ics_results_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock ICS results data"""
        assessment_types = ["Customer Satisfaction", "Service Quality", "Product Feedback", 
                           "Branch Experience", "Digital Experience"]
        
        data = []
        for i in range(count):
            numeric_score = round(random.uniform(1, 10), 1)
            score_date = fake.date_between(start_date="-1y", end_date="today")
            data.append({
                "ics_id": f"ICS_{i+1:06d}",
                "ics_summary": fake.paragraph(nb_sentences=1),
                "ics_score": f"{numeric_score}/10",
                "score_date": score_date,
                "customer_id": fake.random_element(self.customer_ids),
                "assessment_type": fake.random_element(assessment_types),
                "numeric_score": numeric_score
            })
        return data
    
    def generate_tariffs_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock current account tariffs data"""
        tariff_names = ["Standard Business", "Premium Business", "Corporate Elite", 
                       "SME Basic", "Enterprise Plus", "Startup Account"]
        account_types = ["Business Current", "Corporate Current", "SME Current", 
                        "Premium Current", "Standard Current"]
        currencies = ["GBP", "USD", "EUR"]
        
        data = []
        for i in range(count):
            effective_date = fake.date_between(start_date="-2y", end_date="today")
            data.append({
                "tariff_id": f"TAR_{i+1:06d}",
                "tariff_name": fake.random_element(tariff_names),
                "monthly_fee": round(random.uniform(5.0, 50.0), 2),
                "transaction_fee": round(random.uniform(0.1, 2.5), 2),
                "account_type": fake.random_element(account_types),
                "customer_id": fake.random_element(self.customer_ids),
                "effective_date": effective_date,
                "currency": fake.random_element(currencies)
            })
        return data
    
    def generate_digitally_active_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock digitally active data"""
        digital_channels = ["Mobile App", "Online Banking", "ATM", "Phone Banking", 
                           "Branch Kiosk", "API"]
        activity_types = ["Login", "Transfer", "Payment", "Balance Check", "Statement Download", 
                         "Profile Update", "Card Management"]
        device_types = ["Mobile", "Desktop", "Tablet", "ATM", "Kiosk"]
        
        data = []
        for i in range(count):
            activity_date = fake.date_between(start_date="-6m", end_date="today")
            data.append({
                "activity_id": f"ACT_{i+1:06d}",
                "customer_id": fake.random_element(self.customer_ids),
                "activity_date": activity_date,
                "digital_channel": fake.random_element(digital_channels),
                "activity_type": fake.random_element(activity_types),
                "session_duration": random.randint(30, 1800),  # 30 seconds to 30 minutes
                "transaction_count": random.randint(1, 10),
                "device_type": fake.random_element(device_types)
            })
        return data
    
    def generate_vulnerability_data(self, count: int) -> List[Dict[str, Any]]:
        """Generate mock vulnerability data"""
        vulnerability_types = ["Financial Hardship", "Mental Health", "Physical Disability", 
                              "Age Related", "Language Barrier", "Digital Exclusion", "Cognitive Impairment"]
        mitigation_statuses = ["Identified", "Support Offered", "Active Support", "Monitoring", "Resolved"]
        severity_levels = ["Low", "Medium", "High", "Critical"]
        
        data = []
        for i in range(count):
            assessment_date = fake.date_between(start_date="-1y", end_date="today")
            data.append({
                "vulnerability_id": f"VUL_{i+1:06d}",
                "customer_id": fake.random_element(self.customer_ids),
                "vulnerability_type": fake.random_element(vulnerability_types),
                "risk_score": round(random.uniform(0.1, 10.0), 2),
                "assessment_date": assessment_date,
                "mitigation_status": fake.random_element(mitigation_statuses),
                "severity_level": fake.random_element(severity_levels),
                "notes": fake.paragraph(nb_sentences=1) if random.choice([True, False]) else None
            })
        return data
    
    def get_existing_tables(self):
        """Get list of existing table names in the dataset"""
        try:
            dataset_ref = self.client.dataset(DATASET_ID)
            tables = self.client.list_tables(dataset_ref)
            return [table.table_id.lower() for table in tables]
        except NotFound:
            print(f"Dataset {DATASET_ID} not found")
            return []
        except Exception as e:
            print(f"Error listing tables: {e}")
            return []
    
    def create_dataset_if_not_exists(self):
        """Create the dataset if it doesn't exist"""
        dataset_id = f"{PROJECT_ID}.{DATASET_ID}"
        
        try:
            self.client.get_dataset(dataset_id)
            print(f"Dataset {dataset_id} already exists.")
        except NotFound:
            print(f"Creating dataset {dataset_id}...")
            dataset = bigquery.Dataset(dataset_id)
            dataset.location = "US"  # Change as needed
            dataset = self.client.create_dataset(dataset, timeout=30)
            print(f"Created dataset {dataset.project}.{dataset.dataset_id}")
    
    def check_table_exists(self, table_name: str, schema: List[bigquery.SchemaField]):
        """Check if table exists, create only if it doesn't"""
        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        
        try:
            existing_table = self.client.get_table(table_id)
            print(f"✓ Table {table_id} already exists - will insert data into existing table.")
            return True
        except NotFound:
            print(f"Creating new table {table_id}...")
            table = bigquery.Table(table_id, schema=schema)
            table = self.client.create_table(table)
            print(f"Created table {table.project}.{table.dataset_id}.{table.table_id}")
            return False
    
    def get_table_schema_info(self, table_name: str):
        """Get existing table schema information"""
        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        try:
            table = self.client.get_table(table_id)
            schema_info = {}
            for field in table.schema:
                schema_info[field.name.lower()] = {
                    'name': field.name,
                    'type': field.field_type,
                    'mode': field.mode or 'NULLABLE'
                }
            return schema_info
        except Exception as e:
            print(f"Error getting schema for {table_name}: {e}")
            return {}
    
    def adapt_data_to_schema(self, data: List[Dict[str, Any]], schema_info: Dict, table_name: str):
        """Adapt generated data to match existing table schema exactly"""
        adapted_data = []
        
        # Show which fields will be matched
        generated_fields = set(key.lower() for key in data[0].keys()) if data else set()
        schema_fields = set(schema_info.keys())
        matching_fields = generated_fields.intersection(schema_fields)
        
        print(f"   Generated fields: {len(generated_fields)}, Table fields: {len(schema_fields)}")
        print(f"   Matching fields ({len(matching_fields)}): {', '.join(sorted(matching_fields))}")
        
        if not matching_fields:
            print(f"   WARNING: No matching fields found for {table_name}")
            return []
        
        for row in data:
            adapted_row = {}
            
            # Only include fields that exist in the target table
            for key, value in row.items():
                key_lower = key.lower()
                if key_lower in schema_info:
                    field_info = schema_info[key_lower]
                    actual_field_name = field_info['name']
                    field_type = field_info['type']
                    field_mode = field_info['mode']
                    
                    # Convert value based on field type
                    if value is None and field_mode == 'REQUIRED':
                        # Provide default values for required fields
                        if field_type == 'STRING':
                            converted_value = 'Unknown'
                        elif field_type == 'INTEGER':
                            converted_value = 0
                        elif field_type == 'FLOAT':
                            converted_value = 0.0
                        elif field_type == 'DATE':
                            converted_value = '2024-01-01'
                        else:
                            converted_value = 'Default'
                    elif isinstance(value, date):
                        converted_value = value.strftime('%Y-%m-%d')
                    elif field_type == 'STRING' and not isinstance(value, str):
                        converted_value = str(value)
                    elif field_type == 'INTEGER' and isinstance(value, float):
                        converted_value = int(value)
                    elif field_type == 'FLOAT' and isinstance(value, int):
                        converted_value = float(value)
                    else:
                        converted_value = value
                    
                    adapted_row[actual_field_name] = converted_value
            
            adapted_data.append(adapted_row)
        
        return adapted_data
    
    def insert_data_to_table(self, table_name: str, data: List[Dict[str, Any]]):
        """Insert data using SQL INSERT statements to avoid schema issues"""
        table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
        
        try:
            # Get the actual schema of the existing table
            schema_info = self.get_table_schema_info(table_name)
            if not schema_info:
                print(f"   Could not get schema for {table_name}, skipping...")
                return
            
            print(f"   Table has {len(schema_info)} fields")
            
            # Adapt our data to match the exact schema
            adapted_data = self.adapt_data_to_schema(data, schema_info, table_name)
            
            if not adapted_data:
                print(f"   No compatible data generated for {table_name}")
                return
            
            # Build INSERT statement
            field_names = list(adapted_data[0].keys())
            fields_str = ", ".join([f"`{field}`" for field in field_names])
            
            # Build VALUES clauses in batches
            batch_size = 10
            total_inserted = 0
            
            for i in range(0, len(adapted_data), batch_size):
                batch = adapted_data[i:i + batch_size]
                
                values_clauses = []
                for row in batch:
                    values = []
                    for field in field_names:
                        value = row[field]
                        if value is None:
                            values.append("NULL")
                        elif isinstance(value, str):
                            # Handle date strings and regular strings
                            if field.lower().endswith('_date') or field.lower() == 'date':
                                # Date field - use DATE() function
                                values.append(f"DATE('{value}')")
                            else:
                                # Regular string - proper escaping for BigQuery
                                escaped_value = value.replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
                                values.append(f"'{escaped_value}'")
                        elif isinstance(value, (int, float)):
                            values.append(str(value))
                        else:
                            # Convert other types to string with proper escaping
                            str_value = str(value).replace("\\", "\\\\").replace("'", "\\'").replace('"', '\\"')
                            values.append(f"'{str_value}'")
                    
                    values_clauses.append(f"({', '.join(values)})")
                
                # Execute INSERT for this batch
                insert_query = f"""
                INSERT INTO `{table_id}` ({fields_str})
                VALUES {', '.join(values_clauses)}
                """
                
                job = self.client.query(insert_query)
                job.result()  # Wait for completion
                
                total_inserted += len(batch)
                print(f"   Inserted batch {i//batch_size + 1}: {len(batch)} rows")
            
            # Get updated row count
            table = self.client.get_table(table_id)
            print(f" Successfully inserted {total_inserted} rows total")
            print(f"   Total rows in table: {table.num_rows}")
            
        except Exception as e:
            print(f" Error inserting data into {table_name}: {e}")
            # Try to show sample query for debugging
            if 'insert_query' in locals():
                print(f"   Sample query (first 200 chars): {insert_query[:200]}...")
    
    def generate_all_mock_data(self):
        """Generate and insert all mock data"""
        print("Starting mock data generation...")
        
        # Create dataset
        self.create_dataset_if_not_exists()
        
        # Generate data for each table
        generators = {
            "complaints": self.generate_complaints_data,
            "inhibits": self.generate_inhibits_data,
            "journeys": self.generate_journeys_data,
            "ics_results": self.generate_ics_results_data,
            "current_account_tariffs": self.generate_tariffs_data,
            "digitally_active": self.generate_digitally_active_data,
            "vulnerability": self.generate_vulnerability_data
        }
        
        # First, check which tables actually exist
        existing_tables = self.get_existing_tables()
        print(f"Found {len(existing_tables)} existing tables: {', '.join(existing_tables)}")
        
        for table_name, config in TABLE_CONFIGS.items():
            print(f"\n📊 Processing table: {table_name}")
            
            # Skip tables that don't exist in BigQuery
            if table_name.lower() not in existing_tables:
                print(f"   Table {table_name} doesn't exist in BigQuery - creating it...")
                self.check_table_exists(table_name, config["schema"])
            else:
                print(f"   Table {table_name} exists - adapting data to existing schema")
            
            # Generate and insert data
            generator_func = generators[table_name]
            data = generator_func(config["generate_count"])
            self.insert_data_to_table(table_name, data)
        
        print("\nMock data generation completed!")
    
    def query_sample_data(self, table_name: str, limit: int = 5):
        """Query sample data from a table"""
        query = f"""
        SELECT *
        FROM `{PROJECT_ID}.{DATASET_ID}.{table_name}`
        LIMIT {limit}
        """
        
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            
            print(f"\nSample data from {table_name}:")
            for row in results:
                print(dict(row))
        except Exception as e:
            print(f"Error querying {table_name}: {e}")


def main():
    """Main function to run the mock data generation"""
    print("HSBC Mock Data Generator for BigQuery")
    print("=" * 50)
    print("This will add mock data to your existing BigQuery tables.")
    print("Existing tables will NOT be modified, only populated with data.\n")
    
    # Check if required environment variables are set
    if not PROJECT_ID or PROJECT_ID == "ai-ml-team-sandbox":
        print(f"Using project: {PROJECT_ID}")
        print(f"Using dataset: {DATASET_ID}")
    
    try:
        generator = MockDataGenerator()
        
        # Generate all mock data
        generator.generate_all_mock_data()
        
        # Show sample data from each table
        print("\n" + "=" * 50)
        print("Sample data from populated tables:")
        for table_name in TABLE_CONFIGS.keys():
            generator.query_sample_data(table_name, 2)
            
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure you have:")
        print("1. Set up Google Cloud credentials (GOOGLE_APPLICATION_CREDENTIALS)")
        print("2. Set BQ_PROJECT_ID environment variable") 
        print("3. Installed required dependencies: pip install google-cloud-bigquery faker")


if __name__ == "__main__":
    main()
