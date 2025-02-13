import pandas as pd
from sqlalchemy import create_engine
import os
from time import time

def main():
    # PostgreSQL connection parameters
    user = "admin"
    password = "admin123"
    host = "localhost"
    port = "5432"
    db = "retail_store_sales"
    
    # Create SQLAlchemy engine
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    
    try:
        # Test connection
        with engine.connect() as conn:
            print("Successfully connected to the database!")
            
            # Example: Query the users table
            query = "SELECT * FROM users"
            df = pd.read_sql(query, conn)
            print("\nCurrent users in the database:")
            print(df)
            
    except Exception as e:
        print(f"Error connecting to the database: {e}")

def ingest_data():
    # Create SQLAlchemy engine
    engine = create_engine('postgresql://admin:admin123@localhost:5432/retail_store_sales')
    
    # Read CSV file
    df = pd.read_csv('./retail_store_sales.csv')
    df.columns = df.columns.str.replace(' ', '_')
    df.to_csv('retail_store_sales_cleaned.csv', index=False)
    df.Transaction_Date = pd.to_datetime(df.Transaction_Date)
    
    # Insert data into PostgreSQL
    df.to_sql('retail_store_sales', engine, if_exists='append', index=False)

if __name__ == "__main__":
    main()
    ingest_data() 