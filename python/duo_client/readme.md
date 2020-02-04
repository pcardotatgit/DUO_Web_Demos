# DUO Client How to do

	- This demonstration is a simpler version of the demo of DUO MFA used for user Authentication thanks to NFC Card Reader
		- https://www.youtube.com/watch?v=NgMu5lcIi9Y
	- This is exactly the same demo but without the NFC card reader
	- This is a proof of concept which demonstrate how it can be easily to create / integrate into what could be an IOT device DUO secondary Authentication 	when the device tries to connect to an application ( or to the network ).
	- The duo client automatically sends the push DUO MFA when a NFC tag is read 

# 0/ Install the duo_client module

	- pip install duo_client

# Run it and Test it

	- We assume here that you previously rolled out the DUO WEB PHP lab.
		- And normally you have generated in your DUO Account, the credentials you need to make this demo work
	- open the duo_client.py and add you DUO credentials
	- run the script
		- python dou_client.py
		- At anytime, type 2 or 3 times on the A key. It simulate a NFC Tag Scanning