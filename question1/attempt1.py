import http.client
import json


URL = "20.244.56.144"
PATH = "/test/register"

connection = http.client.HTTPConnection(URL)

data = {
    'companyName': "goMart",
    'ownerName': "Rahul",
    'rollNo': "1",
    'ownerEmail': "22cs407.lavanya@sjec.ac.in",
    'accessCode': "umHPpw"
}

json_data = json.dumps(data)

headers = {
    "Content-Type": "application/json",
    "Accept": "text/plain"
}

connection.request("POST", PATH, body=json_data, headers=headers)

response = connection.getresponse()
response_data = response.read()

print("Status:", response.status)
print("Response:", response_data.decode())

connection.close()































