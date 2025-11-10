import pandas as pd
import sqlite3
import os

print("🚀 Starting to load Lending Club data...")

# Load first 2000 rows for better analysis
df = pd.read_csv("D:/loan_analysis/accepted_2007_to_2018Q4.csv", nrows=2000, low_memory=False)
print(f"✅ Loaded {len(df):,} loan records!")

# Select important columns
columns_we_need = [
    'loan_amnt', 'term', 'int_rate', 'grade', 'sub_grade', 'emp_length', 
    'home_ownership', 'annual_inc', 'loan_status', 'addr_state', 'issue_d',
    'purpose', 'dti', 'total_pymnt', 'recoveries', 'collection_recovery_fee'
]

df_clean = df[columns_we_need].copy()

# Clean data
df_clean['emp_length'] = df_clean['emp_length'].fillna('Not Provided')
df_clean['loan_status'] = df_clean['loan_status'].fillna('Unknown')

# Create SQLite database
conn = sqlite3.connect('loan_analysis.db')
df_clean.to_sql('lending_club_loans', conn, if_exists='replace', index=False)
conn.close()

print("🎉 SUCCESS! Data loaded to SQLite database!")
print(f"📊 Final dataset: {df_clean.shape}")