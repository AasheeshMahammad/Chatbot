from utils import init_db, insertdb, viewdb
import requests
from geopy.geocoders import Nominatim
 

def show_locs(latitude,longitude,limit):
    URL = "https://discover.search.hereapi.com/v1/discover"
    api_key = "d6-oHLamtfluzYmMSL86mPgCa6QQrVu7-zfzexMgNKk" 
    query = 'Laptop Service'
    PARAMS = {'apikey':api_key,'q':query,'limit': limit,'at':'{},{}'.format(latitude,longitude)}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    data = list(data["items"])
    data.sort(key=lambda x:int(x["distance"]))
    print("---------------------------------------------")
    for i in data:
        # print(i)
        if "contacts" in i:
            if "mobile" in i["contacts"][0]:
                print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}m\nContact:{i['contacts'][0]['mobile'][0]['value']}")
            elif "phone" in i["contacts"][0]:
                print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}m\nContact:{i['contacts'][0]['phone'][0]['value']}")
            else:	print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}m")
        else:	print(f"Title:{i['title']}\nAddress:{i['address']['label']}\nDistance:{i['distance']}m")
        print("---------------------------------------------")
    return data

if __name__ == "__main__":
	# init_db()
	# insertdb("Rohith","Gangadhara","Asus FX505GE", "Dabba Service Centre", "Dabba Road, Dabba Cross, Dabba Layout, Dabbapura-560420")
	# insertdb("Santosh","","HP FX505GE", "Dabba Service Centre", "Dabba Road, Dabba Cross, Dabba Layout, Dabbapura-560420")
	# viewdb()
	loc = Nominatim(user_agent="GetLoc")
	getLoc = loc.geocode("lakkasandra bengaluru")
	latitude = getLoc.latitude
	longitude = getLoc.longitude
	data=show_locs(latitude,longitude,2)
	print(data)