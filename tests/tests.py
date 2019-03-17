import requests

res = requests.post('http://172.19.0.3:80/setrule', json={"id":"a", "unit":1, "logic":0, "templ": 22.22, "temph": 33.4})
print(res.content)

res = requests.get('http://172.19.0.3:80/getrule', json={"id":"a"})
print(res.content)

res = requests.post('http://172.19.0.3:80', json={"id":"a", "value": 110.3, "unit": 0})
print(res.content)
