# How to setup DUO secondary authentication into your web server

## 0/ Setup your DUO Web lab

In order to setup your DUO Web lab, you just need to copy all the content of the [ duo_no ] folder into your web server doc directory.
If you don't have a web server, install XAMPP .  Easy to find on the INTERNET, and very easy to install.
Once XAMPP is intalled, for the windows version locate the [ htdocs ] folder and copy [ duo_no ] into it.

- Test your web server : http://localhost/duo_no
- Authenticate with username = patrick and password = password.

## 1/  How works the authentication without DUO secondary authentication

- The user authentication is handled by the valid.php file.
- Open it in the [ duo_no ] folder and have a look at it.  It is very straight forward

### 1.1/ Add DUO secondary authentication into this php login form

- Create duo_yes directory into your web server root documentation directory  ( ex : Apache in the htdocs folder )
- copy all the [ duo_no ] content and paste it into the  [ htdocs/duo_yes ] folder.
- Go to DUO Web documentation https://duo.com/docs/duoweb
- Go to the [ First Steps ] chapter and follow all instruction described in steps 1, 2 and 3
- In Step 4 click on the PHP Link. It will redirect you to the Github repository where are located all PHP resources you need.
	- Click on the [ clone or Download ] button and Download zip
	- Unzip the retreived zip file ( duo_php-master.zip )
	- In the [ htdocs/duo_yes ] folder create a subdirectory named [ js ] and copy into it the Duo-Web-v2.js file located into |[ duo_php-master/js ]  folder
	- In the [ htdocs/duo_yes ] folder create a subdirectory named [ scr ] and copy into it the Web.php file located into |[ duo_php-master/src ]  folder
	- The open the [ duo_php-master/demos/simple/index.php ] and have to look to it.  You will find 3 steps which will be the part we need to copy and paste into our valid.php file
	- open the valid_new.php file, have a look at where the 3 steps from the index.php sample have been pasted.
	- Modify the valid_new.php file with your duo credentials
	- AKEY must be an Alphanumerical string with 40 chars minimum. You can define it manually. An choose any strings you want.
	- copy valid_new.php to the [ htdocs/duo_yes ] folder as valid.php

## 2/ Test it

- Finally open your browser and connect to http://localhost/duo_yes
- Connect with username = patrick , password = password
- Then you should see the DUO self enrollment page appearing.
- Start you mobile device enrollment process
- Once done,  