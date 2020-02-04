# How to setup DUO secondary authentication to your Python web server

# 0/ Install a Python Interpreter

	- First of all you must have a Python Interpreter installed into your lab laptop.
	- Go to www.python.org in order to download and install Python on your laptop
	- Install a version 3.x version ( it will work with python version 2 as well )

# 1/ Download a Simple DUO Python Sample

- Go to DUO Web documentation https://duo.com/docs/duoweb
- Go to the [ First Steps ] chapter and follow all instruction described in steps 1, 2 and 3
- In Step 4 click on the Pyton Link. It will redirect you to the Github repository where are located all Python resources you need.
	- Click on the [ clone or Download ] button and Download zip
	- Unzip the retreived zip file ( duo_python-master.zip )
	- then goto to the [ duo_python-master\demos\simple ] folder
	- We assume here that you previously rolled out the PHP lab.
		- And normally you have generated in your DUO Account all the credentials we need to make this demo works
	- install needed python modules
		- pip install requirements.txt
	- Modify the duo.conf file
	- Then run the web server : 
		- python server.py
	- The Web server is ready

# 2/ Test it

	- Open your browser on the following location
		- http://localhost:8080/?user=myname
	- Your probably know what to do next