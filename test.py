import json
import requests

url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
}
r1 = requests.get(url1, headers)
res1 = json.loads(r1.text)
data_all = json.loads(res1["data"])
e = data_all.keys()
#print (res1)
print (e)
#print(data_all)
#print(data_all["chinaDayList"])
