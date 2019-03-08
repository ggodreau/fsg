import requests

res = requests.post('http://172.19.0.3:80/setrule', json={"id":"b", "scale":"1", "logic":"1"})
print(res.content)

res = requests.post('http://172.19.0.3:80/getrule', json={"id":"a"})
print(res.content)
