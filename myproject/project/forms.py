from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField, RadioField, TextAreaField
from wtforms.fields.html5 import IntegerRangeField
from wtforms.validators import DataRequired, Optional
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask_login import current_user

# questionaire 

class ProjectForm(FlaskForm):
    project_name = StringField('Please enter the name of the project: ',validators=[DataRequired()])
    description = TextAreaField('Description: ', validators=[Optional()])
    upload_file = FileField('Select Video: ', validators=[FileAllowed(['mp4'])]) #FileRequired()
    # get_info = SubmitField('Details about the video uploaded')
    select_gpu = RadioField(u'Select GPU: ', choices=[('4gb', '4GB'), ('8gb', '8GB'), ('12gb', '12GB')])
    compute_hrs = IntegerRangeField('Select Compute time: ', validators=[DataRequired()])
    '''q1 = TextAreaField('What is your name?') # , validators=[DataRequired()]
    q2 = TextAreaField('What is your age?')
    q3 = RadioField(u'Do you like cats?', choices=[('yes', 'Yes'), ('no', 'No')])'''
    start_training = SubmitField('Start Training!')












