
tenantId = 32231
robotId ='581f92c7-f5e7-4411-b412-d3e12f102842'
adminkey = 'aWNzLWJpZy1jdXN0b21lci00MzA0YjYzNC02YzI3LTQ0YjItOTY5YS03M2ZhNTc2YTkyYzMtMTY0OTk5MDE4NjQ1Ng=='
adminscret='8108772a245740c4bab4f08c8bb1fdc2'
customerId = '4304b634-6c27-44b2-969a-73fa576a92c3'
robotsecret = 'c77784565de920aee6104d4b400299a5'

import time
timestamp=int(round(time.time() * 1000))
import random

nonce=random.randint(12345678,22345678)
import hashlib
md5=hashlib.md5()
...
uri=f'/v1/openapi/tenants/{tenantId}/robots/{robotId}/robot/ask'
md5.update(f"adminkey:{adminkey},adminsecret:{adminscret},customerId:{customerId},nonce:{nonce},robotsecret:{robotsecret},timestamp:{timestamp},uri:{uri}".encode('utf8'))
sign=md5.hexdigest()
print(sign)
url=f'https://bot.4paradigm.com{uri}?adminkey={adminkey}&customerId={customerId}&nonce={nonce}&timestamp={timestamp}&sign={sign}'
print(url)
import requests

userId='c97e2fcf-1ffc-4baa-9e98-504d3f04b046'
dic={
    "userId": f"{customerId}",
    "question": "保险公司会不会倒闭",
    "channel": "API",
    "questionType": "TEXT"
}
header={
"Content-Type":"application/json"
}
res=requests.post(url,data=dic)

print(res.text)