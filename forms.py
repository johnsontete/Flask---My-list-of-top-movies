from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, DateField, IntegerField
from wtforms.validators import DataRequired

class UpdateForm(FlaskForm):
    rating = StringField("Your Rating out of 10", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")


class AddMovie(FlaskForm):
    title = StringField('Movie Name',validators=[DataRequired()])
    year = DateField('Year', format="%Y-%m-%d",validators=[DataRequired()])
    discription = StringField('Description',validators=[DataRequired()])
    rating = FloatField('Rating',validators=[DataRequired()])
    ranking = IntegerField('Ranking',validators=[DataRequired()])
    review = StringField('Review',validators=[DataRequired()])
    img_url = StringField('Image',validators=[DataRequired()])
    submit = SubmitField("Add Movie")