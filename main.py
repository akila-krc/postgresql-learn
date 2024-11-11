from flask import Flask, request, redirect, url_for, render_template
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5


app = Flask(__name__)
app.config['SECRET_KEY']="8BYkEfBA6O6donzWlSihBXox7C0sKR6b"


# CREATE DATABASE
class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///postgresql-test.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

Bootstrap5(app)

# Create a User table for all your registered users
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


with app.app_context():
    db.create_all()

class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField(label='Submit')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UserForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = request.form['name']
        print(name)
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return render_template('success.html')

    return render_template('user.html', form=form)


if __name__ == "__main__":
    app.run(debug=True)