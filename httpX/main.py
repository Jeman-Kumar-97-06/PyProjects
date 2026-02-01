import httpx
r = httpx.get('http://jsonplaceholder.typicode.com/posts/1')
print(r.text)
print(r.json())
print(r.status_code)