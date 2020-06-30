import requests

response = requests.get('http://localhost:5000/get-data')
print('response:', response)
print('response.content:', response.content)
print('response.json():', response.json())
