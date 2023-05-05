from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from datetime import timedelta
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = "hello"
app.permanant_session_lifetime = timedelta(days=5)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))


app.app_context().push()

#initializes the user details in the database
class User(db.Model, UserMixin):
     id = db.Column(db.Integer, primary_key=True)
     username = db.Column( db.String(20), nullable=False, unique=True)
     password = db.Column(db.String(80), nullable=False)

#inputs for the registration form and its validation
class RegisterForm(FlaskForm):
     username = StringField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Username"})
     
     password = PasswordField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Password"})
     
     submit = SubmitField("Register")

     #username validation
     def validate_username(self, username):
          existing_user_username = User.query.filter_by(
               username = username.data).first()
          if existing_user_username:
               raise ValidationError(
                    "That username already exists. Please choose a different one."
               )   


#inputs for the login form
class LoginForm(FlaskForm):
     username = StringField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Username"})
     
     password = StringField(validators=[InputRequired(), Length(
          min=4, max=20)], render_kw={"placeholder": "Password"})
     
     submit = SubmitField("Login")



#returns the homepage with the retrieved prediction from the text file
@app.route('/homepage', methods = ["POST", "GET"])
#@login_required
def homepage():
    with open('output.txt', 'r') as f:
        data = f.read()
    date = data.split(',')[0].split(':')[1].strip()
    price = data.split(',')[1].split(':')[1].strip()
    return render_template('HomePage.html', date=date, price=price)

#return the landing page
@app.route('/')
def landingpage():
    return render_template('LandingPage.html')

#returns the login page with the login form
@app.route("/login", methods = ["POST", "GET"])
def login():
        form = LoginForm()
        if form.validate_on_submit():
             user = User.query.filter_by(username=form.username.data).first()
             if user:
                  if bcrypt.check_password_hash(user.password, form.password.data):
                       login_user(user)
                       return redirect(url_for('homepage'))
        return render_template('LoginPage.html', form=form)


#returns the registration page with the form
@app.route("/register")
def register():
        form = RegisterForm()

          #form validation
        if form.validate_on_submit():
             hashed_password = bcrypt.generate_password_hash(form.password.data) #hashed password
             new_user = User(username=form.username.data, password=hashed_password) #creates a new user
             db.session.add(new_user)#adds the user to the database
             db.session.commit()
             return redirect(url_for('login'))

        return render_template('RegisterPage.html', form=form)
    
#returns the about page
@app.route("/aboutpage")
def aboutpage():
            return render_template('AboutPage.html')

#logout function and return to the login page
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for("login"))
    

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)


