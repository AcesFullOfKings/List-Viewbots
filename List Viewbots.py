import requests
import ctypes

from itertools import combinations
from difflib import SequenceMatcher
from time import sleep
from os import path
from contextlib import suppress


ctypes.windll.kernel32.SetConsoleTitleW("Viewbot Detector") # set window name

similarity = lambda a, b: SequenceMatcher(None, a, b).ratio()

views_url = ""

bound = 0

if path.exists("config.txt"):
	with open("config.txt", "r") as f:
		file = f.read()
	for line in file.split("\n"):
		with suppress(ValueError):
			key, val = line.split("=")
			if key.replace(" ", "") == "bound" and 0 < int(val) < 100: # ValueError if val not formatted properly (eg is str), will be suppressed and line ignored
				bound = int(val) 
				break
			elif key == "channel" and 0 < len(str(val)) <= 20 and val.lower()!="valkia":
				views_url = "https://tmi.twitch.tv/group/user/{channel}/chatters".format(channel=val)
				print("Using channel {c} from config".format(c=val))

if views_url == "":
	views_url = "https://tmi.twitch.tv/group/user/valkia/chatters"
	print("Using channel Valkia (default)")
if bound == 0:
	bound = 75
	print("Minimum similarity is {x}% (default value)".format(x=bound))
else:
	print("Minimum similarity is {x}% (read from config)".format(x=bound))

viewers = requests.get(views_url).json()["chatters"]["viewers"]
name_pairs = list(combinations(viewers, 2))

bound = bound / 100

print("There are {n} viewers in the list. Searching for similar names..\n\n".format(n=len(viewers)))

found = False

for a,b in name_pairs:
	match = similarity(a,b)
	if match >= bound:
		found = True
		print("{a} | {b} ({x}% match)".format(a=a.rjust(15), b=b.ljust(15), x=round(match*100, 1)))

if not found:
	print("No sufficiently similar names found.")
else:
	print("\nDone.")

for i in range(3):
	ctypes.windll.user32.FlashWindow(ctypes.windll.kernel32.GetConsoleWindow(), True)
	sleep(1.5)

input()