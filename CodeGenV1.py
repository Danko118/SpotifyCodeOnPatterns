# author:danko
# git: Danko118

from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import sys
import json
import requests
from PIL import Image
import shutil
import os

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="YOUR_CLIENT_ID",client_secret="YOUR_CLIENT_SECRET_CODE"))
dir = os.path.abspath(os.curdir)

if len(sys.argv) > 1:
    search_str = sys.argv[1]
else:
    pprint.pprint("Warning: missing requered argument!")
    exit()


searchResult = sp.search(search_str , limit=1)
parsedResult = json.dumps(searchResult)
jsonResult = json.loads(parsedResult)
print("Downloading spotify code...")
photo = requests.get("https://www.spotifycodes.com/downloadCode.php?uri=jpeg%2F000000%2Fwhite%2F640%2Fspotify%3Atrack%3A" + jsonResult["tracks"]["items"][0]["uri"].replace("spotify:track:","")).content

try:
	os.mkdir(dir + "/out/" + search_str);
	path = dir + "/out/" + search_str + "/"
except OSError:
	print ("Warning: cannot create out directory!")

with open(path + search_str + ".png", "wb") as f:
	f.write(photo)

print("Making spotify code on pattern...")

shutil.copyfile(dir + "/patterns/1.png",path + search_str + "_patt.png")
im1 = Image.open(path + search_str + ".png")
im2 = Image.open(path + search_str + "_patt.png")
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
im1.save(path + search_str + ".png", quality=95)
im2.paste(im1, (45, 295) , im1)
im2.save(path + search_str + "_spotify_card.png", quality=95)
im1.close()
im2.close()
print("Complete!")