from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///users.db', echo=True)
 
app = Flask(__name__)
 
@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('welcome.html',USERNAME=session['user'])
 
@app.route('/login', methods=['POST'])
def do_admin_login():
 
	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
 
	Session = sessionmaker(bind=engine)
	s = Session()
	query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
	result = query.first()
	if result:
		session['logged_in'] = True
		session['user'] = POST_USERNAME
	else:
		flash('wrong password!')
	return home()
	
	
@app.route("/logout")
def logout():
	session['logged_in'] = False
	session.pop('pseudo', None)
	return home()	
	
@app.route('/test', methods=['GET'])
def test():
	if session['user']== "patrick":
		return render_template('test.html')	
	else:
		return render_template('deny.html',USERNAME=session['user'])
 
if __name__ == "__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True,host='0.0.0.0', port=4000)