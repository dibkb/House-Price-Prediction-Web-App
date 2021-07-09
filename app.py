from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for,request
from datetime import datetime
import pickle
import os
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'u23t4y2g4hj323e32xi4y234234bk3r54a*43uyy4d'

#comment this part in development

uri = os.getenv("DATABASE_URL")  
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

#load the preprocessor and model
scaler = pickle.load(open('pickle/scaler.pkl', 'rb'))
regr = pickle.load(open('pickle/svr.pkl', 'rb'))

ENV = 'prod'

if ENV == 'dev':
   app.debug = True
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' 
else:
   app.debug = False
   app.config['SQLALCHEMY_DATABASE_URI'] = uri  

db = SQLAlchemy(app)

#Database model
class User(db.Model):
   id = db.Column(db.Integer,primary_key = True)
   name = db.Column(db.String(120),unique = False, nullable = False)
   date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

   def __repr__(self):
       return f"User('{self.name}',{self.date_posted})"



#define routes
@app.route('/')
@app.route('/home')
def home():
   return render_template('home.html')



@app.route('/form',methods = ['GET','POST'])
def form():
   if request.method == 'POST':

      
      # append the data to dictionary
      user = User(name = request.form['name'])
      db.session.add(user)
      db.session.commit()

      #prediction
      # make a numpy arrat in this format
      # Avg. Area Income	Avg. Area House Age	Avg. Area Number of Rooms	Avg. Area Number of Bedrooms	Area Population
      data = np.array([
         float(request.form['area_income'])*1000 ,
         request.form['house_age'],
         request.form['rooms'],
         request.form['bed_rooms'],
         float(request.form['area_population'])*1000
      ]).reshape(1,-1)
      
      #grab only the integer value
      pred = np.expm1(regr.predict(scaler.transform(data)))[0]
      return render_template('result.html',pred = pred,name = request.form['name'])
   return render_template('form.html')



@app.route('/form_mobile',methods = ['GET','POST'])
def formMobile():
   if request.method == 'POST':

      
      # append the data to dictionary
      user = User(name = request.form['name'])
      db.session.add(user)
      db.session.commit()

      #prediction
      # make a numpy arrat in this format
      # Avg. Area Income	Avg. Area House Age	Avg. Area Number of Rooms	Avg. Area Number of Bedrooms	Area Population
      data = np.array([
         float(request.form['area_income'])*1000 ,
         request.form['house_age'],
         request.form['rooms'],
         request.form['bed_rooms'],
         float(request.form['area_population'])*1000
      ]).reshape(1,-1)
      
      #grab only the integer value
      #grab only the integer value
      pred = np.expm1(regr.predict(scaler.transform(data)))[0]
      return render_template('result.html',pred = pred,name = request.form['name'])
   return render_template('form(mobile).html')



if __name__ == '__main__':
    app.run()