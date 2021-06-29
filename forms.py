from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField
from wtforms.validators import DataRequired



class Form(FlaskForm):
    FileName = FileField("File to upload: ", validators=[DataRequired()])
    MainColor = IntegerField("Number of Colors: ", validators=[DataRequired()])

    submit = SubmitField("Upload")


