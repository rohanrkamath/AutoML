
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

from flask_login import current_user
from myproject.models import User

class LoginForm(FlaskForm):
    email = StringField('Email: ',validators=[DataRequired(),Email()])
    password = PasswordField('Password: ',validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name: ',validators=[DataRequired()])
    last_name = StringField('Last Name: ',validators=[DataRequired()])
    email = StringField('Email: ',validators=[DataRequired(),Email()])
    phone_no = IntegerField('Phone Number: ',validators=[DataRequired()])
    company_name = StringField('Company Name: ', validators=[DataRequired()])
    username = StringField('UserName: ',validators=[DataRequired()])
    password = PasswordField('Password: ',validators=[DataRequired(),EqualTo('pass_confirm',message='Passwords must match!')])
    pass_confirm = PasswordField('Confirm Password: ',validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Your username has been registered already!')
