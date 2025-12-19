import sqlite3
import os

print("Creating SQLite database manually...")

# Create connection - this creates the file
conn = sqlite3.connect('testdb.db')
cursor = conn.cursor()

# Create tables manually
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    role TEXT DEFAULT 'staff',
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS borrowers (
    borrower_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone_number TEXT,
    id_number TEXT UNIQUE,
    address TEXT,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY,
    borrower_id INTEGER NOT NULL,
    principal_amount REAL NOT NULL,
    interest_rate REAL NOT NULL,
    total_due REAL NOT NULL,
    amount_paid REAL DEFAULT 0.0,
    loan_status TEXT DEFAULT 'active',
    date_issued TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    created_by INTEGER,
    FOREIGN KEY (borrower_id) REFERENCES borrowers (borrower_id),
    FOREIGN KEY (created_by) REFERENCES users (user_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS repayments (
    repayment_id INTEGER PRIMARY KEY,
    loan_id INTEGER NOT NULL,
    amount_paid REAL NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method TEXT DEFAULT 'cash',
    recorded_by INTEGER,
    FOREIGN KEY (loan_id) REFERENCES loans (loan_id),
    FOREIGN KEY (recorded_by) REFERENCES users (user_id)
)
''')

# Add some test data
cursor.execute("INSERT INTO users (username, password_hash, full_name, role) VALUES ('admin', 'hash123', 'Admin User', 'admin')")
cursor.execute("INSERT INTO borrowers (full_name, phone_number, id_number, address) VALUES ('Test Borrower', '0712345678', '12345678', 'Test Address')")
cursor.execute("INSERT INTO loans (borrower_id, principal_amount, interest_rate, total_due, due_date, created_by) VALUES (1, 1000, 10, 1100, '2024-12-31', 1)")

conn.commit()
conn.close()

print(f"✓ Database created: testdb.db")
print(f"✓ File size: {os.path.getsize('testdb.db')} bytes")
print(f"✓ Location: {os.path.abspath('testdb.db')}")