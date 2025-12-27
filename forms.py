from flask_wtf import FlaskForm 
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 


class AddTaskForm(FlaskForm):
  
    title = StringField ('Enter your wish here',validators= [DataRequired()] )
   
    submit = SubmitField('Send your wish to Santa!')

