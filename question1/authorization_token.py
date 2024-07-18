import http.client
import json

URL = "20.244.56.144"
PATH = "/test/auth"

connection = http.client.HTTPConnection(URL)

data = {
    "companyName":"goMart",
           "clientID":"4c1b0bae-6bd1-4dea-b691-96ab9016c211",
           "clientSecret":"gcXxrbaWlOXnfVcl",
           "ownerName":"Rahul",
           "ownerEmail":"22cs407.lavanya@sjec.ac.in",
           "rollNo":"1"
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