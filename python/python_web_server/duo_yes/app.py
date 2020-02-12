#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from sqlalchemy.orm import sessionmaker
from tabledef import *
engine = create_engine('sqlite:///users.db', echo=True)
import duo_web

# TODO : add you DUO credentials here under
ikey = 'iiiiiiiiiiiiiiiiiiiiiiii'
skey = 'ssssssssssssssssssssssss'
akey = 'aaaaaaaaaaaaaaaaaaaaaaaa'
host = 'hhhhhhhhhhhhhhhhhhhhhhhh'
 
app = Flask(__name__)
 
@app.route('/')
def home():
	if not session.get('logged_in'):
		return render_template('login.html')
	else:
		return render_template('welcome.html',USERNAME=session['user'])
 
@app.route('/login', methods=['POST'])
def do_admin_login():
	if request.form['sig_response'] == 'none' :
		session['logged_in'] = False
		POST_USERNAME = str(request.form['username'])
		POST_PASSWORD = str(request.form['password'])
	 
		Session = sessionmaker(bind=engine)
		s = Session()
		query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
		result = query.first()
		if result:
			session['logged_in'] = True
			session['user'] = POST_USERNAME
			sig_request = duo_web.sign_request(ikey, skey, akey,session['user'])
			return render_template('duo_mfa.html',host=host,sig_request=sig_request)
		else:
			session['logged_in'] = False
			flash('wrong password!')
	else:
		sig_response=request.form['sig_response']
		authenticated_username = duo_web.verify_response(ikey, skey, akey, sig_response)
		if authenticated_username:
			session['logged_in'] = True
			session['user']=authenticated_username
			return home()				
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