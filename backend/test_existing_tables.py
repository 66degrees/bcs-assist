"""
Quick test script to verify existing table structure
Run this before the main data generation to see your existing table schemas
"""

import os
from google.cloud import bigquery

PROJECT_ID = os.getenv("BQ_PROJECT_ID", "ai-ml-team-sandbox") 
DATASET_ID = os.getenv("BQ_DATASET_ID", "HSBC_mock_reuben")

def check_existing_tables():
    """Check what tables exist and their schemas"""
    client = bigquery.Client(project=PROJECT_ID)
    
    try:
        # List all tables in dataset
        dataset_ref = client.dataset(DATASET_ID)
        tables = client.list_tables(dataset_ref)
        
        print(f"Existing tables in {PROJECT_ID}.{DATASET_ID}:")
        print("=" * 60)
        
        for table in tables:
            print(f"\n Table: {table.table_id}")
            
            # Get table details
            table_ref = client.get_table(table.reference)
            print(f"   Rows: {table_ref.num_rows}")
            print(f"   Schema:")
            
            for field in table_ref.schema:
                mode = field.mode or "NULLABLE"
                print(f"     - {field.name} ({field.field_type}, {mode})")
                
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure your credentials and project settings are correct")

if __name__ == "__main__":
    check_existing_tables()
