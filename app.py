from flask import Flask, render_template, request, redirect, url_for, session, flash, escape
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_mysqldb import MySQL, MySQLdb
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
import pandas as pd
from sklearn.model_selection import train_test_split 

import bcrypt 
import pickle

app = Flask(__name__)
app.secret_key = "membuatLOginFlask1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost:3307/fypdb'
db = SQLAlchemy(app)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



tfvect = TfidfVectorizer(stop_words='english', max_df=0.7)

# Load Pickle model
loaded_model = pickle.load(open('model.pkl', 'rb'))


#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_PORT'] = '3307'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'fypDB'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#mysql = MySQL(app) 

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,name, email, password):
        
        self.name = name
        self.email = email
        self.password = password


class Sentiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), unique=True)
    label = db.Column(db.String(1000), unique=True)
    user_email = db.Column(db.String(1000), unique=True)
   

    def __init__(self,text, label,user_email ):
        
        self.text = text
        self.label = label
        self.user_email = user_email
  
class Feedback(db.Model):
    id =db.Column(db.Integer, primary_key=True)
    userMail = db.Column(db.String(1000), unique=True)
    sentiment_id = db.Column(db.Integer, unique=True)

    def __init__(self,user_email,sentiment_id):
        self.user_email = user_email
        self.sentiment_id = sentiment_id

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

# We need to fit the TFIDF VEctorizer
dataframe = pd.read_csv('news.csv')
x = dataframe['text']
y = dataframe['label']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

def fake_news_det(news):
    tfid_x_train = tfvect.fit_transform(x_train)
    tfid_x_test = tfvect.transform(x_test)
    input_data = [news]
    vectorized_input_data = tfvect.transform(input_data)
    prediction = loaded_model.predict(vectorized_input_data)
    return prediction


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('prediction'))
        else:
            
            return "invalid email or password"
    return render_template("login.html")

@app.route('/prediction', methods=['GET', 'POST'])
@login_required
def prediction():
        
        if request.method == "POST":
            news = str(request.form['news'])
            print(news)
            pred = fake_news_det(news) 
            return render_template('prediction.html', prediction=pred)
        else:
            return render_template('prediction.html',prediction="Something went wrong")



@app.route('/addlabel', methods=['POST', 'GET'])
def addlabel():
    if request.method == 'POST':
        
            db.session.add(Sentiment(text=request.form['news'],label=request.form['label'],user_email=request.form['user_id']))
            db.session.commit()
            return redirect(url_for('prediction'))
    else:
        return render_template('404.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        db.session.add(Users(name=request.form['name'],email=request.form['email'], password=request.form['password']))
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')



@app.route('/portfolio')
def portfolio():
    id = current_user.id
    return render_template('portfolio.html',)
    
     
@app.route('/contact')
def contact():
    if 'email' in session:
        return render_template("contact.html")
    else:
        return redirect(url_for('home')) 
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home')) 

#update employee
@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = Users.query.get(request.form.get('id'))
  
        my_data.name = request.form['name']
        my_data.email = request.form['email']
        my_data.password = request.form['password']
        my_data.repassword = request.form['repassword']
  
        db.session.commit()
        flash("Employee Updated Successfully")
        return redirect(url_for('portfolio'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)