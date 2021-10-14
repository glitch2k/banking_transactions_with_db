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

    # this create a user-friendly string that will display to describe
    # ...a record from the database if it is called via code
	# def __repr__(self):
	# 	return f"Video(name = {name}, views = {views}, likes = {likes})"

# YOU NEED TO RUN THE FUNCTION TO CREATE THE DATABASE!!!!!!!
# comment this line after the database has been created
# uncomment this line to create a new empty databse
# db.create_all()


# this dictionary will be used in conjunction with the "@marshal_with" module
# it defines how that module will convert an object into a serialized json object
resource_fields = {
	'id': fields.Integer,
	'fname': fields.String,
	'lname': fields.String,
	'chk_bal': fields.Integer
}

# this boc will parse thru the parameters sent in the PUT request to make sure that
# ...they are valid entries
# it even sends a custom error message when an invalid parameter is sent
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

# this creates an api endpoint to retreive data from the database based on the video id
# ...that was passed in the url
class Video(Resource):
	@marshal_with(resource_fields)
	def get(self, video_id): # "video_id" will hold the value to perform the query with
		result = Member.query.filter_by(id=video_id).first() # this will return an object
		if not result:
			abort(404, message="Could not find video with that id")
		return result


	@marshal_with(resource_fields)
	def put(self, video_id):
		
		# this boc will parse thru the parameters sent in the PUT request to make sure that
		# ...they are valid entries
		# it even sends a custom error message when an invalid parameter is sent
		video_put_args = reqparse.RequestParser()
		video_put_args.add_argument("name", type=str, help="Name of the video is required", required=True)
		video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
		video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

		# once all are parameters are validated, the resultant parameters are saved in the "args"
		# ...variable as an object "most likely a python dict"
		args = video_put_args.parse_args()

		# this boc queries the db to verify if the record that needs to be created does not exist
		# ...in the db
		# if it is not present, the PUT request is aborted and a custom message is sent back
		result = Member.query.filter_by(id=video_id).first()
		if result:
			abort(409, message="Video id is already taken... Choose another id...")

		# once it is verified that the record does not exist, a sqlalchemy object representing the
		# ...record is created using the "Member" class
		# the properties for that object will come from the "args" object
		# the sqlalchemy object representing the record is saved in the variable "video"
		video = Member(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
		# the record is sent to the db with the "db.session.add" method with the "video" object used as
		# ...a parameter of that method
		db.session.add(video)
		db.session.commit()
		return video, 201


# this ties the api endpoint to the a pattern that will be received in from the url request
# when the api receives a GET request with the following url:
#   - http://127.0.0.0:5000/video/2
# it will envoke the "Video" class and pass the parameters from the request into that class for 
# ...further processing 
api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
	app.run(debug=True)