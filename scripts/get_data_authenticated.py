import requests
from mohawk import Sender

url = 'http://localhost:5000/get-data-authenticated'
method = 'GET'
content = ''
content_type = ''

sender = Sender(
    {
        'id': 'client_id1',
        'key': 'client_key1',
        'algorithm': 'sha256'
    },
    url,
    method,
    content=content,
    content_type=content_type
)



response = requests.get(
    url,
    data=content,
    headers={
        'Authorization': sender.request_header,
        'Content-Type': content_type
    }
)

print('response:', response)
print('response.content:', response.content)
print('response.json():', response.json())
