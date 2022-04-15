from geopy.geocoders import Nominatim
import requests
loc = Nominatim(user_agent="GetLoc")
lc = "hsr layout bengaluru"
getLoc = loc.geocode(lc)
latitude = getLoc.latitude
longitude = getLoc.longitude
URL = "https://discover.search.hereapi.com/v1/discover"
api_key = "d6-oHLamtfluzYmMSL86mPgCa6QQrVu7-zfzexMgNKk" 
query = 'Laptop Service'
limit = 10
PARAMS = {'apikey':api_key,'q':query,'limit': limit,'at':'{},{}'.format(latitude,longitude)}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
data = list(data["items"])
# print(type(data))
data.sort(key=lambda x:int(x["distance"]))
print("---------------------------------------------")
for i in data:
	# print(i)
	if "contacts" in i:
		if "mobile" in i["contacts"][0]:
			print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}\nContact:{i['contacts'][0]['mobile'][0]['value']}")
		elif "phone" in i["contacts"][0]:
			print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}\nContact:{i['contacts'][0]['phone'][0]['value']}")
		else:	print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}")
	else:	print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}")
	print("---------------------------------------------")