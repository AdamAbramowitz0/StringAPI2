import requests
import json
host = "localhost:5000"

url = "http://"+host+"/addUser"
data2 = {"apiKey": "6314609", "instanceName": "Chirp", "userName": "test", "code": 0}
z=requests.post(url,data=data2).text

print(z)
