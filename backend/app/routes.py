from flask import jsonify, request
from datetime import datetime
from .models import db,Loan,Borrower,Repayment
from __init__ import app

@app.route ('/api/loans', methods = ['POST'])
def create_loan():
    data = request.json

    principal= float(data['principal_amount'])
    interest_rate = float(data['interest_rate'])
    total_due = principal * (1 + interest_rate /100)

    #SQL...
    new_loan = Loan(
        borrower_id = data['borrower_id'],
        principal_amount = principal,
        interest_rate = interest_rate,
        total_due = total_due,
        due_date = datetime.strptime(data['due_date'], '%Y-%m-%d').date()
    )

    db.session.add(new_loan)
    db.session.commit()

    return jsonify({
        'message' : 'Loan created',
        'loan_id' : new_loan.loan_id,
        'total_due' : new_loan.total_due,
        'balance' : new_loan.balance
    }), 201


@app.route('/api/loans/' , methods = ['GET'])
def show_loans():
    #API endpoint to get all loans

    loans = Loan.query.all()

    loan_list = []
    for loan in loans:
        loan_list.append({
            'loan_id' : loan.loan_id,
            'borrower_id' : loan.borrower_id,
            'borrower_name' : loan.borrower.full_name,
            'principal_amount': loan.principal_amount,
            'interest_rate' : loan.interest_rate,
            'total_due' : loan.total_due,
            'amount_paid' : loan.amount_paid,
            'balance' : loan.balance,
            'status' : loan.loan_status,
            'date_issued' : loan.date_issued.isoformat() if loan.date_issued else None,
            'due_date' : loan.due_date.isoformat() if loan.date_issued else None,
            'is_overdue' : loan.is_overdue
        }) 
        

    return jsonify({'loans' : loan_list})

