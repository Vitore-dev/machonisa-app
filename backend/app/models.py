from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

#staff table
class User(db.Model):
    __tablename__='users'

    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique = True,nullable=False)
    password_hash = db.Column(db.string(200),nullable = False)
    full_name = db.Column(db.String(100),nullable = False)
    role = db.Column(db.String(20),default = 'staff')
    creation_date = db.Column(db.Datetime,default = datetime.catnow)

    loans_created = db.relationship('loan',backref = 'creator' , lazy=True)

#Borrowers table
class Borrower(db.model):
    __tablename__ = 'borrowers'

    borrower_id = db.Column(db.Integer , primary_key=True)
    full_name = db.Column(db.String(100),nullable = False)
    phone_number = db.Column(db.String(20))
    id_number = db.Column(db.String(50),unique = True)
    address = db.Column(db.Text)
    date_joined = db.Column(db.Datetime, default = datetime.catnow)

    loans = db.relationship('Loan', backref = 'borrower' , lazy = True)


#loans table
class Loan(db.Model):
    __tablename__ = 'loans'

    loan_id = db.Column(db.integer,primary_key = True)
    borrower_id = db.Column(db.Integer , db.ForeignKey('borrowers.borrower_id'),nullable = False)

    principal_amount = db.Column(db.Float,nullable = False)
    interest_rate = db.Column(db.Float, nullable = False)
    total_due = db.Column(db.Float, nullable = False)
    amount_paid = db.Column(db.Float, default = 0.0)

    loan_status = db.Column(db.String(20),default = 'active')
    date_issued = db.Column(db.Datetime, default = datetime.catnow)
    due_date = db.Column(db.Date, nullable = False)
    

    created_by = db.Column(db.Integer,db.ForeignKey('users.user_id'))

    repayments = db.relationship('Repayment',backref = 'loan' , lazy = True)


    @property
    def balance(self):
        return self.total_due - self.amount_paid
    
    @property
    def is_overdue(self):
        return datetime.catnow().date()>self.due_date and self.balance > 0
    
#repayments date
class Repayment(db.model):
    __tablename__ = 'repayments'

    repayment_id = db.Column(db.Integer , primary_key=True)
    loan_id = db.Column(db.Integer, db.ForeignKey('loans.loan_id'),nullable = False)

    amount_paid = db.Column(db.Float , nullable=False)
    payment_date = db.Column(db.Datetime, default = datetime.catnow)
    payment_method = db.Column(db.String(20), default = 'cash')

    recorded_by = db.Column(db.Integer, db.ForeignKey('users.user_id'))
   