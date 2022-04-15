import requests

URL = "https://discover.search.hereapi.com/v1/discover"
latitude = 12.96643
longitude = 77.5871
api_key = "d6-oHLamtfluzYmMSL86mPgCa6QQrVu7-zfzexMgNKk" # Acquire from developer.here.com
#OEyNuBrUN0tyiFUTw1FyiypLWd5hRefw0InWZyoMUBA
query = 'laptop service'
limit = 5

PARAMS = {
            'apikey':api_key,
            'q':query,
            'limit': limit,
            'at':'{},{}'.format(latitude,longitude)
         } 

# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
data = r.json()
print(data)