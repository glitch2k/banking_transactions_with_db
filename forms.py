from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField

class CreateMem(FlaskForm):
    fname = StringField('Member First Name')
    lname = StringField('Member Last Name')
    chk_bal = IntegerField('Starting Balance')
    submit = SubmitField('Create Member Acct')
