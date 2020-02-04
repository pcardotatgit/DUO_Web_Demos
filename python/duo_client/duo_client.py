#!/usr/bin/env python


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

import json
import os
import duo_client
import time
import random
import cgi
import sys
import msvcrt

def duo_auth(user):
	# Configuration and information about objects to create.
	#TODO put these to env variables
	
	ikey = 'xxxxxxxxxxxxxx'
	skey = 'yyyyyyyyyyyyyy'
	akey = 'zzzzzzzzzzzzz'
	host = 'aaaaaaaaaaaaa'	
	auth_api = duo_client.Auth(
		ikey,
		skey,
		host
	)

	# Retrieve user info from API:
	ping_result = auth_api.ping()

	print('ping result :' + json.dumps(ping_result)) 

	# Retrieve user info from API:
	preauth_result = auth_api.preauth(username=user)

	print('preauth result :' + json.dumps(preauth_result)) 

	# Retrieve user info from API:
	if preauth_result['result']=='auth':
		auth_result = auth_api.auth(username=user,factor='push',device='auto')
	elif preauth_result['result']=='enroll':
		r=send_enrolement_to_webexteams(preauth_result['enroll_portal_url'],user)
		print('This user must enroll to DUO')
		status='enroll'
		return status
	else:
		print(preauth_result['status_msg'])
		status='error' #TODO  do enrole here and send enrolment process over webex (see json response for unrecongnized user)
		return status
	print('auth result :'+ json.dumps(auth_result)) 
		
	if auth_result['status']=='allow':
		status= auth_result['status']
	else:
		status= "error"
	return status
	
if __name__ == '__main__':
	print ('Click 2 or 3 times on a keystroke to break the loop ..')
	print ('Press the A key,  or another key')
	print ('The A key simulate a Tag Scanning and trigger DUO authentication')
	print ('any other key will stop the programm')
	tag='unknown'
	# Here after we simulate a loop waiting for a NFC TAG Scanning
	while 1:	
		# body of the loop ...
		if msvcrt.kbhit():
			if ord(msvcrt.getch()) == 27:
				print ('Escape')
				break
			if ord(msvcrt.getch()) == 97:
				print ('A')	
				tag='patrick'	
				break			
			print(ord(msvcrt.getch()))
			break	
	authentication=duo_auth(tag)
	if authentication=="allow":
		print('==============================')
		print('WELCOME !!!')
	else:
		print('FAILED')	
