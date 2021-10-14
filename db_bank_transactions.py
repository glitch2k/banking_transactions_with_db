from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
# this will config the sqlite3 database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)



# this will create the table that will hold the records
# it also defines the parameters for the fields that will be
# ...holding the values for each record
class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(100), nullable=False)
	lname = db.Column(db.String(100), nullable=False)
	chk_bal = db.Column(db.Integer, nullable=False)

# YOU NEED TO RUN THE FUNCTION TO CREATE THE DATABASE!!!!!!!
# comment this line after the database has been created
# uncomment this line to create a new empty databse
# db.create_all()


# define the transaction python classes that will be used to interact with the
# ...member's acct balance

# every banking transaction will get its own class

# every time a transaction needs to be made on a member's acct (deposit)
# ...an object of that particular transaction will be created from its class

# that object will be made using arguments coming from the member's object

# that transaction object will have 1 method to perform the logic & calculation 
# ...to the member's balance

# once the member's new balance has been updated to its in-memory object, that
# ...method will also perform the commit action to save the member's updated in-memory
# ...object into the db

# class for creating deposit objects to perform deposit 
# ...transactions to member's account
class Transaction():
    def __init__(self, id, fname, lname, chk_bal, amt):
        self.id = id
        self.fname = fname
        self.lname  = lname
        self.chk_bal = chk_bal
        self.trans_amt = amt 

    def show_details(self):
        print("Personal Details")
        print("")
        print("First Name ", self.fname)
        print("Last Name  ", self.lname)
        print("Checking Account Balance ", self.chk_bal)

    def deposit(self):
        self.chk_bal = self.chk_bal + self.trans_amt
        mem.chk_bal = self.chk_bal
        db.session.commit()
        verify = Member.query.filter_by(id=mem_id).first()
        print('\n' *2)
        print(verify.fname)
        print(verify.lname)
        print(verify.chk_bal)

    def withdraw(self):
        # verify if member has enough money to perform withdraw
        if self.trans_amt > self.chk_bal:
            print('the member does not have enough money to perform this withdraw')
            print('please ensure withdraw amount is less than member\'s balance displayed below')
            print(self.chk_bal)
            print('\n' *5)
            return
        else:
            self.chk_bal = self.chk_bal - self.trans_amt
            mem.chk_bal = self.chk_bal
            db.session.commit()
            verify = Member.query.filter_by(id=mem_id).first()
            print('\n' *2)
            print(verify.fname)
            print(verify.lname)
            print(verify.chk_bal)
            print('\n' *5)
            return







    



# main-menu-01 logic
# ******************

print('member transaction => a')
print('')
print('add new member     => b')

menu_1 = input('enter choice : ')

if menu_1 == 'a':

    # request to enter member's id 
    print('enter member\'s id')
    mem_id = input(': ') 
    # use 'mem_id' to query db for member's object and store
    # ...it in memory with a variable
    mem = Member.query.filter_by(id=mem_id).first()
    print('\n' * 2)
    print(mem.id)
    print(mem.fname)
    print(mem.lname)
    print(mem.chk_bal)

    # main-menu-02 logic
    # ******************

    print('for member deposit => a')
    print('')
    print('for member withdraw     => b')
    menu_2 = input('enter choice : ')

    # CODE TO PERFORM A DEPOSIT
    if menu_2 == 'a':
        # request amount to deposit
        print('enter amount member is depositing')
        dep_amt = int(input(': '))

        # create deposit object with member in-memory object & the amount entered
        # ...by user, then perform the deposit action using the deposit method,
        # ...update the member's in-memory object accont balance property,
        # ... then commit the member's in-memory object into the db

        trans_obj = Transaction(mem.id, mem.fname, mem.lname, mem.chk_bal, dep_amt)
        trans_obj.deposit()

    # CODE TO PERFORM A WITHDRAW
    if menu_2 == 'b':
        # request amount to withdraw
        print('enter amount member is withdrawing')
        dep_amt = int(input(': '))

        # create deposit object with member in-memory object & the amount entered
        # ...by user, then perform the deposit action using the deposit method,
        # ...update the member's in-memory object accont balance property,
        # ... then commit the member's in-memory object into the db

        trans_obj = Transaction(mem.id, mem.fname, mem.lname, mem.chk_bal, dep_amt)
        trans_obj.withdraw()
    



    






if menu_1 == 'b':
    # request all required information to create a new member's acct
    print('enter new member\'s first name')
    mem_fname = input(': ')
    print('')
    print('enter new member\'s last name')
    mem_lname = input(': ')
    print('')
    print('enter staring balance')
    mem_strt_bal = input(': ')
    print('')

    # create a db member object with the information given 
    # ...and save the db object to the db
    db_mem = Member(fname=mem_fname, lname=mem_lname, chk_bal=mem_strt_bal)
    db.session.add(db_mem)
    db.session.commit()