#set VLC to loop mode before running this script
import os
import requests
import time

CURRENTDIR = os.path.dirname(os.path.realpath(__file__))	#current script path
PARAMETERS = 'vlc --repeat --fullscreen --video-on-top --no-osd --one-instance'
STANDBYTIME = 120	#time before stand by

starttime = time.time()
lastVideo = 0	#to compare new video
secondsPast = 0	#to reset video
inStandBy = True
exception = False	#in case of exception

def playVideo(num):
	global secondsPast, exception
	secondsPast = 0	#reset counter
	exception = False	#reset exception flag

	fullPath = CURRENTDIR + '/media/' + num + '.mp4'	#path to video

	if os.path.isfile(fullPath):	#check if video exists
		os.system('start ' + PARAMETERS + ' ' + fullPath)	#play video
		print(num)
	else:
		raise Exception(num + ' is not a valid video number')

while True:	#infinite loop
	if(not inStandBy):
		secondsPast += 1	#increase counter
		if(secondsPast >= STANDBYTIME):
			playVideo('0')	#default video
			inStandBy = True	#stop counter

	try:
		try:
			res = requests.post('http://192.168.1.100:5000/get')	#flask endpoint

		except requests.ConnectionError as e:
			raise Exception('The script is not active on the main machine')	#connection refused / aborted
	
		videoNumber = res.json()

		if(videoNumber):	#map is active
			if(videoNumber != lastVideo):	#point changed (else do nothing)
				lastVideo = videoNumber
				playVideo(videoNumber)	#play video
				inStandBy = False	#restart counter
		else:
			raise Exception('Map is not active')

	except Exception as e:
		if(not exception):	#display default video
			print('Error: ' + str(e))

			playVideo('0')
			exception = True

	finally:
		time.sleep(1.0 - ((time.time() - starttime) % 1.0))	#restart once a second