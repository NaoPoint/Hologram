#set VLC to loop mode before running this script
import os
import requests
import time

CURRENTDIR = os.path.dirname(os.path.realpath(__file__))	#current script path
PARAMETERS = 'vlc --repeat --fullscreen --video-on-top --no-osd'
STANDBYTIME = 120	#time before stand by

starttime = time.time()
lastVideo = 0	#to compare new video
secondsPast = 0	#to reset video
inStandBy = True

def playVideo(num):
	global secondsPast
	secondsPast = 0	#reset counter

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
		res = requests.post('http://192.168.1.100:5000/get')	#flask endpoint
		videoNumber = res.json()

		if(videoNumber):	#map is active
			if(videoNumber != lastVideo):	#point changed (else do nothing)
				lastVideo = videoNumber
				playVideo(videoNumber)	#play video
				inStandBy = False	#restart counter
		else:
			raise Exception('Map is not active')

	except requests.ConnectionError as e:
		print(e)	#connection refused / aborted
	
	except Exception as e:
		print('Error: ' + str(e))

	finally:
		time.sleep(1.0 - ((time.time() - starttime) % 1.0))	#restart once a second