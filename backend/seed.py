import os
from datetime import datetime
from app import create_app, db
from app.models import User, Borrower, Loan, Repayment

# Delete old database (optional)
db_path = os.path.join(os.path.dirname(__file__), 'testdb.db')
if os.path.exists(db_path):
    os.remove(db_path)
    print("Old testdb.db deleted.")

# Create app and context
app = create_app()
with app.app_context():
    db.create_all()
    print("Database and tables created.")

    # Sample user
    user = User(username="staff", password_hash="hashed_password", full_name="Staff User")
    db.session.add(user)
    db.session.commit()

    # Sample borrower
    borrower = Borrower(full_name="John Doe", phone_number="0712345678", id_number="12345678", address="Nairobi")
    borrower = Borrower(full_name="Pat Separamoto", phone_number="0712345679", id_number="12345478", address="Gaborone")

    db.session.add(borrower)
    db.session.commit()

    # Sample loan
    loan = Loan(
        borrower_id=borrower.borrower_id,
        principal_amount=10000.0,
        interest_rate=10.0,
        total_due=11000.0,
        amount_paid=0.0,
        due_date=datetime(2025, 12, 31).date(),
        created_by=user.user_id
    )
    loan = Loan(
        borrower_id=borrower.borrower_id,
        principal_amount=12000.0,
        interest_rate=15.0,
        total_due=13800.0,
        amount_paid=0.0,
        due_date=datetime(2025, 12, 31).date(),
        created_by=user.user_id
    )
    db.session.add(loan)
    db.session.commit()

    # Sample repayment
    repayment = Repayment(
        loan_id=loan.loan_id,
        amount_paid=2000.0,
        payment_method="cash",
        recorded_by=user.user_id
    )
    db.session.add(repayment)
    db.session.commit()

    print("✅ Sample data inserted successfully!")
