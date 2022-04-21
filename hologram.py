import os
import requests
import time

starttime = time.time()

while True:	#infinite loop
	try:
		res = requests.post('http://192.168.1.15:5000/get')	#flask endpoint
		videoNumber = res.json()

		if(videoNumber):	#map is active
			currentDir = os.path.dirname(os.path.realpath(__file__))	#current script path
			fullPath = currentDir + "/media/" + videoNumber + ".mp4"	#path to video
		
			if os.path.isfile(fullPath):	#check if video exists
				os.system("start " + fullPath)	#play video
				print(videoNumber)
			else:
				raise Exception(videoNumber + " is not a valid video number")
		else:
			raise Exception("Map is not active")

	except requests.ConnectionError as e:
		print(e)	#connection refused / aborted
	
	except Exception as e:
		print("Error: " + str(e))

	finally:
		time.sleep(1.0 - ((time.time() - starttime) % 1.0))	#restart once a second