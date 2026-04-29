# Handles loading leads from CSV and storing them in SQLite.
# Also provides functions to add new leads manually.

import sqlite3
import pandas as pd
import os
from datetime import datetime

# Path to SQLite database file
DB_PATH = "db/leads.db"

# Function to create a connection to the SQLite database
def get_connection():
    
    os.makedirs("db", exist_ok=True)
    return sqlite3.connect(DB_PATH)

# Function to initialize the database and create the leads table if it doesn't exist
def initialize_database():
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            company TEXT,
            email TEXT,
            phone TEXT,
            source TEXT,
            country TEXT,
            industry TEXT,
            product_interest TEXT,
            budget_usd REAL,
            company_size TEXT,
            notes TEXT,
            created_at TEXT,
            score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Unqualified',
            score_reason TEXT DEFAULT '',
            chat_summary TEXT DEFAULT '',
            sales_note TEXT DEFAULT ''
        )
    """)
    
    conn.commit()
    conn.close()

# Function to load leads from a CSV file into the database
def load_csv_to_db(csv_path="data/sample_leads.csv"):
    
    conn = get_connection()
    df = pd.read_csv(csv_path)
    
    inserted = 0
    for _, row in df.iterrows():
        # Check if email already exists in the database
        existing = pd.read_sql(
            "SELECT id FROM leads WHERE email = ?", 
            conn, 
            params=(row['email'],)
        )
        
        if existing.empty:
            # Insert the lead (without the CSV's id — let SQLite auto-assign one)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO leads 
                (name, company, email, phone, source, country, industry, 
                 product_interest, budget_usd, company_size, notes, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['name'], row['company'], row['email'], row['phone'],
                row['source'], row['country'], row['industry'],
                row['product_interest'], row['budget_usd'],
                row['company_size'], row['notes'], row['created_at']
            ))
            inserted += 1
    
    conn.commit()
    conn.close()
    return inserted

# Function to retrieve all leads from the database as a pandas DataFrame
def get_all_leads():
    
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM leads ORDER BY id DESC", conn)
    conn.close()
    return df

# Function to retrieve a single lead by its ID
def get_lead_by_id(lead_id):
  
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM leads WHERE id = ?", conn, params=(lead_id,))
    conn.close()
    if df.empty:
        return None
    return df.iloc[0].to_dict()

# Function to add a new lead entered manually through the UI
def add_lead_manually(name, company, email, phone, source, country,
                      industry, product_interest, budget_usd, company_size, notes):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO leads 
        (name, company, email, phone, source, country, industry,
         product_interest, budget_usd, company_size, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name, company, email, phone, source, country, industry,
        product_interest, float(budget_usd), company_size, notes,
        datetime.now().strftime("%Y-%m-%d")
    ))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

# Function to update the scoring result for a lead
def update_lead_score(lead_id, score, status, score_reason):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leads SET score = ?, status = ?, score_reason = ?
        WHERE id = ?
    """, (score, status, score_reason, lead_id))
    conn.commit()
    conn.close()

# Function to update the AI chat summary for a lead
def update_lead_chat(lead_id, chat_summary):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leads SET chat_summary = ? WHERE id = ?
    """, (chat_summary, lead_id))
    conn.commit()
    conn.close()

# Function to update the sales handoff note for a lead record
def update_lead_sales_note(lead_id, sales_note):

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leads SET sales_note = ? WHERE id = ?
    """, (sales_note, lead_id))
    conn.commit()
    conn.close()