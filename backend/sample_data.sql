-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- ======================================
-- Create tables
-- ======================================
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    password_hash VARCHAR(200) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'staff',
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS borrowers (
    borrower_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    id_number VARCHAR(50) UNIQUE,
    address TEXT,
    date_joined DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    borrower_id INTEGER NOT NULL,
    principal_amount REAL NOT NULL,
    interest_rate REAL NOT NULL,
    total_due REAL NOT NULL,
    amount_paid REAL DEFAULT 0.0,
    loan_status VARCHAR(20) DEFAULT 'active',
    date_issued DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATE NOT NULL,
    created_by INTEGER,
    FOREIGN KEY (borrower_id) REFERENCES borrowers(borrower_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS repayments (
    repayment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    amount_paid REAL NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    payment_method VARCHAR(20) DEFAULT 'cash',
    recorded_by INTEGER,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id),
    FOREIGN KEY (recorded_by) REFERENCES users(user_id)
);

-- ======================================
-- Insert sample data
-- ======================================

INSERT INTO users (username, password_hash, full_name, role)
VALUES ('admin', 'hashed_password_here', 'Admin User', 'admin');

INSERT INTO borrowers (borrower_id ,full_name, phone_number, id_number, address)
VALUES ('1' ,'John Doe', '0712345678', '12345678', 'Nairobi');

INSERT INTO loans (borrower_id, principal_amount, interest_rate, total_due, amount_paid, due_date, created_by)
VALUES (1, 10000.00, 10.0, 11000.00, 0.0, '2025-12-31', 1);

INSERT INTO repayments (loan_id, amount_paid, payment_method, recorded_by)
VALUES (1, 2000.00, 'cash', 1);

INSERT INTO users (user_id ,username, password_hash, full_name, role)
VALUES ('2','staff', 'hashed_password', 'Staff User', 'staff');