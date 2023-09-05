import requests
import json

url3 = "htt://stringapi.net/addABunchOfUsers"

data4 = {"apiKey": "3260497", "instanceName": "AlphaTest","users":["bobby","joey","TTimmy"]}

q = requests.post(url3, json=data4).text
print(q)