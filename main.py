from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from forms import UpdateForm, AddMovie
import requests

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)


app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-ten-movies.db"
# initialize the app with the extension
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(unique=True)
    year: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String(250))
    rating: Mapped[float] = mapped_column(Float)
    ranking: Mapped[int] = mapped_column(Integer)
    review: Mapped[str] = mapped_column(String(250))
    img_url: Mapped[str]= mapped_column(String(500))

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    # with app.app_context():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all()
    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()
    return render_template("index.html", movies=all_movies)

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_view(id):
    m_id = id
    movie = db.get_or_404(Movie, m_id)
    form  = UpdateForm()
    if request.method == 'POST':
        ratings = request.form.get('rating')
        reviews = request.form.get('review')
        # with app.app_context():
        # movie_to_update = db.session.execute(db.select(Movie).where(Movie.id == m_id)).scalar()
        movie.rating = ratings
        movie.review = reviews
        db.session.commit() 
        return redirect(url_for('home'))
    return render_template('edit.html', form=form, movie=movie)

@app.route('/delete/<int:id>')
def delete_it(id):
    m_id = id
    delete_movie = db.get_or_404(Movie, m_id)
    db.session.delete(delete_movie)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/add', methods=['GET','POST'])
def add_movie():
    add_form = AddMovie()
    if request.method == 'POST':
        with app.app_context():
            title = request.form.get('title')
            year = request.form.get('year')
            rating = request.form.get('rating')
            ranking = request.form.get('ranking')
            description = request.form.get('discription')
            review = request.form.get('review')
            img = request.form.get('img_url')
            new_movie = Movie(title=title , year=year , description=description, ranking=ranking ,rating=rating ,review=review , img_url=img)
            db.session.add(new_movie)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template('add.html', form=add_form)


if __name__ == '__main__':
    app.run(debug=True) 
