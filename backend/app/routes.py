from flask import render_template, request, jsonify
from datetime import datetime

from . import db
from .models import Loan, Borrower, Repayment

def init_app(app):


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


    
    @app.route('/api/loans')
    def show_loans():
        """Homepage - show all loans"""
        try:
            loans = Loan.query.all()
            
            loan_list = []
            for loan in loans:
                loan_list.append({
                    'loan_id': loan.loan_id,
                    'borrower_id': loan.borrower_id,
                    'borrower_name': loan.borrower.full_name if loan.borrower else 'Unknown',
                    'principal_amount': loan.principal_amount,
                    'interest_rate': loan.interest_rate,
                    'total_due': loan.total_due,
                    'amount_paid': loan.amount_paid,
                    'balance': loan.balance,
                    'status': loan.loan_status,
                    'date_issued': loan.date_issued,
                    'due_date': loan.due_date,
                    'is_overdue': loan.is_overdue
                })
            
            # Debug: Print what we're sending to template
            print(f"Sending {len(loan_list)} loans to template")
            
            return render_template('index.html', loans=loan_list)
        except Exception as e:
            return f"Error loading loans: {str(e)}", 500
        
    @app.route ('/', methods = ['GET', 'POST'])
    def create_borrower():
        if request.method == 'GET':
            borrowers = Borrower.query.all()
            return render_template(template_name_or_list= 'index.html',borrowers=borrowers)
        elif request.method == 'POST':
            full_name = request.form.get('full_name')
            phone_number = str(request.form.get('phone_number'))
            id_number = str(request.form.get('id_number'))
            address = request.form.get('address')
            date_joined =None
            

            borrower = Borrower(
            full_name=full_name,
            phone_number=phone_number,
            id_number=id_number,
            address=address,
            date_joined=date_joined
            )
            db.session.add(borrower)
            db.session.commit()

            borrowers = Borrower.query.all()
            return render_template(template_name_or_list= 'index.html',borrowers=borrowers)

    
        

#api endpoint to get a loans of a specific borrower
    @app.route ('/api/loans/<int:id>', methods = ['GET'])
    def loan_by_borrower(id):

        loans = Loan.query.filter_by(borrower_id=id).all()

        loan_list = []
        for loan in loans:
            if id == loan.borrower_id:
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
