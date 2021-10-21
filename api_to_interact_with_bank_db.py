from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import jsonify, json

app = Flask(__name__)
api = Api(app)
# this will config the sqlite3 database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
db = SQLAlchemy(app)



# this will create the table that will hold the records
# it also defines the parameters for the fields that will be
# ...holding the values for each record
class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	fname = db.Column(db.String(100), nullable=False)
	lname = db.Column(db.String(100), nullable=False)
	chk_bal = db.Column(db.Integer, nullable=False)

	# this create a user-friendly string that will display to describe
	# ...a record from the database if it is called via code
	# def __repr__(self):
	# 	return f"member(name = {name}, views = {views}, likes = {likes})"

# YOU NEED TO RUN THE FUNCTION TO CREATE THE DATABASE!!!!!!!
# comment this line after the database has been created
# uncomment this line to create a new empty databse
# db.create_all()


# this dictionary will be used in conjunction with the "@marshal_with" module
# it defines how that module will convert an object into a serialized json object
mem_info_return = {
	'id': fields.Integer,
	'fname': fields.String,
	'lname': fields.String,
	'chk_bal': fields.Integer
}

total_bal_return = {
	'bank_bal': fields.Integer
}


# this creates an api endpoint to retreive data from the database based on the member id
# ...that was passed in the url
class MemInfo(Resource):
	@marshal_with(mem_info_return)
	def get(self, mem_id): # "mem_id" will hold the value to perform the query with
		result = Member.query.filter_by(id=mem_id).first() # this will return an object
		if not result:
			abort(404, message="Could not find member with that id")
		return result

class BankBalance(Resource):
	# bank_bal = 0
	# @marshal_with(total_bal_return)
	def get(self):
		bank_bal = 0
		accts = Member.query.all()
		# result = Member.query.filter_by(id=1).first()
		for acct in accts:
			bank_bal = acct.chk_bal + bank_bal
		return {"total bank balance": bank_bal}


class CreateNewMem(Resource):
	def post(self):
		new_mem = request.get_json()
		fname = new_mem['fname']
		lname = new_mem['lname']
		chk_bal = new_mem['chk_bal']

		new_mem_db = Member(fname=fname, lname=lname, chk_bal=chk_bal)
		db.session.add(new_mem_db)
		db.session.commit()
		return {"message": "member added"}
		
		


class InitiatNewDB(Resource):
	# bank_bal = 0
	# @marshal_with(total_bal_return)
	def get(self):
		db.create_all()
		return {"message": "New DB Initiated"}


	# def get(self):
	#     accts = Member.query.all()
	# 	for acct in accts:
	#     	bank_bal = acct.chk_bal + bank_bal
	#     # result = jsonify(accts)
	#     return bank_bal


# this ties the api endpoint to the a pattern that will be received in from the url request
# when the api receives a GET request with the following url:
#   - http://127.0.0.0:5000/member/2
# it will envoke the "member" class and pass the parameters from the request into that class for 
# ...further processing 
api.add_resource(MemInfo, "/member/<int:mem_id>")
api.add_resource(BankBalance, "/bank_bal")
api.add_resource(InitiatNewDB, "/initiatnewdb")
api.add_resource(CreateNewMem, "/createmem")

if __name__ == "__main__":
	# app.run(debug=True, host='0.0.0.0')
	app.run(debug=True)