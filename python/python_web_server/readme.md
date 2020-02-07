# DUO MFA integration into a Python Flask Proof Of Concept Web Server

	- The goal of this proof of concept is to show an example of a DUO secondary Authentication into a Python Flask Web Server Application.
	- You will find into the [ duo_no ] folder the Flask Application without DUO MFA
	- And you will find into the [ duo_yes ] folder the same Flask Application then with DUO MFA
	
# 1 / Test the duo_no Application

- Download and unzip all the code into your development laptop
- open a shell cmd window into the [ duo_no ] folder and run the application
	- python app.py
- Then open your browser to  http://localhost:4000
- Authenticate with username = patrick , password = password
- Remarks
	- users are store into a sqlite database : users.bd
	- you can change the content of this database just by deleting it, and after use the add_users.py script ( open it to understand how to use it )
	
# 2 / Add DUO MFA to this Flask Application

- We assume here that you previously rolled out the DUO WEB PHP lab.
	- And normally if you did it you have generated in your DUO Account, the credentials ( ikey, skey, akey and host ) you need to make this demo work
- You have a fully functionnal solution in the [ duo_yes ] folder. But let's have a look to how to modify the [ duo_no ] application in order to acheive our goal.
- create a new directory called [ duo_yes ] and copy and paste into it all the content of the [ duo_no ] directory
- Go to DUO Web documentation https://duo.com/docs/duoweb
- If not already done, Go to the [ First Steps ] chapter and follow all instruction described in steps 1, 2 and 3
- In Step 4 click on the Pyton Link. It will redirect you to the Github repository where are located all Python resources you need.
	- Click on the [ clone or Download ] button and Download zip
	- Unzip the retreived zip file ( duo_python-master.zip )
	- Find in this directory tree the Duo-Web-v2.js and Duo-Frame.css files. Copy these two file into the newly created [ duo_yes/static ] folder
- Open and modify the app.py script
	- Here are some explanations to understand what we have to do.
		- In the previous labs ( the PHP one ) you probably understood that we have to include into the part of your programm which check the username / password authentication, instead of going to the authorized landing page, you include a call of the DUO MFA. And for doing this you just have to insert the html iframe example given into the documentation https://duo.com/docs/duoweb.
		- In this iframe you must set correctly some arguments.
			- give correct path to the locations into you own application where you copied the Duo-Web-v2.js and Duo-Frame.css files ( /static/ )
			- pass two important variables : host and sig_request
			- the sig_request variable is built by the DUO sign in request function which uses your DUO credentials
		- When this iframe is correctly defined, after the first authentication into your login page, you should see a blank page appearing with in the middle the DUO MFA PUSH Page.
			- Remark, if you see appearing an empty IFRAME, that means that host and sig_request are not correctly defined ( check that you passed correct DUO credentials
		- If the IFRAME correctly appear and if you are able to click on the push button, well done, you are able to double authenticate with your mobile.
		- Do it and approve the authentication
		- What happens at this point, as mentionned in the documentation : The IFRAME will generate a signed response called sig_response and POST it back to the post_action URL ( If we don't define a post_action, we will come back to the page which called the IFRAME
		- Your server-side code should then call verify_response() to verify that the signed response is legitimate.
		- Finally if the signed response is legitimate, then go the the authorized landing page and that's it !
	- So the question is now how to integrate this whole process into our code. Let's have a look
	- You are editing the app.py file
	- on the top of it add the  import duo_web statement. We will use the duo_web python module
	- Add some where the DUO Credential ( I just defined them as global variables, a configuration file should be better )
	- You have only to modify the route called : def do_admin_login():.  This is this function which check username / password and which route to the landing page
	- First in this function we check if the sig_response variable is equal or not to none.( remember this variable is returned back the DUO MFA and when we arrived the first time to the do_admin_login() function, this variable is not set as we didn't call yet DUO MFA.
	- So in order to get an error there, we defined this variable in the login.html page.
	- Open login.html page and insert into the authentication form the sig_response = 'none'
	- This will allow the if condition to go the the username / password validation from the original code, and if success, we call the duo_web.sign_request(ikey, skey, akey,session['user']) function, and we pass the result as the sig_request variable to the return statement, we add the host variable as well to that statement.
	- Finally we call the duo_mfa.html and we pass to it the sig_request and host variables
	- Create the duo_mfa.html into the /templates/ folder. Use the example given into the [ duo_yes ] github repo
	- Open it and have a look at it. This is just the IFRAME with correct variable statements
	- Whe DUO MFA is done, the program comes back to the do_admin_login() route. But now the sig_response is set by DUO MFA
	- That means that we come back the begining of the if condition and then we go to the else statements
	- There we verify the DUO response ( sig_response ) and then we continue on the original procedure
	- The user is logged into his landing page.
