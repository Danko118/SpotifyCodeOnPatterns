# author:danko
# git: Danko118

from PIL import Image
from os.path import expanduser
from pathlib import Path
from spotipy.oauth2 import SpotifyClientCredentials
import enquiries
import json
import os
import requests
import shutil
import spotipy
import sys

home = Path(expanduser("~") + "/scop.json")

keys = ["client_id" , "client_secret"]
values = []

if not home.exists():
	values.append(enquiries.freetext("client_id:"))
	values.append(enquiries.freetext("client_secret:"))
	with open(home,'w') as jsonf:
		jsonf.write(json.dumps(dict(zip(keys,values))))
else:
	with open(home, 'r') as jsonf:
		values = json.loads(jsonf.read())

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=values["client_id"],client_secret=values["client_secret"]))
dir = os.path.abspath(os.curdir)

search_str = enquiries.freetext("Enter track name:")

searchResult = sp.search(search_str , limit=5)
parsedResult = json.dumps(searchResult)
jsonResult = json.loads(parsedResult)

options = ['Artist', 'Album', 'Track']
response = enquiries.choose("What are we generating?", options)

uri = []
name = []
i=0

for key in jsonResult["tracks"]["items"]:
	if options.index(response) == 0:
		uri.append(key["artists"][0]["uri"])
		name.append(key["artists"][0]["name"])
	elif options.index(response) == 1:
		uri.append(key["album"]["uri"])
		name.append(key["album"]["name"])
	else:
		uri.append(key["uri"])
		name.append(key["name"])
	i += 1

answer = enquiries.choose("Which " + response.lower() + "?", name)

print("Downloading spotify code...")
photo = requests.get("https://www.spotifycodes.com/downloadCode.php?uri=jpeg%2F000000%2Fwhite%2F640%2Fspotify%3A" + response.lower() + "%3A" + uri[name.index(answer)].replace("spotify:" + response.lower() +  ":","")).content

path = dir + "/out/" + answer + "/"
my_file = Path(path)

try:
	if not my_file.exists():
		os.mkdir(path)
except OSError:
	print ("Warning: cannot create out directory!")

with open(path + answer + ".png", "wb") as f:
	f.write(photo)

print("Making spotify code on pattern...")

shutil.copyfile(dir + "/patterns/1.png",path + answer + "_patt.png")
im1 = Image.open(path + answer + ".png")
im2 = Image.open(path + answer + "_patt.png")
im1 = im1.convert("1")
im1 = im1.convert("RGBA")
datas = im1.getdata()
newData = []
for item in datas:
    if item[0] == 0 and item[1] == 0 and item[2] == 0:
        newData.append((0, 0, 0, 0))
    else:
        newData.append(item)
im1.putdata(newData)
im1 = im1.resize((320, 80), Image.ANTIALIAS)
im1 = im1.resize((640, 160), Image.BICUBIC)
im1.save(path + answer + ".png", quality=95)
im2.paste(im1, (45, 295) , im1)
im2.save(path + answer + "_spotify_card.png", quality=95)
im1.close()
im2.close()
print("Removing temp files...")
os.remove(path + answer + "_patt.png")
os.remove(path + answer + ".png")
print("Complete!")

