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
import random
from time import sleep
import time
import sys
import RPi.GPIO as GPIO
sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

GPIO.setmode(GPIO.BOARD)

rfid_reader = SimpleMFRC522()

def duo_auth(user):
	blink_led(7,5)
	GPIO.output(3, GPIO.HIGH) # Turn on
	GPIO.output(7, GPIO.HIGH) # Turn on
	# Configuration and information about objects to create.
	#TODO put these to env variables
	ikey = 'iiiiiiiiiiiiiiiiiiiiii'
	skey = 'ssssssssssssssssssssss'
	akey = 'aaaaaaaaaaaaaaaaaaaaaa'
	host = 'hhhhhhhhhhhhhhhhhhhhhh'	
	auth_api = duo_client.Auth(
		ikey,
		skey,
		host
	)

	# Retrieve user info from DUO API:
	ping_result = auth_api.ping()

	print('ping result :' + json.dumps(ping_result)) 

	# Retrieve user info from DUO API:
	preauth_result = auth_api.preauth(username=user)

	print('preauth result :' + json.dumps(preauth_result)) 

	if preauth_result['result']=='auth':
		auth_result = auth_api.auth(username=user,factor='push',device='auto')
	elif preauth_result['result']=='enroll':
		status='enroll'
		return status
	else:
		print(preauth_result['status_msg'])
		status='error'
		return status

	print('auth result :'+ json.dumps(auth_result)) 
	if auth_result['status']:
		status= auth_result['status']
	else:
		status= "error"
	return status

def leds_off():
	GPIO.output(3, GPIO.LOW)
	GPIO.output(5, GPIO.LOW)
	GPIO.output(7, GPIO.LOW)

def leds_init():
	GPIO.output(3, GPIO.LOW)
	GPIO.output(5, GPIO.LOW)
	GPIO.output(7, GPIO.HIGH)

def set_gpio():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setwarnings(False) # Ignore warning for now
	GPIO.setup(5, GPIO.OUT, initial=GPIO.LOW) # Set pin 5 to be an output pin and set initial value to low (off)  green = allow 
	GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW) # Set pin 3 to be an output pin and set initial value to low (off) red = red
	GPIO.setup(7, GPIO.OUT, initial=GPIO.HIGH) # Set pin 7 to be an output pin and set initial value to high (on) blue = ready

def blink_led(LED_PIN,number_of_blinks):
	for i in range(number_of_blinks): # Run forever
		GPIO.output(LED_PIN, GPIO.HIGH) # Turn on
		sleep(0.2) # Sleep for 1 second
		GPIO.output(LED_PIN, GPIO.LOW) # Turn off
		sleep(0.2) # Sleep for 1 second

if __name__ == '__main__':
	set_gpio() # init GPIO
	try:
		while True:
			print("Waiting for a tag to be scanned by the NFC reader")
			id, user = rfid_reader.read()
			print(id)
			print(user)
			r=duo_auth(user)
			if r=="allow":
				print('loging authorised by DUO MFA !')
				leds_off()
				blink_led(5,5)
				GPIO.output(5, GPIO.HIGH) # Turn on
				sleep(2) # Sleep for 2 second
				GPIO.output(5, GPIO.LOW) # Turn on				
				leds_init()
			elif r=="deny":
				print('loging denied by DUO MFA !')
				leds_off()				
				blink_led(3,5)	
				GPIO.output(3, GPIO.HIGH) # Turn on
				sleep(1) # Sleep for 1 second
				GPIO.output(3, GPIO.LOW) # Turn on		
				leds_init()
			elif r=='enroll':
				print('User not know by DUO. This is a New user enrolement process to be sent to him')
				blink_led(3,5)	
				GPIO.output(3, GPIO.HIGH) # Turn on
				sleep(1) # Sleep for 1 second
				GPIO.output(3, GPIO.LOW) # Turn on		
				leds_init()
			else: #fall back to PIN code using keypad
				print('Fist login failed !')
				GPIO.output(3, GPIO.HIGH) # Turn on
				sleep(2) # Sleep for 2 second
	finally:
		GPIO.cleanup()
