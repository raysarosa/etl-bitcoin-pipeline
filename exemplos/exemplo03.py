import requests

url = 'https://jsonplaceholder.typicode.com/comments'
params = {'postId': 1}

response = requests.get(url, params=params)
comments = response.json()

print(f'Total of {len(comments)} comments found')
print(f'Erro : {response.status_code} - {response.text}')